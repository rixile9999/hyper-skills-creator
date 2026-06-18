#!/usr/bin/env python3
"""Search the local Claude plugin/skill catalog and rank candidates.

This is hyper-skills' fast, offline first-pass filter. It reads the
marketplace catalog cache that Claude Code already maintains on disk, plus the
list of installed plugins and the user's personal skills directory, and ranks
candidates against a free-text query.

Why a script instead of doing this in-context: the catalog is ~330KB of JSON
covering 200+ plugins and hundreds of skills. Loading it into the conversation
to eyeball it would burn context every invocation. Ranking deterministically
here is faster, cheaper, and reproducible — the agent only sees the shortlist.

Usage:
    python3 search_catalog.py "postgres query optimization" [--limit 12] [--json]
    python3 search_catalog.py --category database --limit 20
    python3 search_catalog.py "react" --skills-only   # rank individual skills

Output (default human form): a ranked table the agent turns into choices.
With --json: structured records for programmatic branching.

Scoring favors relevance first, then popularity (installs) as a tiebreaker,
and lightly penalizes heavy always-on token cost. The weights are deliberately
simple and legible — tune them in the WEIGHTS block if your taste differs.
"""
import argparse
import json
import math
import os
import re
import sys
from glob import glob

HOME = os.path.expanduser("~")
CATALOG = os.path.join(HOME, ".claude/plugins/plugin-catalog-cache.json")
INSTALLED = os.path.join(HOME, ".claude/plugins/installed_plugins.json")
USER_SKILLS_DIRS = [
    os.path.join(HOME, ".claude/skills"),
    os.path.join(HOME, ".agents/skills"),  # Codex-style, harmless if absent
]

WEIGHTS = {
    "name_hit": 6.0,        # query term appears in plugin/skill name
    "skill_name_hit": 5.0,  # query term appears in a contained skill's name
    "desc_hit": 2.0,        # query term appears in the description
    "category_hit": 3.0,    # query term matches the category
    "popularity": 1.0,      # coefficient on log10(installs+1)
    "token_penalty": 0.15,  # coefficient on log10(always_on_chars+1)
}


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def installed_plugin_names():
    data = load_json(INSTALLED)
    if not data or "plugins" not in data:
        return set()
    # keys look like "name@marketplace"
    return {k.split("@")[0] for k in data["plugins"].keys()}


def user_skill_names():
    names = set()
    for base in USER_SKILLS_DIRS:
        for sk in glob(os.path.join(base, "*", "SKILL.md")):
            names.add(os.path.basename(os.path.dirname(sk)))
    return names


def terms_of(query):
    return [t for t in re.split(r"[^a-z0-9]+", (query or "").lower()) if len(t) > 1]


def always_on_chars(entry):
    """Best-effort always-on context cost across known models."""
    toks = entry.get("tokens") or {}
    best = 0
    for model in toks.values():
        best = max(best, model.get("always_on", 0))
    return best


def score_entry(entry, terms, category_filter):
    me = entry.get("marketplace_entry", {}) or {}
    name = (entry.get("plugin") or me.get("name") or "").lower()
    desc = (me.get("description") or "").lower()
    cat = (me.get("category") or "").lower()
    skills = [s.get("name", "").lower() for s in entry.get("components", {}).get("skills", [])]

    if category_filter and category_filter.lower() not in cat:
        return None

    score = 0.0
    matched_skills = []
    for t in terms:
        if t in name:
            score += WEIGHTS["name_hit"]
        if t in desc:
            score += WEIGHTS["desc_hit"]
        if t in cat:
            score += WEIGHTS["category_hit"]
        for sk in skills:
            if t in sk:
                score += WEIGHTS["skill_name_hit"]
                matched_skills.append(sk)

    # With no terms (pure category browse) everything in-category is a candidate.
    if not terms:
        score = 1.0

    if score <= 0:
        return None

    installs = entry.get("unique_installs", 0) or 0
    score += WEIGHTS["popularity"] * math.log10(installs + 1)
    score -= WEIGHTS["token_penalty"] * math.log10(always_on_chars(entry) + 1)

    return {
        "score": round(score, 3),
        "plugin": entry.get("plugin"),
        "source": entry.get("source"),
        "category": me.get("category"),
        "description": me.get("description"),
        "homepage": me.get("homepage"),
        "installs": installs,
        "always_on_chars": always_on_chars(entry),
        "skills": [s.get("name") for s in entry.get("components", {}).get("skills", [])],
        "matched_skills": sorted(set(matched_skills)),
        "n_commands": len(entry.get("components", {}).get("commands", [])),
        "n_agents": len(entry.get("components", {}).get("agents", [])),
    }


def main():
    ap = argparse.ArgumentParser(description="Search the local Claude plugin/skill catalog.")
    ap.add_argument("query", nargs="?", default="", help="free-text query")
    ap.add_argument("--category", help="restrict to a marketplace category substring")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--skills-only", action="store_true",
                    help="rank individual skills rather than whole plugins")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    ap.add_argument("--catalog", default=CATALOG, help="path to catalog cache")
    args = ap.parse_args()

    catalog = load_json(args.catalog)
    if not catalog:
        print(f"!! catalog not found or unreadable at {args.catalog}\n"
              f"   Run `claude plugin marketplace` once to populate it, then retry.",
              file=sys.stderr)
        sys.exit(2)

    plugins = catalog.get("catalog", {}).get("plugins", {})
    terms = terms_of(args.query)
    installed = installed_plugin_names()
    have_skills = user_skill_names()

    ranked = []
    for entry in plugins.values():
        r = score_entry(entry, terms, args.category)
        if r:
            r["installed"] = r["plugin"] in installed
            r["forked_locally"] = r["plugin"] in have_skills
            ranked.append(r)

    ranked.sort(key=lambda r: r["score"], reverse=True)
    ranked = ranked[: args.limit]

    if args.skills_only:
        rows = []
        for r in ranked:
            shown = r["matched_skills"] or r["skills"]
            for sk in shown:
                rows.append({"skill": sk, "plugin": r["plugin"],
                             "score": r["score"], "category": r["category"],
                             "installs": r["installs"], "installed": r["installed"]})
        if args.json:
            print(json.dumps(rows[: args.limit], indent=2))
        else:
            print(f"# Skill matches for: {args.query!r}\n")
            for x in rows[: args.limit]:
                mark = " [installed]" if x["installed"] else ""
                print(f"  {x['score']:6.2f}  {x['skill']:<32} ({x['plugin']}, {x['category']}){mark}")
        return

    if args.json:
        print(json.dumps(ranked, indent=2))
        return

    fetched = catalog.get("fetchedAt", "?")
    print(f"# {len(ranked)} candidates for: {args.query!r}"
          f"{' / cat=' + args.category if args.category else ''}   (catalog fetched {fetched})\n")
    for r in ranked:
        flags = []
        if r["installed"]:
            flags.append("installed")
        if r["forked_locally"]:
            flags.append("forked")
        flag = (" [" + ", ".join(flags) + "]") if flags else ""
        print(f"## {r['score']:6.2f}  {r['plugin']}  ({r['category']}){flag}")
        print(f"   {r['description']}")
        bits = [f"{r['installs']:,} installs",
                f"~{r['always_on_chars']} always-on chars",
                f"{len(r['skills'])} skills"]
        if r["n_commands"]:
            bits.append(f"{r['n_commands']} cmds")
        if r["n_agents"]:
            bits.append(f"{r['n_agents']} agents")
        print("   " + " · ".join(bits))
        if r["matched_skills"]:
            print(f"   matched skills: {', '.join(r['matched_skills'])}")
        elif r["skills"]:
            preview = ", ".join(r["skills"][:6])
            more = "" if len(r["skills"]) <= 6 else f", +{len(r['skills']) - 6} more"
            print(f"   skills: {preview}{more}")
        if r["homepage"]:
            print(f"   {r['homepage']}")
        print()


if __name__ == "__main__":
    main()

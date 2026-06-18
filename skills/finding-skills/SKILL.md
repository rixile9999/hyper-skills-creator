---
name: finding-skills
description: Use when the user wants to find, discover, choose, compare, recommend, adopt, or install a Claude coding-agent skill or plugin but isn't sure which one fits — phrases like "is there a skill for X", "what skill should I use", "find me a skill/plugin", "recommend a skill for my workflow", "I have too many plugins, which ones help", or any time someone is overwhelmed by skill choice and wants help narrowing it down interactively. Hands off to personalizing-skills when the user wants to tune the chosen skill rather than adopt it as-is.
---

# Finding Skills

## Overview

There are now hundreds of coding-agent skills and plugins, and the hard part is
no longer *building* one — it's **choosing** the right one for a given person.
There's no universally correct skill; the effective set depends on the user's
own taste, skill level, and workflow. This skill is a **matchmaker**: the user
says roughly what they want, you search the available pool, narrow it down *with
them* through interactive choices, and land on a skill to adopt.

**Core principle:** you are a guide, not an oracle. Never silently pick "the
best" skill. Surface real candidates with honest trade-offs and let the user
steer at each fork. The branching *is* the product.

**The loop:** `Clarify intent → Search the pool → Narrow interactively →
Adopt / refine / hand off`. Loop back any time — narrowing too far with nothing
good means widening the search.

This is the discovery half of `hyper-skills-creator`. When the chosen skill is a
good base but needs tuning, **hand off to the `personalizing-skills` skill**.

## When to Use

- "Is there a skill/plugin for <task>?" / "What should I use for <task>?"
- "Recommend me a skill for my React + Postgres workflow."
- "I installed 30 plugins and I'm lost — which ones actually help me?"
- Any moment the user is paralyzed by skill choice.

**Not for:** tuning an already-chosen skill (use `personalizing-skills`), or
authoring a brand-new skill from a blank page (`skill-creator` /
`superpowers:writing-skills`).

## Step 1 — Clarify intent

Don't search on a vague request. Get just enough to query well. If the user was
specific ("postgres query tuning skill"), skip ahead. If vague ("I want a good
skill"), ask **one** focused branching question first — the catalog's own
categories make natural branches:

> development · productivity · database · security · monitoring · deployment ·
> design · testing · learning

Use `AskUserQuestion` with 2–4 of these (plus the user's own free-text "Other")
to fix a direction before searching. Capture: the *task*, the *stack/tools*
involved, and whether they want a single skill or a whole workflow set.

Ask only what you need *to search well* — one question is usually enough here.
The real narrowing happens at Step 3 once there are concrete candidates on the
table, so don't front-load every decision.

## Step 2 — Search the pool

The candidate pool is **the Claude marketplace + web search**. Search in this
order, stopping as soon as you have a strong shortlist:

1. **Local catalog (fast, offline first pass).** Run the bundled script:
   ```bash
   python3 scripts/search_catalog.py "<query terms>" --limit 12
   python3 scripts/search_catalog.py "<query>" --skills-only   # rank skills, not plugins
   python3 scripts/search_catalog.py --category database        # browse a category
   ```
   It ranks the on-disk catalog cache by relevance + popularity, marks what's
   already `[installed]`/`[forked]`, and reports install counts and token cost.
   This is your default — it's instant and covers 200+ plugins.

   *Watch for cross-domain noise:* scoring matches query terms anywhere, so a
   generic word like "test" can surface security/compliance plugins. Sanity-check
   that the `matched skills` are actually on-topic, and add `--category` to cut a
   noisy field (e.g. `--category development`) before trusting the ranking.

2. **Live marketplace (freshness / confirmation).** Refresh when the cache is
   clearly stale (its printed `fetchedAt` is more than ~2 weeks old) or when the
   user expects something newer than that; otherwise the cache is fine. Refresh
   and re-search via the `claude plugin` CLI.

3. **Web search (breadth / community skills).** When the marketplace has no good
   fit, use `WebSearch`/`WebFetch` for GitHub and community skills. Treat these
   as *unverified* — flag provenance and skim the source before recommending.

**Full pool & search mechanics:** read `references/pool-and-search.md`.

## Step 3 — Narrow interactively

This is the heart of the skill. Turn the shortlist into choices, never a wall of
text. Guidance:

- **Present 2–4 candidates at a time** via `AskUserQuestion`, each option a real
  candidate. In the description give the honest hook: what it's good at, install
  count (social proof), always-on token cost (it's always loaded — cost matters),
  and the catch. Recommended pick goes first, labeled "(추천)".
- **If the shortlist is large**, branch on an axis first (sub-domain, official
  vs community, heavy-vs-light) to halve the field before showing leaf
  candidates.
- **Let the user dig in.** Offer a "show me details / compare top 2" path that
  reads the candidate's actual SKILL.md before committing.
- **Dead end is a valid branch.** If nothing fits, loop to Step 2 with widened
  terms or the web, or suggest synthesizing a new skill (that's a
  `personalizing-skills` path).
- **No interactive UI?** If `AskUserQuestion` isn't available (headless/non-
  interactive run), present the same choices as a numbered list in text and ask
  the user to reply with a number.

Keep going until the user lands on a candidate.

## Step 4 — Adopt, refine, or hand off

Once a candidate is chosen, ask what to do with it. **Present this as a choice —
the right action is situational, so let the user pick:**

| Action | What happens | When it fits |
|--------|--------------|--------------|
| **Adopt as-is** | Install/enable the plugin or skill unchanged | The skill already fits; user just wants it on |
| **Personalize** | Hand off to `personalizing-skills` | Good base, wrong defaults |
| **Refine / keep looking** | Back to Step 2/3 | Not quite right |

For **Adopt**: install via the marketplace, or for a single skill copy it into
`~/.claude/skills/`. **Confirm the source before installing anything** —
installing runs third-party content. See `references/pool-and-search.md`. After
adopting, a quick trigger check is worthwhile: fire 1–2 realistic sentences and
confirm it activates (the `personalizing-skills` skill's `verify` reference has
deeper options if wanted).

For **Personalize**: hand the chosen candidate to the **`personalizing-skills`**
skill, which owns the tuning modes (fork & edit / preference overlay / synthesize)
and verification. Pass along what you learned: the candidate, why it's close, and
any stack/preference cues the user already gave.

## Quick Reference

```
intent ──▶ search_catalog.py ──▶ [shortlist] ──▶ AskUserQuestion (narrow)
   ▲            │ thin/stale?            │                 │
   └── widen ◀──┴── live CLI / web ◀─────┘          chosen candidate
                                                          │
                            ┌── adopt ──────── install / copy to ~/.claude/skills
        action choice ──────┼── personalize ── → personalizing-skills
                            └── refine ─────── back to search
```

## Example

For a full run that continues from search all the way into the personalization
flow — sourcing `grill-me` (community, via web search) and
`test-driven-development` (marketplace), then handing off to build a
"clarify the spec (architecture + principles), then build TDD" skillset — plus a
one-step adopt-as-is case, see `EXAMPLES.md` at the plugin root.

## Common Mistakes

- **Auto-picking the top result.** Defeats the purpose. Always present choices;
  the user's taste is the deciding input, not your ranking.
- **Ignoring token cost.** A skill's `description` is always in context. A bloaty
  always-on cost is a real downside — surface it.
- **Installing without confirming provenance.** Marketplace and especially web
  skills are third-party code. Show the source/homepage and get a yes first.
- **Over-asking.** If intent is already specific, don't interrogate — search.
- **Treating web results as trusted.** Flag them as unverified; skim before
  recommending.
- **Doing the tuning here.** Personalization lives in `personalizing-skills` —
  hand off rather than reinventing it.

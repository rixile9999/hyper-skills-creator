---
name: finding-skills
description: Use when the user wants to find, discover, choose, compare, recommend, adopt, or install a Claude coding-agent skill or plugin but isn't sure which one fits — phrases like "is there a skill for X", "what skill should I use", "find me a skill/plugin", "recommend a skill for my workflow", "I have too many plugins, which ones help", or any time someone is overwhelmed by skill choice and wants help narrowing it down interactively. Also covers decomposing a feature into capabilities and finding small unit skills (local first) to compose rather than one do-everything skill. Hands off to customizing-skills when the user wants to compose or tune the chosen skill(s) rather than adopt as-is.
---

# Finding Skills

## Overview

There are now hundreds of coding-agent skills and plugins, and the hard part is
no longer *building* one — it's **choosing** the right one for a given person.
There's no universally correct skill; the effective set depends on the user's
own taste, skill level, and workflow. This skill is a **matchmaker**: the user
says roughly what they want, you search the available pool, narrow it down *with
them* through interactive choices, and land on what to adopt.

**A feature is rarely one skill.** Before hunting for a single skill that does
everything, decompose the need into capabilities and look for small **unit
skills** — local ones first — that each cover a part. Often the best answer is a
*set* of units composed together, not one monolith. Composing well-maintained
units (kept as-is, glued by a thin overlay) keeps the whole thing light and lets
each unit keep its **upstream updates** — forking one big skill severs that. So
search for units to compose first; fall back to a single skill only when the
capability really is atomic.

**Core principle:** you are a guide, not an oracle. Never silently pick "the
best" skill. Surface real candidates with honest trade-offs and let the user
steer at each fork. The branching *is* the product.

**The loop:** `Clarify intent → Decompose into capabilities → Gather unit-skill
candidates → Narrow interactively → Adopt / compose / refine / hand off`.
Candidates come from any source (including ones the user brings in) — getting
them is the cheap part; the narrowing and hand-off are the value. Loop back any
time — narrowing too far with nothing good means widening the pool.

This is the discovery half of `hyper-skills-creator`. When the chosen skill (or
set of units) is a good base but needs tuning or wiring together, **hand off to
the `customizing-skills` skill**, which leads with composing units under a thin
overlay.

## When to Use

- "Is there a skill/plugin for <task>?" / "What should I use for <task>?"
- "Recommend me a skill for my React + Postgres workflow."
- "I installed 30 plugins and I'm lost — which ones actually help me?"
- Any moment the user is paralyzed by skill choice.

**Not for:** tuning an already-chosen skill (use `customizing-skills`), or
authoring a brand-new skill from a blank page (`skill-creator` /
`superpowers:writing-skills`).

## Step 1 — Clarify intent, then decompose into capabilities

Don't search on a vague request. Get just enough to query well. If the user was
specific ("postgres query tuning skill"), skip ahead. If vague ("I want a good
skill"), ask **one** focused branching question first — the catalog's own
categories make natural branches:

> development · productivity · database · security · monitoring · deployment ·
> design · testing · learning

Use `AskUserQuestion` with 2–4 of these (plus the user's own free-text "Other")
to fix a direction before searching. Capture: the *task*, the *stack/tools*
involved, and whether they want a single skill or a whole workflow set.

**Then decompose.** Before searching, break the stated need into the
capabilities it actually requires — "set up a TDD workflow" is really *clarify
the spec* + *write tests first* + *run/verify*. Each capability becomes its own
search. A need that splits into 2–4 capabilities is a strong signal to look for
**unit skills to compose** rather than one do-everything skill. If the need is
genuinely atomic, it's a single search — don't manufacture parts that aren't
there.

Ask only what you need *to search well* — one question is usually enough here.
The real narrowing happens at Step 3 once there are concrete candidates on the
table, so don't front-load every decision.

## Step 2 — Get candidates on the table

Raw retrieval is a commodity — the marketplace, the official `/plugin` browser,
and several community searchers all do it, some over live directories. **Don't
compete on search.** This skill's value is the *interactive narrowing and the
hand-off to customization* (Steps 3–4), so treat search as a thin, swappable
input layer: get a decent shortlist by whatever path is cheapest, then move on.

**Search per capability, local first.** If Step 1 split the need into parts, run
a search for each part and keep a small shortlist *per capability* — you're
assembling a set, not crowning one winner. Start with what's already on disk
(local skills and the cached catalog; `--skills-only` ranks individual units): a
unit the user already has composes for free and is the lightest possible answer.
Only widen to live/web sources for the capabilities nothing local covers.

Candidates can come from **any** of these — use the first that yields a strong
shortlist, and freely accept results the user already gathered elsewhere:

1. **BYO candidates (preferred when available).** If the user already ran another
   discovery tool (`skillless`, `find-skills`, the `/plugin` browser, a list a
   colleague sent), have them paste the names/URLs. Take those as the shortlist
   directly — no reason to re-search. We consume other searchers' output rather
   than racing them.

2. **Local catalog (fast offline first pass).** When there's nothing to BYO, the
   bundled script is the cheapest first look — instant, offline, covers 200+
   plugins:
   ```bash
   python3 scripts/search_catalog.py "<query terms>" --limit 12
   python3 scripts/search_catalog.py "<query>" --skills-only   # rank skills, not plugins
   python3 scripts/search_catalog.py --category database        # browse a category
   ```
   It ranks the on-disk catalog cache by relevance + popularity, marks what's
   already `[installed]`/`[forked]`, and reports install counts and token cost.
   *Watch for cross-domain noise:* scoring matches query terms anywhere, so a
   generic word like "test" can surface security/compliance plugins. Sanity-check
   the `matched skills` are on-topic, and add `--category` to cut a noisy field.
   It's a cache, so it goes stale — confirm anything important against a live
   source (below) before recommending strongly.

3. **Live sources (freshness / breadth).** When the cache is stale (its printed
   `fetchedAt` is more than ~2 weeks old), thin, or the user expects something
   newer: refresh and query live via the `claude plugin` CLI, and widen to
   community directories and GitHub with `WebSearch`/`WebFetch`. Treat web/
   community results as *unverified* — flag provenance and skim the source before
   recommending.

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
  `customizing-skills` path).
- **No interactive UI?** If `AskUserQuestion` isn't available (headless/non-
  interactive run), present the same choices as a numbered list in text and ask
  the user to reply with a number.

Keep going until the user lands on a candidate.

## Step 4 — Adopt, refine, or hand off

Once a candidate is chosen, ask what to do with it. **Present this as a choice —
the right action is situational, so let the user pick:**

| Action | What happens | When it fits |
|--------|--------------|--------------|
| **Adopt as-is** | Install/enable the skill(s) unchanged | A single skill — or a set of units that already work side by side — fits; user just wants them on |
| **Compose** | Hand off to `customizing-skills` to wire several units under a thin overlay | The need spans 2+ unit skills that should act as one workflow |
| **Customize** | Hand off to `customizing-skills` | Good single base, wrong defaults |
| **Refine / keep looking** | Back to Step 2/3 | Not quite right |

For **Adopt**: install via the marketplace, or for a single skill copy it into
`~/.claude/skills/`. **Confirm the source before installing anything** —
installing runs third-party content. See `references/pool-and-search.md`. After
adopting, a quick trigger check is worthwhile: fire 1–2 realistic sentences and
confirm it activates (the `customizing-skills` skill's `verify` reference has
deeper options if wanted).

For **Compose / Customize**: hand the chosen candidate(s) to the
**`customizing-skills`** skill. It leads with **composing units under a thin
overlay** (units stay as-is, upstream keeps flowing), then preference overlay,
synthesize, and — only as a last resort — fork & edit. Pass along what you
learned: the unit skills picked and what each covers, why they're close, and any
stack/preference cues the user already gave.

## Quick Reference

```
intent ─▶ decompose into capabilities ─▶ (one search per capability)
        BYO candidates ──┐
        local first ─────┼─▶ [shortlist(s)] ──▶ AskUserQuestion (narrow)
   ▲    live CLI / web ──┘        │                   │
   └── widen ◀────────────────────┘          chosen skill / unit set
                                                       │
                  ┌── adopt as-is ─── install / copy to ~/.claude/skills
   action ────────┼── compose ─────── → customizing-skills (overlay glue)
                  ├── customize ───── → customizing-skills
                  └── refine ──────── back to candidates
```

## Example

For a full run that continues from search all the way into the customization
flow — sourcing `grill-me` (community, via web search) and
`test-driven-development` (marketplace), then handing off to build a
"clarify the spec (architecture + principles), then build TDD" skillset — plus a
one-step adopt-as-is case, see `EXAMPLES.md` at the plugin root.

## Common Mistakes

- **Auto-picking the top result.** Defeats the purpose. Always present choices;
  the user's taste is the deciding input, not your ranking.
- **Forcing one skill to do everything.** If the need splits into capabilities,
  look for unit skills to compose rather than a single do-everything skill —
  composing keeps the skillset lighter and preserves each unit's upstream.
- **Skipping local.** A unit the user already has on disk is the cheapest,
  lightest match and composes for free — search on-disk before going to the web.
- **Ignoring token cost.** A skill's `description` is always in context. A bloaty
  always-on cost is a real downside — surface it.
- **Installing without confirming provenance.** Marketplace and especially web
  skills are third-party code. Show the source/homepage and get a yes first.
- **Over-asking.** If intent is already specific, don't interrogate — search.
- **Treating web results as trusted.** Flag them as unverified; skim before
  recommending.
- **Doing the tuning here.** Customization lives in `customizing-skills` —
  hand off rather than reinventing it.

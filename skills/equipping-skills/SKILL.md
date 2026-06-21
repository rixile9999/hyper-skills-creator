---
name: equipping-skills
description: Use this DURING an ordinary planning or implementation task — NOT when the user asked about skills — at the moment you notice the work would go meaningfully better with a specialized skill you don't currently have. Triggers on your own mid-task realization: you're about to hand-roll a workflow that a dedicated skill exists for, you're repeating a specialized procedure (framework migration, a test strategy, a release flow, a domain like a11y/security/perf audits), or planning surfaces a capability gap. Propose equipping a skill, confirm with the user, then hand off to finding-skills — and resume the original task afterward.
---

# Equipping Skills

## Overview

The other skills in this plugin wait for the user to ask about skills. This one
is different: it fires **from your own realization in the middle of real work**.
You're planning or implementing some task the user actually came for, and you
notice — *this would go better with a specialized skill I don't have.* That gap
is the trigger. The user never said "find me a skill"; you inferred the need.

This is the **equip** path: detect the gap → propose lightly → on a yes, hand
off to `finding-skills` to search/adopt (and `customizing-skills` to tune) →
**then come back and finish the original task** with the new skill in hand.

**Core principle: the user's task is the job; the skill is a means.** Never
derail the work to go skill-shopping. Surface the gap in one line, let the user
decide, and if they decline, just continue. The default is always "keep going."

**The loop:** `Notice a gap → Propose (one line) → On yes: hand off to
finding-skills → Resume the original task`.

## When to Use

Fire this when **all** of these hold:

- You're mid-task on something the user asked for (a feature, a refactor, a plan,
  a debugging session) — *not* responding to a "help me with skills" request.
- The task is a **specialized or recurring** procedure where a purpose-built
  skill would plausibly raise quality or speed — e.g. a framework migration, a
  particular test strategy (TDD, snapshot, property-based), a release/changelog
  flow, or a domain audit (accessibility, security, performance, i18n).
- **No installed skill already covers it** (check before proposing — see Step 1).

**Do NOT fire when:**

- The user is explicitly asking about skills already → that's `finding-skills`
  (discovery) or `customizing-skills` (tuning) or the `hyper-skills-creator`
  router. Don't add a hop.
- The task is a one-off or trivial enough that hand-rolling it now is clearly
  faster than finding, vetting, and adopting a skill. Equipping has a cost;
  only pay it when the gap is real and likely to recur.
- A capable installed skill already exists — just use it.

When in doubt, lean toward **not interrupting**. A wrong proposal is a tax on the
user's attention; missing one just means you do the task the normal way.

## Step 1 — Confirm the gap is real

Before you say anything, do a fast, silent check so you don't propose a skill the
user already has:

```bash
# What's already installed/forked that might cover this?
python3 ../finding-skills/scripts/search_catalog.py "<task keywords>" --limit 8
ls ~/.claude/skills/ 2>/dev/null
```

If something on-topic is already `[installed]`/`[forked]`, there's no gap — use
it and move on, no proposal needed. Only continue if the gap stands.

## Step 2 — Propose in one line, don't derail

Surface the gap as a **single, skippable line** inside your normal task flow —
not a wall of options, not a context switch. Make the cost/benefit legible and
default to continuing:

> "This is a Rails→Next migration — there are dedicated migration skills that
> codify the gotchas. Want me to pull one in before we go further, or just
> proceed as-is?"

Use `AskUserQuestion` with two or three options when it helps:

- **Pull in a skill** (→ Step 3) — recommended only when the gap is strong.
- **Proceed without** — do the task the normal way; optionally note the gap.
- **Not now, remind me later** — record it and keep going.

Keep it proportional: the bigger the task and the stronger the gap, the more a
proposal is warranted. For a small gap, a one-line aside ("there's a skill for
this if you want it later") is enough — don't open a menu.

## Step 3 — Hand off, then resume

On a yes, hand the gap to **`finding-skills`** as if the user had asked for that
skill — but carry the context so they don't re-explain:

- the **task** you're in the middle of and what capability it needs,
- the **stack/tools** already visible in the repo and conversation,
- whether this is a one-shot need or a recurring one (affects adopt vs customize).

`finding-skills` runs its own loop (search → narrow → adopt), and hands off to
`customizing-skills` if the base needs tuning. When it lands on an adopted skill:

1. **Note that newly adopted skills load at session start.** If the user adopts a
   skill mid-session, it may not be active until they restart `claude`. Say so,
   and offer to apply its *approach* manually for the current task in the
   meantime.
2. **Return to the original task.** This is the part that's easy to forget:
   equipping was a detour, not the destination. Pick the task back up — now
   informed by (or using) the skill — and finish what the user actually came for.

## Quick Reference

```
mid-task realization: "a specialized skill would help here"
        │
   Step 1: check installed/catalog ── already covered? ─▶ use it, no proposal
        │ gap is real
   Step 2: one-line proposal (AskUserQuestion)
        ├── proceed without ──────────▶ continue the task normally
        ├── not now ──────────────────▶ note the gap, continue
        └── pull in a skill
                 │
   Step 3: hand off to finding-skills (carry task + stack context)
                 │  → customizing-skills if tuning needed
                 ▼
          adopt ─▶ (note: loads next session) ─▶ RESUME original task
```

## Common Mistakes

- **Derailing the task.** The user came for the feature, not a skill hunt. Propose
  in one line and default to continuing. Never silently switch into shopping mode.
- **Over-proposing.** Firing on trivial or one-off work is noise. Only when the
  gap is specialized/recurring *and* uncovered does equipping earn its cost.
- **Skipping the installed check.** Proposing a skill the user already has reads
  as not paying attention. Always do Step 1 first.
- **Forgetting to come back.** After adoption, resume the original task —
  equipping is a means, not the end. Leaving the user in the skill flow with their
  actual work unfinished is the worst outcome.
- **Reinventing search/tuning here.** This skill only detects the gap and hands
  off. Discovery lives in `finding-skills`, tuning in `customizing-skills`.
- **Ignoring the session-reload gap.** A skill adopted mid-session usually isn't
  live until restart — say so and offer to apply its approach by hand for now.

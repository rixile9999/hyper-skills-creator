---
name: personalizing-skills
description: Use when the user has an existing Claude coding-agent skill or plugin and wants to adapt, tune, customize, personalize, or tailor it to their own stack, conventions, taste, or workflow — phrases like "tune this skill to how I work", "customize this skill for my React+Postgres setup", "make this skill match my style", "fork and edit this skill", or "combine the good parts of these skills into one". Receives hand-offs from finding-skills once a base skill is chosen.
---

# Personalizing Skills

## Overview

A chosen skill is rarely a perfect fit out of the box — its defaults assume some
stack, some conventions, some level of rigor. This skill adapts an existing skill
to the user, and verifies the result. It's the personalization half of
`hyper-skills-creator`; it usually receives a hand-off from `finding-skills`, but
also triggers directly when the user already has a skill in mind to tune.

**Core principle:** the *mode* of personalization is situational, so let the user
pick — don't assume. The same goes for how rigorously to verify. Present real
choices and recommend a default based on what you see.

**The loop:** `Capture preferences → Choose a mode (fork / overlay / synthesize)
→ Apply → Choose a verify level → Verify`.

## When to Use

- "Take <skill> and tune it to how I like to work."
- "Customize this skill for my stack / conventions / style."
- "Combine the best parts of these skills into one for me."
- A hand-off from `finding-skills` after the user chose a base skill to adapt.

**Not for:** discovering which skill to start from (use `finding-skills`).

## Step 1 — Capture preferences

Gather the inputs once and reuse them across modes. Ask only what's not already
obvious from the conversation, the hand-off, or the user's repo:

- **Stack / languages / frameworks** (e.g. TS + React, Python + FastAPI)
- **Conventions** (test framework, lint/format, commit style, dir layout)
- **Working style** (TDD-strict vs pragmatic, how much explanation they want,
  how aggressively to use subagents, verification rigor)
- **Constraints** (token budget, offline, monorepo, CI specifics)

Save durable, cross-project preferences to memory so future runs start from them.

## Step 2 — Choose a personalization mode

Present these three as a choice (`AskUserQuestion`) — situational, so the user
picks. Recommend a default from what you saw: good base / wrong defaults →
overlay; want deep changes → fork; pieces from several skills → synthesize.

| Mode | What it produces | Trade-off |
|------|------------------|-----------|
| **Fork & edit** | A copy in `~/.claude/skills/<name>/` you edit freely | Full control; you own maintenance, lose upstream updates |
| **Preference overlay** | A thin companion skill or project `CLAUDE.md` notes layered on top | Non-destructive; survives upstream updates |
| **Synthesize new** | One user-specific skill cherry-picked from several | Heaviest; a new skill to maintain |

**Full instructions for each mode:** read `references/personalize.md`.

Key safety rule for all modes: **never edit a skill in its install path** —
plugin paths may be read-only and get overwritten on update. Personalize by
copying into `~/.claude/skills/`.

## Step 3 — Verify

After applying, ask whether and how to verify. **Present as a choice** — a tiny
overlay barely needs testing; a synthesized skill for daily use deserves a real
eval:

1. **Lightweight check (default)** — fire 1–3 realistic trigger sentences and
   confirm the skill activates and behaves. Quick, no overhead.
2. **Formal skill-creator eval** — with/without comparison, benchmark, and
   description-trigger optimization. Rigorous; route through `skill-creator`.
3. **None** — user verifies on their own; hand off cleanly (where it lives, what
   triggers it, how to tweak the `description`).

**Details and trigger-phrase tips:** read `references/verify.md`.

## Quick Reference

```
preferences ──▶ mode choice ──┬── fork & edit ──── copy to ~/.claude/skills + edit
                              ├── overlay ──────── companion skill / CLAUDE.md
                              └── synthesize ───── → skill-creator / writing-skills
                                       │
                          verify choice ── light │ formal eval │ none
```

## Example

For a worked overlay example — wiring `grill-me` + `test-driven-development` into
a personalized `grill-then-tdd` skillset tuned to a TypeScript/vitest user — see
`EXAMPLES.md` at the plugin root.

## Common Mistakes

- **Assuming the mode.** The user picks fork vs overlay vs synthesize — it's a
  real trade-off, not a default you choose silently.
- **Editing an installed skill in place.** Read-only / overwritten on update.
  Copy to `~/.claude/skills/` first.
- **Over-fitting to one example.** Bake in the user's *general* preferences, not
  a single task's specifics, or the personalized skill won't generalize.
- **Skipping the why.** When editing a skill body, explain *why* a convention
  matters rather than adding rigid MUSTs — it generalizes better.
- **Forgetting trigger collisions.** If both original and fork may be active,
  give the fork a distinct `name` so they don't both fire.

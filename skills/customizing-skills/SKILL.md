---
name: customizing-skills
description: Use when the user has an existing Claude coding-agent skill or plugin and wants to adapt, tune, customize, personalize, or tailor it to their own stack, conventions, taste, or workflow — phrases like "tune this skill to how I work", "customize this skill for my React+Postgres setup", "make this skill match my style", "fork and edit this skill", "wire these unit skills into one workflow", or "combine the good parts of these skills into one". Leads with composing unit skills under a thin overlay (upstream-safe) before forking. Receives hand-offs from finding-skills once a base skill — or a set of unit skills — is chosen.
---

# Customizing Skills

## Overview

A chosen skill is rarely a perfect fit out of the box — and a whole capability is
rarely one skill at all. This skill adapts existing skills to the user: most
often by **composing several unit skills under a thin overlay** you own, and
sometimes by tuning a single base. Then it verifies the result. It's the
customization half of `hyper-skills-creator`; it usually receives a hand-off from
`finding-skills` (often with a *set* of unit skills, not just one), but also
triggers directly when the user already has skill(s) in mind to tune.

**Core principle:** keep the upstream link alive. Prefer non-destructive moves —
**compose units with an overlay**, or layer preferences on top — so each skill
keeps receiving its upstream updates and your skillset stays light. Forking a
skill's body is the *last resort*: it severs upstream and you own it forever.
Beyond that, the *mode* is situational — present real choices and recommend a
default based on what you see.

**The loop:** `Capture preferences → Choose a mode (compose / overlay /
synthesize / fork) → Apply → Choose a verify level → Verify`.

## When to Use

- "Take <skill> and tune it to how I like to work."
- "Customize this skill for my stack / conventions / style."
- "Wire these unit skills together into one <feature> workflow."
- "Combine the best parts of these skills into one for me."
- A hand-off from `finding-skills` after the user chose a base skill — or a set
  of unit skills — to adapt.

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

## Step 2 — Choose a customization mode

Present these as a choice (`AskUserQuestion`) — situational, so the user picks.
They're ordered by how well they preserve upstream updates; recommend the
highest one that fits. Default from what you saw: a need spanning several unit
skills → **compose**; one good base with wrong defaults → overlay; a capability
no existing skill covers → synthesize; deep changes to a skill's body → fork.

| Mode | What it produces | Trade-off |
|------|------------------|-----------|
| **Compose (overlay glue)** | A thin orchestration overlay in `~/.claude/skills/<feature>/` that sequences several unit skills, each kept as-is | Lightest; **every unit keeps its upstream** — you maintain only the glue |
| **Preference overlay** | A thin companion skill or project `CLAUDE.md` notes layered on one base | Non-destructive; survives upstream updates |
| **Synthesize new** | One user-specific skill cherry-picked from several | Heavier; a new skill to maintain — use when no unit covers a capability |
| **Fork & edit** | A copy in `~/.claude/skills/<name>/` you edit freely | **Last resort:** full control but severs upstream; you own maintenance forever |

**Full instructions for each mode:** read `references/customize.md`.

Key safety rule for all modes: **never edit a skill in its install path** —
plugin paths may be read-only and get overwritten on update. Customize by
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
preferences ──▶ mode choice ──┬── compose ─────── overlay glue over unit skills (upstream-safe)
                              ├── overlay ──────── companion skill / CLAUDE.md (upstream-safe)
                              ├── synthesize ───── → skill-creator / writing-skills
                              └── fork & edit ──── copy + edit (last resort, severs upstream)
                                       │
                          verify choice ── light │ formal eval │ none
```

## Example

For a worked overlay example — receiving the `grill-me` + `test-driven-development`
hand-off from `finding-skills` and wiring them into a customized `spec-then-tdd`
skillset (clarify spec + architecture → write it down → TDD) tuned to a
TypeScript/vitest user — see `EXAMPLES.md` at the plugin root.

## Common Mistakes

- **Assuming the mode.** The user picks compose vs overlay vs synthesize vs fork
  — it's a real trade-off, not a default you choose silently.
- **Forking when you could compose.** Forking a monolith severs upstream and
  makes the skillset heavier. If the need is several capabilities, compose unit
  skills under a thin overlay first; reserve fork for deep edits to one skill's
  body that an overlay genuinely can't express.
- **Editing an installed skill in place.** Read-only / overwritten on update.
  Copy to `~/.claude/skills/` first.
- **Over-fitting to one example.** Bake in the user's *general* preferences, not
  a single task's specifics, or the customized skill won't generalize.
- **Skipping the why.** When editing a skill body, explain *why* a convention
  matters rather than adding rigid MUSTs — it generalizes better.
- **Forgetting trigger collisions.** If both original and fork may be active,
  give the fork a distinct `name` so they don't both fire.

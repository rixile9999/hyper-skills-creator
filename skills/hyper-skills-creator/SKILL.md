---
name: hyper-skills-creator
description: Use as the entry point when the user wants help with Claude coding-agent skills end-to-end but hasn't said whether they're discovering or tuning — broad umbrella phrases like "help me sort out my skills", "I want a skill that fits how I work", "set me up with the right skill for X", "find a skill and make it mine", "do the whole skill-matchmaking thing", or any time the request spans both finding and customizing. Routes to and composes the two sub-skills — finding-skills (search → narrow → adopt) and customizing-skills (tune → verify). Defer to those two directly when the user's ask is already clearly one or the other.
---

# Hyper Skills Creator

## Overview

There's no single "best" coding-agent skill — the right one depends on the
user's taste, level, and workflow. This is the **front door** of
`hyper-skills-creator`: it takes a broad, undifferentiated request and runs the
matchmaking journey end-to-end by composing two sub-skills:

- **`finding-skills`** — search the pool → narrow interactively → adopt.
- **`customizing-skills`** — tune a chosen skill → verify.

This skill owns no discovery or tuning logic of its own. Its whole job is to
**figure out where the user is in the journey and hand off to the right
sub-skill** — then, when the journey continues, hand off again. The sub-skills
already hand off to each other; this skill exists so a vague "help me with
skills" lands somewhere sensible instead of falling between them.

> **A third, self-triggered path:** `bootstrapping-skills` is *not* routed from
> here — it fires on its own when, mid-task on something else, you realize a
> specialized skill would help. It then feeds into the same `finding-skills` →
> `customizing-skills` pipeline. This router is for *user-initiated* skill
> requests; the bootstrap path is for *agent-initiated* ones.

> **"creator" vs `skill-creator`:** this plugin *creates your customized
> skillset out of existing skills* (find → adopt → fork/overlay/synthesize),
> whereas `skill-creator` authors a single new skill from a blank page. Reach for
> `skill-creator` when there's nothing to start from.

**The full pipeline:**

```
intent ─▶ finding-skills ─(chosen base, wants tuning)─▶ customizing-skills ─▶ done
            │ adopt as-is                                      │
            └────────────────── done                          verify ─▶ done
```

## When to Use

- "Help me sort out my skills." / "Set me up with the right skill for <X>."
- "Find a skill for my stack **and** tune it to how I work." (spans both halves)
- "I want the full skill-matchmaking thing."
- Any request that's clearly about skills but doesn't say *discover* vs *tune*.

**Defer directly to a sub-skill — skip this router — when the ask is already
unambiguous:**

- Pure discovery ("is there a skill for X?", "what should I use?") → go straight
  to **`finding-skills`**.
- Pure tuning ("customize *this* skill to my React+Postgres setup") → go straight
  to **`customizing-skills`**.
- Authoring a brand-new skill from a blank page → that's `skill-creator` /
  `superpowers:writing-skills`, not this plugin.

## Step 1 — Route

Read the request and place it on the journey. Don't interrogate — one read is
usually enough; ask at most one clarifying question, and only if you genuinely
can't tell which branch fits.

| The user… | Hand off to | 
|-----------|-------------|
| doesn't yet have a skill in mind | **`finding-skills`** (start of pipeline) |
| already has a skill, wants it adapted | **`customizing-skills`** |
| wants both ("find one *and* make it mine") | **`finding-skills`** first, then chain |

If it's genuinely ambiguous between the two, ask **one** branching question
(`AskUserQuestion`): *"Are we hunting for a skill, or tuning one you already
have?"* — then route.

## Step 2 — Compose the journey

Hand off to the sub-skill and let it run its own loop fully. Then continue the
pipeline based on where it lands:

1. **Discovery** — invoke `finding-skills`. It clarifies intent, searches the
   pool, narrows interactively, and ends on a chosen candidate with an action
   (adopt / customize / keep looking).
2. **The chain point** — when `finding-skills` lands on *customize* (good base,
   wrong defaults), the journey continues into `customizing-skills`. Carry the
   context forward: the chosen candidate, *why* it's close, and any stack or
   preference cues already surfaced — don't make the user repeat themselves.
3. **Tuning** — `customizing-skills` captures preferences, picks a mode
   (fork / overlay / synthesize), applies it, and verifies.

Loop back any time: a dead end in tuning can send the user back to discovery
with widened terms. The branching is the product — never silently auto-pick.

## Quick Reference

```
"help me with skills" (vague)
        │
   route (Step 1)
        ├── discover ──▶ finding-skills ──┬── adopt as-is ──────▶ done
        │                                 └── customize ─┐
        ├── tune existing ────────────────────────────────┤
        │                                                  ▼
        └── both ──▶ finding-skills ──▶ customizing-skills ──▶ verify ──▶ done
```

## Common Mistakes

- **Doing the work here.** This skill routes and composes — it holds no search or
  tuning logic. Hand off; don't reimplement either sub-skill.
- **Routing when you don't need to.** If the ask is plainly discovery-only or
  tuning-only, go straight to that sub-skill instead of adding a hop.
- **Dropping context at the chain point.** When `finding-skills` → `customizing-skills`,
  pass the chosen candidate and the cues already gathered, or the user re-explains.
- **Over-asking at the fork.** At most one branching question to decide the
  route; the real narrowing happens inside the sub-skills.
- **Auto-picking a path.** Whether to adopt-as-is, customize, or keep looking
  is the user's call — surface it, don't decide it for them.

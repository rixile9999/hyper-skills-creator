# Verification modes

After adopt/personalize (Step 5), offer these three as a choice. The right level
is situational — a tiny overlay barely needs testing; a synthesized skill the
user will lean on daily deserves a real eval.

## Mode 1 — Lightweight check (default)

Confirm two things: it **triggers** on the right intent, and it **behaves** once
triggered.

- Write 1–3 realistic trigger sentences — the kind the user would actually type,
  concrete and specific (file paths, real tool names, casual phrasing), not
  abstract ("do the thing"). Triggering depends on the `description`, so test
  phrasings that *should* fire and one near-miss that *shouldn't*.
- Run them (in this session or a quick subagent) and check the skill activates
  and produces sane output. If it under-triggers, the `description` needs more
  concrete triggers/symptoms; if it over-triggers, tighten it.
- Report what you tried and the result. Done in a couple of minutes.

## Mode 2 — Formal skill-creator eval

For skills that matter enough to benchmark. Route through `skill-creator`, which
provides the full machinery:

- **Output quality:** spawn with-skill vs baseline runs over a small eval set,
  grade against assertions, and view the comparison (`generate_review.py`).
- **Triggering accuracy:** the description-optimization loop (`run_loop.py`)
  evaluates ~20 should/shouldn't-trigger queries and proposes a better
  `description`, selected on a held-out split to avoid overfitting.

Use when the user explicitly wants rigor, or when a personalized/synthesized
skill is going into heavy daily use. It's slower and needs subagents.

## Mode 3 — None

The user verifies on their own. Just hand off cleanly: tell them where the skill
lives (`~/.claude/skills/<name>/`), what phrases trigger it, and how to tweak the
`description` if triggering feels off.

---

**Triggering reminder:** skills only fire for tasks the agent can't trivially do
itself. A one-step request ("read this file") may not trigger a skill even with a
perfect description — so make verification prompts substantive enough that
consulting a skill is actually worthwhile.

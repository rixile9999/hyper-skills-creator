---
description: Mid-task, equip a specialized skill for what you're working on — check what's installed, propose a fit, then find/adopt and resume.
argument-hint: [task or capability you need a skill for]
---

You are being invoked explicitly to **equip a skill** for the work currently
in progress. Follow the `equipping-skills` skill, but skip the "should I
propose?" hesitation — the user asked for this directly.

Context for what they need a skill for: $ARGUMENTS

(If `$ARGUMENTS` is empty, infer the need from the current task and conversation;
if it's genuinely unclear, ask one short question about what capability they want.)

Steps:

1. **Check what's already there** (don't recommend something they have):
   - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/finding-skills/scripts/search_catalog.py "<task keywords>" --limit 8`
   - `ls ~/.claude/skills/ 2>/dev/null`
   If an installed/forked skill already covers it, say so and use it — don't go
   searching.

2. **Hand off to `finding-skills`** with the task context carried forward (what
   you're building, the visible stack/tools, one-shot vs recurring need). Let it
   run search → narrow → adopt, chaining into `customizing-skills` if the base
   needs tuning.

3. **Resume the original task.** Note that a skill adopted mid-session may not be
   active until `claude` restarts — offer to apply its approach by hand for the
   current task meantime — then finish what the user was actually doing.

# Customization modes

This is the detail behind Step 2 of the `customizing-skills` skill. Present the
modes as a choice (`AskUserQuestion`) — the right one is situational. They're
ordered below by how well they preserve upstream updates; recommend the highest
one that fits the need: a need spanning several unit skills → compose; one good
base with wrong defaults → overlay; a capability nothing covers → synthesize;
deep edits to a skill's body → fork (last resort).

Preferences are captured once in Step 1 of the skill (stack, conventions,
working style, constraints) — reuse them here; don't re-ask.

---

## Mode 1 — Compose (overlay glue)

The default when a capability spans several unit skills. You write a thin
**orchestration overlay** that wires the units together; the units stay
installed and as-is, so each keeps receiving its upstream updates and you
maintain only the glue. This is the lightest, most upstream-friendly path —
small composable units, joined by a layer you own.

1. Confirm the unit skills are available (installed, or copied into
   `~/.claude/skills/` if sourced from web/git). **Don't edit them.**
2. Create a small overlay skill at `~/.claude/skills/<feature>/SKILL.md`. Its
   body does **not** reimplement the units — it *sequences* them and adds the
   user's conventions as glue:
   > "To do <feature>: first use `<unit-A>` to <X>, then `<unit-B>` for <Y>,
   > then `<unit-C>` to verify <Z>. Conventions: <the user's stack/style>."
3. Give it a `name`/`description` that triggers on the *feature* intent (the
   whole workflow), so the overlay is the entry point and the units fire as it
   directs — rather than competing with them.
4. Keep it lean: wiring + preferences only. The moment the overlay starts
   restating what a unit already does, you're drifting toward a fork — stop and
   point at the unit instead.

When any unit ships an upstream update you get it for free, and the overlay
rarely needs to change.

## Mode 2 — Preference overlay (non-destructive)

For a single base skill that's fundamentally fine but has the wrong defaults.
The original stays installed and keeps updating; preferences layer on top.

Pick the lighter sub-form that fits:

- **Companion skill** — a small skill in `~/.claude/skills/<base>-prefs/` whose
  body is just the user's preferences and a pointer: "When using `<base>`, apply
  these conventions: …". Triggers on the same domain and rides alongside.
- **Project notes** — for repo-specific tuning, write the preferences into the
  project's `CLAUDE.md` instead. Best when the customization is about *this
  codebase*, not the user globally.

This survives upstream changes and is trivial to delete. Prefer it when the base
skill is fundamentally fine and only its defaults are off. (Mode 1 is the same
mechanism aimed at *several* skills at once; this one tunes a single base.)

## Mode 3 — Synthesize a new skill

Cherry-pick the strongest parts of several candidates into one user-specific
skill. Reach for this when a capability has **no existing unit skill to
compose** — you're filling a genuine gap, not gluing what already exists. This
is real authoring — hand off to the authoring skills rather than improvising:

- Use `skill-creator` (eval-driven draft → test → iterate) or
  `superpowers:writing-skills` (TDD-for-skills: baseline → write → close
  loopholes). Both are typically already installed.
- Bring them the inputs you've gathered: the candidate skills to draw from,
  which parts of each the user liked, and the captured preferences.
- The output lands in `~/.claude/skills/<new-name>/` and then flows into Step 3
  verification.

Be explicit with the user that this is heavier than composing and produces a
skill they'll maintain.

## Mode 4 — Fork & edit (last resort)

The last resort. Full control, but it **severs upstream** — the user now owns
maintenance forever and the skillset gets heavier. Reach for it only when you
need deep changes to a *single* skill's body that an overlay can't express (Mode
1/2 should be ruled out first).

1. Locate the source SKILL.md (install path or web/git source).
2. Copy the whole skill dir into the personal skills directory — **never edit the
   install path** (read-only, overwritten on update):
   ```bash
   cp -r <source>/<skill-name> ~/.claude/skills/<skill-name>
   ```
3. Edit `~/.claude/skills/<skill-name>/SKILL.md` and bundled files to the user's
   preferences: bake in their stack, swap generic examples for their conventions,
   tune verification rigor, trim sections they'll never use to save context.
4. Keep the `name` unique if both original and fork might be active at once
   (e.g. `<name>-mine`) to avoid trigger collisions; otherwise preserving the
   name shadows the original cleanly.
5. Update the `description` so it still triggers on the same intents.

# Personalization modes

This is the detail behind Step 2 of the `personalizing-skills` skill. Present
the three modes as a choice (`AskUserQuestion`) — the right one is situational.
Below is how to execute each. Recommend a default based on what you saw: good
base / wrong defaults → overlay; want deep changes → fork; pieces from several →
synthesize.

Preferences are captured once in Step 1 of the skill (stack, conventions,
working style, constraints) — reuse them here; don't re-ask.

---

## Mode 1 — Fork & edit

Full control; the user now owns maintenance and loses upstream updates.

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

## Mode 2 — Preference overlay (non-destructive)

Original stays installed and keeps updating; preferences layer on top.

Pick the lighter sub-form that fits:

- **Companion skill** — a small skill in `~/.claude/skills/<base>-prefs/` whose
  body is just the user's preferences and a pointer: "When using `<base>`, apply
  these conventions: …". Triggers on the same domain and rides alongside.
- **Project notes** — for repo-specific tuning, write the preferences into the
  project's `CLAUDE.md` instead. Best when the customization is about *this
  codebase*, not the user globally.

This survives upstream changes and is trivial to delete. Prefer it when the base
skill is fundamentally fine and only its defaults are off.

## Mode 3 — Synthesize a new skill

Cherry-pick the strongest parts of several candidates into one user-specific
skill. This is real authoring — hand off to the authoring skills rather than
improvising:

- Use `skill-creator` (eval-driven draft → test → iterate) or
  `superpowers:writing-skills` (TDD-for-skills: baseline → write → close
  loopholes). Both are typically already installed.
- Bring them the inputs you've gathered: the candidate skills to draw from,
  which parts of each the user liked, and the captured preferences.
- The output lands in `~/.claude/skills/<new-name>/` and then flows into Step 5
  verification.

Be explicit with the user that this is the heaviest path and produces a skill
they'll maintain.

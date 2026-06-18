# hyper-skills-creator

An interactive **skill matchmaker** for coding agents, shipped as a plugin: one
entry skill that routes broad requests and composes two sub-skills.

There's no single "best" skill — the effective set depends on your taste, level,
and workflow. So instead of guessing, this plugin lets you describe what you
want, searches the available pool, narrows it down *with you* through choices,
and then adopts a skill as-is or personalizes it to fit.

## Why this exists

Coding agents move fast. Models, tools, and the harness around them change on a
scale of weeks — and every change shifts what a good skill actually looks like.
A skillset (harness) that was a perfect fit a few months ago can quietly stop
fitting the present: it assumes a tool that's been replaced, leans on a workaround
the model no longer needs, or misses a capability that just landed.

That means a skillset isn't something you set up once and forget. To keep it
effective you have to keep **updating and personalizing** it — pruning what's
gone stale, pulling in what's new, and re-tuning the rest to your current stack
and taste. This plugin is built for exactly that loop: not a one-time setup, but
a recurring "is my skillset still the right fit?" pass you can run whenever the
ground shifts under you.

## One entry skill + two sub-skills

| Skill | Does | Triggers on |
|-------|------|-------------|
| **hyper-skills-creator** | the front door — route a vague request, then compose the two below end-to-end | "help me sort out my skills", "find a skill **and** make it mine", anything spanning both halves |
| **finding-skills** | search the pool → narrow interactively → adopt/install | "is there a skill for X", "what should I use", "recommend a skill" |
| **personalizing-skills** | tune a chosen skill → verify | "tune this skill to how I work", "customize for my stack" |

They compose: the `hyper-skills-creator` entry skill takes an undifferentiated
"help me with skills" request and routes it. `finding-skills` discovers and
adopts; when the user wants tuning instead, it hands off to `personalizing-skills`.
Each sub-skill also triggers on its own, so an unambiguous ask skips the router
and lands directly.

```
hyper-skills-creator:  route ─┬─ discover ─▶ finding-skills
                              ├─ tune ─────▶ personalizing-skills
                              └─ both ─────▶ finding-skills ─▶ personalizing-skills

finding-skills:  clarify intent → search pool → narrow interactively
                   → adopt-as-is │ refine │ ──hand off──▶ personalizing-skills

personalizing-skills:  capture prefs → mode (fork│overlay│synthesize)
                        → apply → verify (light│formal eval│none)
```

- **Pool** = the Claude marketplace (local catalog cache + live `claude plugin`
  CLI) + web search for community skills.
- **Personalize** = your choice of fork-&-edit · preference overlay · synthesize.
- **Verify** = your choice of lightweight check · formal skill-creator eval · none.

Every fork is a choice you make — the branching is the point.

## Use cases

See [`EXAMPLES.md`](./EXAMPLES.md) for worked runs that go from search straight
through the personalization flow — including a **"clarify the spec (architecture +
principles), then build TDD"** skillset: `finding-skills` sources `grill-me`
(community) + `test-driven-development` (marketplace), then hands off to
`personalizing-skills` to wire them into a `spec-then-tdd` overlay tuned to a
TypeScript/vitest user.

## Layout

```
hyper-skills-creator/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── hyper-skills-creator/
│   │   └── SKILL.md                       # entry skill: route + compose the two below
│   ├── finding-skills/
│   │   ├── SKILL.md
│   │   ├── scripts/search_catalog.py      # fast offline catalog ranking
│   │   └── references/pool-and-search.md
│   └── personalizing-skills/
│       ├── SKILL.md
│       └── references/
│           ├── personalize.md             # the three personalization modes
│           └── verify.md                  # the three verification modes
└── README.md
```

## Install

**As a plugin from this marketplace** (recommended) — this repo *is* a
marketplace, so point Claude at it and install:

```bash
claude plugin marketplace add rixile9999/hyper-skills-creator
claude plugin install hyper-skills-creator
```

See "Publishing to a marketplace" below for how this is wired up.

**For local use / development** — symlink the three skills into your personal
skills dir:

```bash
ln -sfn "$PWD/skills/hyper-skills-creator" ~/.claude/skills/hyper-skills-creator
ln -sfn "$PWD/skills/finding-skills"       ~/.claude/skills/finding-skills
ln -sfn "$PWD/skills/personalizing-skills" ~/.claude/skills/personalizing-skills
```

Skills load at session start, so start a new `claude` session to pick them up.
Then just ask: *"Help me sort out my skills"*, *"Is there a skill for <X>?"*, or
*"find me a skill and tune it to how I work."*

## The search script

```bash
python3 skills/finding-skills/scripts/search_catalog.py "postgres query optimization"
python3 skills/finding-skills/scripts/search_catalog.py "react" --skills-only
python3 skills/finding-skills/scripts/search_catalog.py --category security --limit 20
python3 skills/finding-skills/scripts/search_catalog.py "<query>" --json
```

Ranks the on-disk marketplace catalog by relevance + popularity, marks what's
already installed/forked, and reports install counts and always-on token cost.
No network needed.

## Publishing to a marketplace

A plugin is the unit you publish. To make it installable via
`claude plugin install`, host it in a marketplace repo: a git repo with a
`.claude-plugin/marketplace.json` listing this plugin. You can run your own
marketplace (point Claude at your repo) or submit to an existing one. See the
Claude Code plugin/marketplace docs for the exact `marketplace.json` schema and
`claude plugin marketplace add <repo>` flow.

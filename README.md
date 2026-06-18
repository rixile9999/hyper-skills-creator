# hyper-skills-creator

An interactive **skill matchmaker** for coding agents, shipped as a plugin
composed of two sub-skills.

There's no single "best" skill — the effective set depends on your taste, level,
and workflow. So instead of guessing, this plugin lets you describe what you
want, searches the available pool, narrows it down *with you* through choices,
and then adopts a skill as-is or personalizes it to fit.

## Two sub-skills

| Skill | Does | Triggers on |
|-------|------|-------------|
| **finding-skills** | search the pool → narrow interactively → adopt/install | "is there a skill for X", "what should I use", "recommend a skill" |
| **personalizing-skills** | tune a chosen skill → verify | "tune this skill to how I work", "customize for my stack" |

They compose: `finding-skills` discovers and adopts; when the user wants tuning
instead, it hands off to `personalizing-skills`. Each also triggers on its own.

```
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

**As a local plugin** (recommended once you publish to a marketplace) — see
"Publishing to a marketplace" below.

**For local use / development** — symlink the two skills into your personal
skills dir:

```bash
ln -sfn "$PWD/skills/finding-skills"       ~/.claude/skills/finding-skills
ln -sfn "$PWD/skills/personalizing-skills" ~/.claude/skills/personalizing-skills
```

Skills load at session start, so start a new `claude` session to pick them up.
Then just ask: *"Is there a skill for <X>?"* or *"find me a skill and tune it to
how I work."*

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

# Candidate pool & search mechanics

The pool hyper-skills searches is **the Claude marketplace + web search**. This
file is the detailed how-to behind Step 2 and the "adopt" branch of Step 4.

## 1. Local catalog cache (default, offline)

Claude Code keeps a catalog cache on disk. The bundled script reads it directly:

```bash
python3 scripts/search_catalog.py "<query>"            # ranked plugins
python3 scripts/search_catalog.py "<query>" --json     # structured, for branching
python3 scripts/search_catalog.py "<query>" --skills-only
python3 scripts/search_catalog.py --category <cat> --limit 20
```

Paths it uses (override the first with `--catalog`):
- `~/.claude/plugins/plugin-catalog-cache.json` — the marketplace catalog
- `~/.claude/plugins/installed_plugins.json` — to mark `[installed]`
- `~/.claude/skills/*/SKILL.md`, `~/.agents/skills/*/SKILL.md` — to mark `[forked]`

Each catalog entry carries: `marketplace_entry` (name, description, category,
homepage, author), `components` (skills / commands / agents / hooks / mcpServers
/ lspServers, each with names), `unique_installs` (popularity), and `tokens`
(always-on vs on-invoke context cost per model). The script's scoring favors
relevance, then popularity, lightly penalizing heavy always-on cost. Adjust the
`WEIGHTS` block in the script if a user wants, say, popularity to dominate.

**Reading a candidate's real content.** Ranking is a filter, not a verdict.
Before recommending strongly, read the actual `SKILL.md` of installed/forked
candidates from their install path so you describe what it *does*, not just its
blurb:

```bash
find ~/.claude/plugins/cache -path "*<plugin>*/SKILL.md"
```

## 2. Live marketplace (freshness)

The cache has a `fetchedAt` timestamp (the script prints it). If it's old, thin,
or the user expects something newer, refresh and query live with the bundled CLI
rather than trusting stale JSON:

```bash
claude plugin marketplace --help     # discover the exact subcommands available
claude plugin marketplace list
claude plugin marketplace update     # refresh the cache, then re-run the script
```

Subcommand names vary by version — run `--help` first instead of guessing.

## 3. Web search (breadth / community)

When the marketplace genuinely has no fit, widen to the web with `WebSearch` /
`WebFetch`:

- Search GitHub topics (`claude-code-skill`, `claude-skill`, `agent-skill`),
  awesome-lists, and the agentskills.io specification ecosystem.
- **Provenance is mandatory.** Web skills are unverified third-party code. Show
  the user the repo URL and star count, skim the SKILL.md and any scripts for
  anything surprising (per the "principle of lack of surprise"), and say plainly
  that it's community-sourced before recommending or installing.

## Adopting (installing) a chosen candidate

Confirm the source with the user first — installing runs third-party content.

- **Whole plugin from the marketplace:**
  ```bash
  claude plugin install <name>@<marketplace>     # verify exact syntax with --help
  ```
- **A single skill (from web/git or one skill out of a plugin):** copy just that
  skill directory into the user's personal skills dir:
  ```bash
  mkdir -p ~/.claude/skills
  cp -r <source>/<skill-name> ~/.claude/skills/<skill-name>
  ```
  A skill is active when `~/.claude/skills/<name>/SKILL.md` exists with valid
  `name` + `description` frontmatter.

After installing, do a Step 5 verification pass if the user opted in.

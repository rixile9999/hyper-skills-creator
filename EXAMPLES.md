# Use cases & worked examples

Concrete end-to-end runs of `hyper-skills-creator`. Each shows the interactive
choices as they'd actually appear, so you can see how the branching feels.

---

## Example 1 — A personalized "grill the plan, then build test-first" skillset

**User:** *"I keep letting Claude jump straight into coding before the design is
nailed down, and then the tests come as an afterthought. I want a skillset that
forces me to think the design through first, then build it test-first — tuned to
my stack (TypeScript + vitest, I like concise commits)."*

This is a **skillset** request (two skills working as a sequence), so it runs
through both halves of the plugin: `finding-skills` to source the pieces, then
`personalizing-skills` to wire them into a personalized set.

### finding-skills

**Step 1 — Clarify intent.** Already specific (two needs: design interrogation +
test-first implementation; stack TS/vitest). No clarifying question needed —
search directly.

**Step 2 — Search the pool.** Two intents → two searches.

```bash
python3 skills/finding-skills/scripts/search_catalog.py "test driven development TDD" --limit 4
python3 skills/finding-skills/scripts/search_catalog.py "plan design interview before coding" --limit 6
```

- *TDD* → **`test-driven-development`** (in `superpowers`, 787k installs,
  marketplace). Strong, official, cheap. Found locally.
- *Design interrogation* → the catalog has no clean match (top hits were generic
  brainstorming). So widen to **web search** (per Step 2.3): this surfaces
  **`grill-me`** from `mattpocock/skills` (~100k stars) — "get relentlessly
  interviewed about a plan or design until every branch of the decision tree is
  resolved." Flag it: *community-sourced, unverified — skim the SKILL.md before
  adopting.*

**Step 3 — Narrow interactively.** Present the two pieces and confirm the pairing:

> **AskUserQuestion — "설계-우선 스킬은 이걸로 갈까요?"**
> - **grill-me (mattpocock) — (추천)**: 코딩 전 설계를 집요하게 인터뷰해 결정 트리를 다 해소. ~100k stars, 커뮤니티(미검증 — 소스 확인 후 채택). 당신 문제("바로 코딩 들어감")에 정확히 대응.
> - superpowers:brainstorming: 공식·검증됨, 하지만 더 일반적인 발산형 — "집요한 인터뷰"보다는 아이디어 확장에 가까움.
> - 둘 다 비교: 두 SKILL.md를 나란히 열어 비교.

> **AskUserQuestion — "구현 스킬은?"**
> - **superpowers:test-driven-development — (추천)**: RED-GREEN-REFACTOR. 787k installs, 공식. 이미 설치돼 있을 가능성 높음.

User picks **grill-me + test-driven-development**.

**Step 4 — Action.** Combining two skills into a tuned sequence = personalize.

> **AskUserQuestion — "이 둘을 어떻게 할까요?"**
> - **개인화 (추천)**: 두 스킬을 채택하고, 내 스택에 맞춰 "grill → TDD" 순서로 엮는 스킬셋 구성. → `personalizing-skills`로 인계.
> - 그대로 둘 다 설치: 순서 없이 각각.
> - 더 찾아보기.

Adopt the bases first (confirm sources — `grill-me` is community, so skim it):
```bash
# TDD: from the marketplace
claude plugin install superpowers@claude-plugins-official      # if not already installed
# grill-me: single community skill → copy just that skill in
git clone --depth 1 https://github.com/mattpocock/skills /tmp/mp-skills
cp -r /tmp/mp-skills/skills/productivity/grill-me ~/.claude/skills/grill-me
```
→ hand off to **personalizing-skills**.

### personalizing-skills

**Step 1 — Capture preferences.** From the request: TS, **vitest**, concise
commits. (Save as durable memory for future runs.)

**Step 2 — Choose a mode.**

> **AskUserQuestion — "스킬셋을 어떻게 구성할까요?"**
> - **Preference overlay — (추천)**: grill-me·TDD 원본은 그대로 두고(둘 다 활발히 유지됨), 둘을 순서대로 엮고 내 스택을 주입하는 얇은 컴패니언 스킬 `grill-then-tdd`를 새로 만듦. 비파괴적, 업스트림 업데이트 유지.
> - Fork & edit: TDD 스킬 본문을 복사해 vitest 예시를 깊게 박음 — 더 무겁고 업스트림을 잃음.
> - Synthesize new: 둘을 통째로 합친 단일 스킬 — 가장 무거움.

User picks **overlay**. Create the companion skill (the "skillset" glue):

```markdown
---
name: grill-then-tdd
description: Use when starting any non-trivial feature or design in this user's
  TypeScript projects — before writing implementation code. Sequences a design
  interrogation then a test-first build.
---

# Grill, then TDD (personalized workflow)

When the user starts a feature, run this sequence — don't skip to code:

1. **Grill the design first.** Use the `grill-me` skill: relentlessly interview
   the user about the plan until the decision tree is resolved. Do NOT write
   implementation code during this phase.
2. **Then build test-first.** Use `superpowers:test-driven-development`
   (RED-GREEN-REFACTOR), with this user's conventions baked in:
   - Tests in **vitest** (`describe/it`, `expect().toBe`, `vi.mock`). Write the
     failing test first; watch it fail before implementing.
   - Keep commits **concise** — imperative subject, ~50 chars, no filler body.

The point of pairing them: grill-me removes design ambiguity so the TDD tests
assert the *right* behavior, not a half-understood one.
```

**Step 3 — Verify.**

> **AskUserQuestion — "검증은?"**
> - **Lightweight (추천)**: 트리거 문장 발사 — (1) "TS로 결제 모듈 새로 짤 건데 시작하자" → 발동해야 함; (2) "이 오타 한 줄만 고쳐줘" → 발동 안 해야 함(사소한 작업). 발동·순서 확인.
> - Formal skill-creator eval / None.

Lightweight check passes → done. The user now has a personalized **skillset**:
two upstream-maintained skills (`grill-me`, `test-driven-development`) plus a thin
`grill-then-tdd` overlay that sequences them and speaks their stack.

**Sources:** [mattpocock/skills (grill-me)](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) ·
[Matt Pocock — "My 'Grill Me' Skill Went Viral"](https://www.aihero.dev/my-grill-me-skill-has-gone-viral) ·
[superpowers](https://github.com/obra/superpowers)

---

## Example 2 — Adopt-as-is (no personalization)

**User:** *"Is there a good skill for reviewing my code before I commit?"*

`finding-skills` only. Search `"code review before commit"` → shortlist
(`coderabbit`, `superpowers:requesting-code-review`, official `code-review`).
Present 2–3 as choices with install counts + token cost. User picks one →
**adopt as-is** → `claude plugin install …` → quick trigger check. No hand-off to
`personalizing-skills` because the defaults already fit. Done in one step — not
every request needs tuning.

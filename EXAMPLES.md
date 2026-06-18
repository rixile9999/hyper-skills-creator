# Use cases & worked examples

Concrete end-to-end runs of `hyper-skills-creator`. Each shows the interactive
choices as they'd actually appear, so you can see how the branching feels.

---

## Example 1 — A "clarify the spec (architecture + principles), then build TDD" skillset

**User:** *"Before any real coding I want the program's spec pinned down —
including the architecture and the architectural principles it must uphold — and
written somewhere concrete. Only then do I want to build it TDD-style. Make me a
skillset for that, tuned to my stack (TypeScript + vitest, concise commits)."*

This is a **skillset** request — two skills working as a sequence with a written
artifact in between — so it runs through both halves of the plugin:
`finding-skills` to source the pieces, then `personalizing-skills` to wire them
into a personalized set.

### finding-skills

**Step 1 — Clarify intent.** Already specific: two phases — (a) spec +
architecture clarification, captured to a doc; (b) TDD implementation; stack
TS/vitest. No clarifying question needed — search directly.

**Step 2 — Search the pool.** Two intents → two searches.

```bash
python3 skills/finding-skills/scripts/search_catalog.py "test driven development TDD" --limit 4
python3 skills/finding-skills/scripts/search_catalog.py "architecture spec design interrogation plan" --limit 6
```

- *TDD* → **`test-driven-development`** (in `superpowers`, 787k installs,
  marketplace). Strong, official, cheap. Found locally.
- *Spec/architecture interrogation* → the catalog has no clean match (top hits
  were generic brainstorming). So widen to **web search** (per Step 2.3): this
  surfaces **`grill-me`** from `mattpocock/skills` (~100k stars) — "get
  relentlessly interviewed about a plan or design until every branch of the
  decision tree is resolved." Exactly the spec-pinning engine we need. Flag it:
  *community-sourced, unverified — skim the SKILL.md before adopting.*
  (`superpowers:writing-plans` is a viable official alternative for the
  write-it-down part — offer it in the narrowing step.)

**Step 3 — Narrow interactively.** Present the two pieces and confirm the pairing:

> **AskUserQuestion — "스펙·아키텍처 명확화 스킬은 이걸로 갈까요?"**
> - **grill-me (mattpocock) — (추천)**: 코딩 전 결정 트리를 다 해소할 때까지 집요하게 인터뷰. 아키텍처·경계·원칙까지 캐물어 스펙을 픽스하기에 적합. ~100k stars, 커뮤니티(미검증 — 소스 확인 후 채택).
> - superpowers:writing-plans: 공식·검증됨, 스펙을 문서로 남기는 데 강함. 인터뷰의 집요함은 덜함 — grill-me와 조합도 가능.
> - 둘 다 비교: SKILL.md를 나란히 열어 비교.

> **AskUserQuestion — "구현 스킬은?"**
> - **superpowers:test-driven-development — (추천)**: RED-GREEN-REFACTOR. 787k installs, 공식. 이미 설치돼 있을 가능성 높음.

User picks **grill-me + test-driven-development**.

**Step 4 — Action.** Combining two skills into a tuned sequence = personalize.

> **AskUserQuestion — "이 둘을 어떻게 할까요?"**
> - **개인화 (추천)**: 두 스킬을 채택하고, "스펙 명확화 → 문서화 → TDD" 순서로 엮는 스킬셋 구성. → `personalizing-skills`로 인계.
> - 그대로 둘 다 설치: 순서·문서화 없이 각각.
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
commits; spec must be **written to a doc** before coding. (Save as durable memory
for future runs.)

**Step 2 — Choose a mode.**

> **AskUserQuestion — "스킬셋을 어떻게 구성할까요?"**
> - **Preference overlay — (추천)**: grill-me·TDD 원본은 그대로 두고(둘 다 활발히 유지됨), 둘을 "스펙 명확화 → 문서화 → TDD" 순서로 엮고 내 스택을 주입하는 얇은 컴패니언 스킬 `spec-then-tdd`를 새로 만듦. 비파괴적, 업스트림 업데이트 유지.
> - Fork & edit: TDD 스킬 본문을 복사해 vitest·아키텍처 가드 예시를 깊게 박음 — 더 무겁고 업스트림을 잃음.
> - Synthesize new: 둘을 통째로 합친 단일 스킬 — 가장 무거움.

User picks **overlay**. Create the companion skill (the "skillset" glue):

```markdown
---
name: spec-then-tdd
description: Use when starting any non-trivial feature, module, or service in this
  user's TypeScript projects — before writing implementation code. Clarifies the
  spec (including architecture and the architectural principles to uphold),
  records it to a doc, then drives a test-first build against it.
---

# Spec, then TDD (personalized workflow)

Two phases. Do NOT write implementation code until Phase 1 is written down and
signed off.

1. **Clarify the spec — architecture included.** Use the `grill-me` skill to
   relentlessly interview until the decision tree is resolved. Cover at minimum:
   - functional behavior and edge cases;
   - the **architecture** — modules/layers, boundaries, data flow, key interfaces;
   - the **architectural principles** to uphold — e.g. dependency direction /
     layering rules, separation of concerns, error-handling and testing strategy.
   Write the outcome to a short spec doc (`docs/spec-<feature>.md` or an ADR) so
   Phase 2 builds against something concrete, not memory.
2. **Build test-first against the spec.** Use
   `superpowers:test-driven-development` (RED-GREEN-REFACTOR). Each test asserts a
   behavior from the spec; where a principle is checkable (e.g. a lower layer must
   not import an upper one), add a test or lint rule that guards it. This user's
   conventions: tests in **vitest** (`describe/it`, `expect().toBe`, `vi.mock`),
   **concise** commits (imperative, ~50-char subject).

Why pair them: pinning the architecture and its principles first means the TDD
tests assert the *intended* design, and the principles become executable guards
rather than aspirations.
```

**Step 3 — Verify.**

> **AskUserQuestion — "검증은?"**
> - **Lightweight (추천)**: 트리거 문장 발사 — (1) "TS로 결제 모듈 새 서비스 설계부터 시작하자" → 발동, 스펙 단계부터 시작해야 함; (2) "이 오타 한 줄만 고쳐줘" → 발동 안 해야 함(사소한 작업). 발동·순서·문서화 확인.
> - Formal skill-creator eval / None.

Lightweight check passes → done. The user now has a personalized **skillset**:
two upstream-maintained skills (`grill-me`, `test-driven-development`) plus a thin
`spec-then-tdd` overlay that pins the spec and architecture, writes it down, and
then drives a test-first build against it in their stack.

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

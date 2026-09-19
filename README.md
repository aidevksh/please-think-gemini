# please-think-gemini 🧠⚡
> **"Gemini야, 제발 생각 좀 하고 답해줘!"** / **"Empowering Gemini to Rigorously Think Before Answering"**
> 코딩 에이전트의 지시 파일(`AGENTS.md` / `GEMINI.md` / `CLAUDE.md`)에 붙여넣는 심층 추론 규칙과,
> **그 효과를 420런으로 실측한 독립 검증 결과**.

---

<div align="center">

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Model](https://img.shields.io/badge/Measured_on-Gemini_3.8_Flash-4285F4.svg)](#)
[![Runs](https://img.shields.io/badge/Validation-420_runs-indigo.svg)](index.html)
[![Effect](https://img.shields.io/badge/Effect-%2B7.1pp_(95%25_CI_1.4~14.3)-brightgreen.svg)](index.html)
[![Report](https://img.shields.io/badge/Report-index.html-6366f1.svg)](index.html)

**[한국어](#한국어) | [English](#english)**

</div>

---

<a name="한국어"></a>
## 🇰🇷 한국어

### 1. 한 줄 요약

이 규칙은 **효과가 있습니다. 단, 모든 문제에서가 아니라 한 가지 실패 유형에서만입니다.**

Antigravity CLI(`agy`)로 Gemini 3.8 Flash에 **420회 직접 호출**해 대조군 실험한 결과, v3.1 프롬프트는 **140/140 (100%)** 을 기록해 프롬프트 없음(92.9%)·v1 단순 CoT(92.1%)를 앞섰습니다(Δ **+7.1pp**, 부트스트랩 95% CI **[+1.4, +14.3]**).
그러나 이 이득은 **14개 태스크 중 2개**에서만 발생했고, 나머지 12개는 프롬프트 없이도 전부 100%였습니다.

📊 **전체 리포트: [`index.html`](index.html)** (차트·통계·원자료 · 브라우저에서 열기)

---

### 2. 검증 결과

**조건별 종합** (14 태스크 × 3 조건 × 2 모델 × 5회 = 420런, 엄격 통과 기준)

| 조건 | 정답률 | 95% CI | 평균 응답 시간 | 평균 출력 |
| :--- | :---: | :---: | :---: | :---: |
| 프롬프트 없음 | 92.9% (130/140) | [84.3, 96.9] | 36.5s | 1,962자 |
| v1 단순 CoT ("Think step by step") | 92.1% (129/140) | [83.2, 96.7] | 41.0s | 2,797자 |
| **v3.1 Universal** | **100% (140/140)** | [94.8, 100] | 62.8s | 9,671자 |

**효과가 나온 곳은 단 2개 태스크** (조건당 10런)

| 태스크 | 프롬프트 없음 | v1 단순 CoT | v3.1 Universal |
| :--- | :---: | :---: | :---: |
| 5층 배치 퍼즐 — 질문이 "유일한 해"라 단정하지만 해가 2개 | 20% | **0%** | **100%** |
| 제한 순열 계수 — 저예산 모델의 고난도 조합 계산 | 80% | 90% | **100%** |
| 나머지 12개 태스크 (몬티홀·부분배열·100전구·비선형 최적화·Go 동시성·요세푸스·격자 경로 등) | 100% | 100% | 100% |

- **재현된 주장**: 5층 배치 퍼즐에서 "v1은 조기 수렴으로 실패, v3.1은 완전 탐색으로 해결"은 정확히 재현됐습니다. v1은 10런 전부 해를 1개만 찾았고, v3.1은 10런 전부 2개를 찾았습니다.
- **재현되지 않은 주장**: 몬티홀·부분배열 패리티·100전구·비선형 경계 최적화·Go 캐시 경쟁은 **프롬프트 없이도** Low 예산 모델까지 100%였습니다. Gemini 3.8 세대에서 이 문제들은 이미 천장입니다.

**비용**

| 모델 | 응답 시간 | 출력량 |
| :--- | :---: | :---: |
| Flash Low | 21.1s → 56.2s (**2.7배**) | 1,936자 → 11,941자 (**6.2배**) |
| Flash High | 51.9s → 69.3s (1.3배) | 1,989자 → 7,402자 (3.7배) |

> 💡 **Low + v3.1 (100%, 56.2s)** 이 **High + 무프롬프트 (92.9%, 51.9s)** 보다 정확했습니다.
> 추론 예산을 올리는 것보다 이 프롬프트를 쓰는 편이 비용 대비 유리합니다.

---

### 3. 언제 쓰고, 언제 쓰지 말 것인가

**쓰세요**
- 질문이 **전제를 단정할 때** ("유일한 해는?", "이 버그는 무엇인가?") — 모델이 그 전제를 그대로 받아들이는 것을 막습니다.
- 답이 **여러 개일 수 있는 탐색 문제** — 첫 해에서 멈추는 조기 수렴을 차단합니다.
- **저예산·저지연 모델**로 고난도 추론을 돌려야 할 때 — 상위 예산 모델을 사는 것보다 쌉니다.

**쓰지 마세요**
- 모델이 이미 안정적으로 푸는 정형 문제 — 정확도는 그대로인데 시간 2.7배, 토큰 6.2배를 냅니다.
- 지연 시간이 중요한 대화형·스트리밍 UX.
- "단계별로 생각하라"(v1) 수준의 지시로 충분하다고 기대하는 경우 — 측정 결과 v1은 무프롬프트 대비 **개선 없음**이었고, 거짓 전제 태스크에서는 오히려 0%로 더 나빴습니다.

---

### 4. 4-Phase 적대적 인지 아키텍처

배포본: [`AGENTS.md`](AGENTS.md) · 검증에 사용한 원문: [`FINAL_COT_PROMPT.md`](FINAL_COT_PROMPT.md)

1. **Phase 1 — 문제 해체 및 함정 감사**: 명시된 제약 나열, 도메인별 함정 감사(경계 극값 / Check-then-Act 경합 / 시점 혼동), **질문의 전제 자체를 의심**.
2. **Phase 2 — 발산적 탐색**: 서로 독립적인 해결 경로를 2개 이상 수립하고, 가능한 분기를 전수 조사(조기 수렴 금지).
3. **Phase 3 — 적대적 검증**: 자신의 결론이 틀렸다고 가정하고 반례·경계값·동시성 부하를 가상 실행, 역산 대입으로 확인.
4. **Phase 4 — 최종 합성**: 검증을 통과한 답만 `[FINAL_ANSWER]`로 분리 출력.

측정된 효과(전제 의심 + 완전 탐색)는 **Phase 1·2**에서 나옵니다.

---

### 5. 사용법 — 에이전트 지시 파일에 붙여넣기

이 규칙은 **에이전트가 매 작업마다 읽는 마크다운**에 넣어 쓰는 것을 전제로 만들어졌습니다. 소스 코드에 붙이거나 매 프롬프트에 복사할 필요가 없습니다.

프로젝트 루트(또는 홈 디렉터리)에 아래 이름 중 도구에 맞는 것으로 저장하면 끝입니다:

| 도구 | 파일 경로 |
| :--- | :--- |
| Antigravity CLI (`agy`) | `AGENTS.md` · `GEMINI.md` · `.agents/rules/*.md` |
| Gemini CLI | `GEMINI.md` |
| Claude Code | `CLAUDE.md` |
| Codex · Cursor · 기타 | `AGENTS.md` |

```bash
# 이 저장소의 규칙 파일을 내 프로젝트로 복사
curl -O https://raw.githubusercontent.com/aidevksh/please-think-gemini/main/AGENTS.md

# 다른 도구용 이름이 필요하면 복사 또는 심볼릭 링크
cp AGENTS.md GEMINI.md      # Antigravity / Gemini CLI
cp AGENTS.md CLAUDE.md      # Claude Code
```

전체 내용: **[`AGENTS.md`](AGENTS.md)** — 아래 블록을 그대로 복사해도 동일합니다.

<details>
<summary><b>📋 복사용 전문 (클릭해서 펼치기)</b></summary>

````markdown
# Deep Reasoning Rules — please-think-gemini v3.1

## When to apply

Run the full 4-phase procedure below **before answering** whenever ANY of these holds:

- The question **asserts a premise** — "the unique solution", "the bug is X", "why does Y always fail".
- **More than one valid answer may exist**, or the task asks *how many* / *list all* / *find every*.
- The task involves **concurrency, boundary conditions, state transitions, or exhaustive counting**.
- The change is **hard to reverse or wide in blast radius** — migrations, deletions, schema or production config.
- You are running on a **small or fast model tier** and the task is not trivial.

**Do NOT run it** for lookups, renames, formatting, single-line edits, or anything you already solve reliably. Answer directly. The procedure costs roughly **2.7× latency and 6× output tokens**, and buys nothing on tasks that were never at risk.

## The one rule that matters most

**Never call an answer unique, complete, or the only cause until you have enumerated the space and shown the other branches fail.** If the user's question presupposes uniqueness and you find a second valid answer, say the premise is wrong and give every answer.

## Phase 1 — Deconstruction & trap audit

1. Enumerate every explicit constraint: rules, constants, domain limits, boundary conditions.
2. Audit the traps for the domain at hand:
   - **Logic & math**: intuitive shortcuts, degree mismatches (linear vs. non-linear terms), interior vs. boundary extrema.
   - **Code & systems**: check-then-act races, lock contention, thundering herds, non-atomic mutations, resource leaks.
   - **Research & data**: temporal drift (outdated versions, deprecated APIs), primary documentation vs. secondary claims.
3. **Question the premise**: is the prompt steering you toward a false assumption — that a unique solution exists when there may be several or none?
4. State the formal space: notation, entities, invariants.

## Phase 2 — Divergent exploration

1. **No early convergence.** Formulate at least TWO independent resolution strategies:
   - *Math*: analytic / Lagrangian vs. boundary / invariant / inequality analysis.
   - *Code*: idiomatic standard library (e.g. `singleflight`, atomics) vs. explicit synchronization (double-checked locking, mutex). Compare complexity and resource overhead.
   - *Research*: multi-source comparison reconciling conflicting specifications.
2. **Exhaustive branch tree.** If multiple cases, configurations, or interleavings exist, branch all of them and prove why the impossible ones fail by explicit contradiction.
3. **Deterministic state tracking.** Use a table or step-indexed transitions for sequential operations, state changes, and concurrent execution orders.

## Phase 3 — Adversarial verification

1. **Assume your tentative answer is wrong.** Ask where it collapses: which edge case, load, or counterexample breaks it?
2. Verify by domain:
   - *Math*: substitute the result back into every original equation and bound.
   - *Code*: mentally execute against null / empty / zero inputs, single-element and boundary thresholds, high-concurrency contention, and cleanup paths (deferred unlock, goroutine leak, context cancellation).
   - *Research*: reconcile sources; when they conflict, identify the authoritative specification or state the exact conditions under which each holds.
3. **Cross-method reconciliation.** Confirm the two strategies from Phase 2 reach the same conclusion. If they disagree, you are not done.

## Phase 4 — Synthesis

State only what survived Phase 3. No logical leaps, no steps skipped silently.

## Output contract

Put the deliberation in `[THOUGHT_PROCESS]` and the result in `[FINAL_ANSWER]`, in this order. `[FINAL_ANSWER]` contains:

- The direct answer, conclusion, or production-ready code, stated first.
- The key proofs, concurrency guarantees, or verified citations that back it.
- Edge cases, **all** valid solutions, and trade-offs.
- The same language as the user's question.
````

</details>

> ⚖️ **측정한 텍스트와 배포본의 차이(중요)**: 위 420런 실험에서 측정한 것은 [`FINAL_COT_PROMPT.md`](FINAL_COT_PROMPT.md)의 v3.1 원문이며, 단일 턴·도구 사용 금지 조건이었습니다.
> [`AGENTS.md`](AGENTS.md)는 4-Phase 본문을 그대로 유지하되 에이전트 상시 로딩에 맞춰 **"When to apply" 게이트와 전제 단정 금지 규칙을 추가**한 버전입니다.
> 즉 4-Phase 절차의 효과는 실측값이지만, 게이트가 붙은 이 배포본 자체를 멀티턴 에이전트 환경에서 측정한 것은 아닙니다.
>
> 💡 **왜 영문인가**: 검증 실험에서 측정한 구성이 "영문 규칙 + 한국어 질문"입니다. 한국어로 물어도 `[FINAL_ANSWER]`는 질문 언어로 나옵니다(출력 규약에 명시).
>
> ⚠️ **적용 범위 주의**: 규칙 첫 문단의 "When to apply" 게이트를 지우지 마세요. 게이트 없이 항상 켜두면 단순 작업에서도 응답 시간 2.7배·출력 6.2배를 그대로 지불하게 됩니다.

**API로 직접 쓰는 경우**에는 같은 내용을 system instruction으로 넣으면 됩니다:

```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="x, y, z >= 0, x + 2y + 3z = 6 일 때 f = x^2*y + 3z 의 최대·최소를 모두 구하시오.",
    config=types.GenerateContentConfig(
        system_instruction=open("AGENTS.md", encoding="utf-8").read(),
        temperature=0.1,
    ),
)
print(response.text)
```

---


### 6. 검증 방법과 재현

측정의 신뢰성을 위해 적용한 통제:

- 매 런을 **빈 임시 디렉터리**에서 실행 — 에이전트가 저장소의 정답 파일을 읽는 경로를 차단
- 세 조건 모두에 **동일한 "도구 사용 금지, 순수 추론" 규칙** 부여
- 정답은 전부 **브루트포스 스크립트로 직접 계산**, `ANSWER:` 한 줄 형식 강제 후 정규식 결정적 채점
- 신규 고난도 태스크 8종은 **난이도 사전 선별 없이 전량 투입**(선택 편향 배제)
- Wilson 95% 신뢰구간 + 20,000회 부트스트랩

재현 코드·원자료: [`experiments/validation/`](experiments/validation/) (하네스, 채점기, 런별 결과, 모델 원본 응답 433건)

**알려진 한계**: 실험 막바지 쿼터 소진으로 2개 태스크(`x_premise` 0/30런, `x_knapsack` 13/30런)가 집계에서 빠졌습니다. 특히 `x_premise`는 위 "거짓 전제" 효과를 독립 태스크로 재현하려던 검증이라, 현재 결론의 핵심 근거는 태스크 1개에 의존합니다. 12개 태스크의 천장 효과 때문에 이 벤치마크는 그 구간에서 우열을 가릴 수 없다는 점도 함께 감안해 주세요.

---

<a name="english"></a>
## 🌐 English

### TL;DR

The prompt **works — but only on one failure mode, not across the board.**

In a controlled experiment of **420 direct calls** to Gemini 3.8 Flash via the Antigravity CLI (`agy`), v3.1 scored **140/140 (100%)** against 92.9% with no prompt and 92.1% with naive "think step by step" CoT (Δ **+7.1pp**, bootstrap 95% CI **[+1.4, +14.3]**). But the entire gain came from **2 of 14 tasks**; the other 12 were already at 100% with no prompt at all.

📊 **Full report: [`index.html`](index.html)**

### Results

| Condition | Pass rate | 95% CI | Mean latency | Mean output |
| :--- | :---: | :---: | :---: | :---: |
| No prompt | 92.9% (130/140) | [84.3, 96.9] | 36.5s | 1,962 chars |
| v1 naive CoT | 92.1% (129/140) | [83.2, 96.7] | 41.0s | 2,797 chars |
| **v3.1 Universal** | **100% (140/140)** | [94.8, 100] | 62.8s | 9,671 chars |

Where the gain came from (10 runs per condition):

| Task | No prompt | v1 naive CoT | v3.1 |
| :--- | :---: | :---: | :---: |
| 5-floor puzzle — question asserts a "unique" solution, but there are 2 | 20% | **0%** | **100%** |
| Restricted permutation count — hard combinatorics on the low-budget model | 80% | 90% | **100%** |
| The other 12 tasks (Monty Hall, subarray parity, 100 bulbs, nonlinear extrema, Go concurrency, …) | 100% | 100% | 100% |

**Reproduced**: the repo's claim that naive CoT prematurely converges on the 5-floor puzzle while v3.1 exhausts the search space — v1 found one solution in all 10 runs, v3.1 found both in all 10.
**Not reproduced**: the claimed baseline failures on Monty Hall, subarray parity, 100-bulb toggle, nonlinear boundary extrema, and the Go cache race. All were solved with no prompt, even on the low reasoning budget.

**Cost**: on Flash Low, 2.7× latency (21.1s → 56.2s) and 6.2× output (1,936 → 11,941 chars). Notably, **Low + v3.1 (100%, 56.2s) beat High + no prompt (92.9%, 51.9s)** — the prompt buys more accuracy per second than a bigger reasoning budget does.

### How to use it

Drop [`AGENTS.md`](AGENTS.md) into your project root under the name your tool reads — `AGENTS.md` (Antigravity CLI, Codex, Cursor), `GEMINI.md` (Antigravity / Gemini CLI), or `CLAUDE.md` (Claude Code). It is written to live in the agent's always-on instruction file, not to be pasted into source or repeated per prompt. Keep the "When to apply" gate at the top: without it you pay 2.7× latency and 6× output on trivial tasks too.

**What was measured vs. what ships**: the 420-run experiment measured the v3.1 text in [`FINAL_COT_PROMPT.md`](FINAL_COT_PROMPT.md), single-turn and with no tools. [`AGENTS.md`](AGENTS.md) keeps that 4-phase body and adds the "When to apply" gate plus the no-false-uniqueness rule for always-on agent use — so the procedure's effect is measured, but this gated build has not been re-measured in a multi-turn agent loop.

### Use it when

The question **asserts a premise** ("what is the unique solution?"), the answer space may hold **multiple valid solutions**, or you need hard reasoning out of a **cheap, fast model**. Skip it for tasks the model already solves reliably — you pay 2.7× latency and 6.2× tokens for no measurable accuracy gain.

### Reproduce

Harness, graders, per-run results and 433 raw model outputs: [`experiments/validation/`](experiments/validation/). Controls: every run in a clean temp dir (no access to the repo's answer files), an identical "no tools, pure reasoning" rule across all three conditions, ground truth computed by brute force, deterministic regex grading on a forced `ANSWER:` line, and no difficulty pre-screening of new tasks. **Known gap**: quota exhaustion left 2 tasks out (`x_premise` 0/30 runs, `x_knapsack` 13/30), and `x_premise` was the planned independent replication of the false-premise effect.

---

## 📁 저장소 구조 (Repository Structure)

```
please-think-gemini/
├── LICENSE                         # Apache License 2.0
├── README.md                       # 이 문서 (한국어 / English)
├── AGENTS.md                       # ⭐ 에이전트 지시 파일용 규칙 (복사해서 쓰는 본체)
├── FINAL_COT_PROMPT.md             # v3.1 원문 프롬프트 + 실측 요약
├── index.html                      # 독립 검증 리포트 (차트·통계)
├── prompts/
│   ├── v1_naive_cot.md             # 1단계: 고전적 "Think step by step"
│   ├── v2_structured_cot.md        # 2단계: 4단 섹션 구조화
│   └── v3_adversarial_cot.md       # 3단계: 적대적 자가 검증
└── experiments/
    ├── tasks.md                    # 논리/퍼즐 벤치마크 정의서
    ├── multi_domain_tasks.md       # 수학/코딩/리서치 벤치마크 정의서
    └── validation/                 # 독립 검증 하네스 · 원자료 · 채점 결과
        ├── README.md               # 재현 방법
        ├── tasks.py                # 태스크 16종 정의(정답 포함)
        ├── runner.py               # agy 호출 하네스
        ├── grade.py / analyze.py   # 결정적 채점 · 통계 집계
        ├── summary.json / graded.json
        └── raw_outputs.tar.gz      # 모델 원본 응답 433건
```

---

## 📄 라이선스 (License)

[Apache License 2.0](LICENSE) 하에 배포됩니다. 자유롭게 인용·수정·재배포하실 수 있습니다.

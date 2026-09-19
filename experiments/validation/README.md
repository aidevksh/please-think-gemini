# 독립 검증 하네스 (Independent Validation Harness)

`FINAL_COT_PROMPT.md`의 v3.1 Universal 프롬프트가 실제로 정답률을 올리는지,
Antigravity CLI(`agy`)로 Gemini 3.8 Flash에 직접 호출해 대조군 실험으로 측정한 코드와 원자료입니다.

결과 리포트: [`../../index.html`](../../index.html)

## 실험 설계

| 항목 | 값 |
| :--- | :--- |
| 조건 | `base`(프롬프트 없음) / `v1`(단순 CoT) / `v31`(v3.1 Universal) |
| 모델 | `gemini-3.8-flash-low`, `gemini-3.8-flash-high` |
| 태스크 | 14종 (저장소 원본 6 + 신규 고난도 8) |
| 반복 | 셀당 5회 · 총 420런 |
| 통제 | 매 런 빈 임시 디렉터리에서 실행(저장소 정답 파일 차단), 전 조건 동일한 "도구 사용 금지" 규칙 |
| 채점 | `ANSWER:` 한 줄 강제 + 정규식 결정적 채점, 항목 전부 정답일 때만 통과 |
| 통계 | Wilson 95% CI, 20,000회 부트스트랩 |

정답(ground truth)은 모두 브루트포스 스크립트로 직접 계산해 확정했습니다.

## 핵심 결과

- v3.1 **140/140 (100%)** vs 프롬프트 없음 92.9% vs v1 92.1%, Δ +7.1pp (95% CI [+1.4, +14.3])
- 다만 이득은 **14개 중 2개 태스크**에서만 발생 — 거짓 전제 다중해 퍼즐(`floors`: 20% → 100%)과
  저예산 모델의 고난도 조합 계수(`x_permcount`: 60% → 100%)
- 나머지 12개 태스크는 전 조건 100% (천장 효과)
- 비용: Low 모델 기준 응답 시간 2.7배, 출력량 6.2배

## 재현 방법

```bash
# 1) 실험 실행: <모델들> <조건들> <태스크들|all> <반복> <병렬도>
python3 runner.py gemini-3.8-flash-low,gemini-3.8-flash-high base,v1,v31 all 5 14

# 2) 채점 (raw/*.json → graded.json)
python3 grade.py

# 3) 통계 집계 (→ summary.json)
python3 analyze.py

# 4) 리포트 HTML 생성
python3 build_report.py
```

`runner.py`는 `raw/<task>__<cond>__<model>__r<n>.json`이 이미 있으면 건너뛰므로,
중단 후 같은 명령을 다시 실행하면 이어서 채웁니다.

## 파일

| 파일 | 설명 |
| :--- | :--- |
| `tasks.py` | 태스크 16종 정의(문제 · 출력 형식 · 정답) |
| `runner.py` | `agy -p` 호출 하네스(빈 작업 디렉터리, 빈 응답 3회 재시도) |
| `grade.py` | 태스크별 결정적 채점기 |
| `analyze.py` | Wilson CI · 부트스트랩 · 태스크별 집계 |
| `build_report.py`, `report_template.html`, `narrative.json` | 리포트 생성 |
| `prompt_v31.txt`, `prompt_v1.txt` | 실험에 투입된 프롬프트 원문 |
| `summary.json`, `graded.json` | 집계 결과 · 런별 채점 결과 |
| `raw_outputs.tar.gz` | 433개 런의 모델 원본 응답 |

## 미완 항목

Antigravity 개인 쿼터 소진으로 아래 2개 태스크는 집계에서 제외했습니다. 쿼터 리셋 후 위 1)~4) 명령을 그대로 실행하면 보강됩니다.

- `x_premise` (4차방정식 거짓 전제): 0/30런 — 거짓 전제 효과의 **독립 재현** 검증이므로 보강 가치가 가장 큽니다.
- `x_knapsack` (배낭 최적화): 13/30런

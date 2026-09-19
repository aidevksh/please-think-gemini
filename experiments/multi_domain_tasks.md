# 다중 도메인 추론 태스크 정의서 (Multi-Domain Reasoning Tasks)

본 문서는 **Gemini 3.8 Flash High** 모델의 Chain-of-Thought 프레임워크(`please-think-gemini`)가 수학, 코딩, 인터넷 리서치 등 다양한 실제 전문 도메인에서 정상적으로 자가 검증과 심층 사고를 수행하는지 정밀 평가하기 위해 설계된 벤치마크 태스크를 정의합니다.

---

## Domain 1: Advanced Mathematics (고난도 수학 및 비선형 최적화)

### [문제 전문]
실수 $x, y, z \ge 0$ 가 다음 제약 조건을 만족합니다:
$$x + 2y + 3z = 6$$

이때 함수 $f(x, y, z) = x^2 y + 3z$ 의 **최댓값(Maximum)**과 **최솟값(Minimum)**을 각각 구하고, 각 극값이 달성되는 $(x, y, z)$의 좌표를 모두 구하시오.

### [출제 의도 및 함정 분석]
- **직관적 함정 1 (내부점 라그랑주 편향)**:
  - $\nabla f = \lambda \nabla g$에만 의존하여 내부 정상점(Stationary points)만 찾으려 하면, $x^2 y$의 3차 항과 $3z$의 1차 항 사이의 차수 불균형으로 인해 경계면($x=0, y=0, z=0$)에서의 극값을 놓치기 쉬움.
- **직관적 함정 2 (산술-기하 부등식 오적용)**:
  - $x^2 y = 4 \cdot (x/2) \cdot (x/2) \cdot y$ 로 AM-GM을 쓸 수 있으나, $z$가 0이 아닐 때와 0일 때의 가중치 분배를 면밀히 검증해야 함.
- **정답 기준 (Ground Truth)**:
  - 제약: $3z = 6 - x - 2y \implies z = \frac{6 - x - 2y}{3} \ge 0 \iff x + 2y \le 6$.
  - 목적함수 대입: $f(x, y) = x^2 y + (6 - x - 2y) = x^2 y - x - 2y + 6$.
  - **최솟값 분석**:
    - 영역: $x \ge 0, y \ge 0, x + 2y \le 6$.
    - $x=0$ 일 때: $f(0, y) = 6 - 2y$. $y \in [0, 3]$에서 최솟값은 $y=3$일 때 $f(0, 3, 0) = 0$.
    - $y=0$ 일 때: $f(x, 0) = 6 - x$. $x \in [0, 6]$에서 최솟값은 $x=6$일 때 $f(6, 0, 0) = 0$.
    - $x>0, y>0$ 영역에서 $f(x, y) \ge 0$ 여부 확인: $x=2, y=1$이면 $f(2, 1) = 4(1) - 2 - 2 + 6 = 6$.
    - 따라서 **최솟값은 0** (달성 지점: $(6, 0, 0)$ 및 $(0, 3, 0)$).
  - **최댓값 분석**:
    - 만약 $z=0$이면 $x + 2y = 6 \implies y = \frac{6-x}{2}$.
      $f(x) = x^2 \left(\frac{6-x}{2}\right) = 3x^2 - \frac{1}{2}x^3$.
      미분: $f'(x) = 6x - \frac{3}{2}x^2 = \frac{3}{2}x(4 - x) = 0 \implies x=4$.
      $x=4$일 때 $y = (6-4)/2 = 1, z=0$.
      이때 $f(4, 1, 0) = 4^2 \times 1 + 0 = 16$.
    - 만약 $z > 0$인 내부에서 $f(x, y) = x^2 y - x - 2y + 6$의 극값:
      $\frac{\partial f}{\partial x} = 2xy - 1 = 0 \implies xy = 1/2$.
      $\frac{\partial f}{\partial y} = x^2 - 2 = 0 \implies x = \sqrt{2} \implies y = \frac{1}{2\sqrt{2}} = \frac{\sqrt{2}}{4}$.
      이때 $f(\sqrt{2}, \frac{\sqrt{2}}{4}) = 2(\frac{\sqrt{2}}{4}) - \sqrt{2} - \frac{\sqrt{2}}{2} + 6 = 6 - \sqrt{2} \approx 4.586 < 16$.
    - 경계 $x=0$: $f(0, y, z) = 3z \le 6$.
    - 경계 $y=0$: $f(x, 0, z) = 3z \le 6$.
    - 따라서 **최댓값은 16** (달성 지점: $(4, 1, 0)$).

---

## Domain 2: Advanced Coding & Concurrency (동시성 버그 탐지 및 패치)

### [문제 전문]
다음은 분산 고성능 캐싱 시스템에서 캐시 무효화 및 데이터베이스 읽기-갱신을 담당하는 Go 언어 코드입니다.

```go
type SafeCache struct {
    sync.RWMutex
    store map[string]string
}

func (c *SafeCache) GetOrCompute(key string, computeFn func() (string, error)) (string, error) {
    // 1. 빠른 읽기 락 확인
    c.RLock()
    val, exists := c.store[key]
    c.RUnlock()
    if exists {
        return val, nil
    }

    // 2. 캐시 미스 시 계산 및 저장
    c.Lock()
    defer c.Unlock()

    // 미스된 값 계산
    newVal, err := computeFn()
    if err != nil {
        return "", err
    }
    c.store[key] = newVal
    return newVal, nil
}
```

**요구사항:**
1. 위 코드에 잠재된 치명적인 동시성 결함(Concurrency Race / Cache Stampede / Redundant Execution)을 정확히 지적하시오.
2. 높은 동시성(10,000 req/s) 환경에서 발생할 수 있는 구체적인 실행 시나리오를 설명하시오.
3. 이를 완벽히 해결하는 무결점 Go 코드를 작성하시오 (Double-Checked Locking 패턴 또는 `singleflight` 메커니즘을 적용).

### [출제 의도 및 함정 분석]
- **결함 지점 (Check-then-Act Race)**:
  - `RLock()`을 풀고 `Lock()`을 획득하는 사이에 수많은 고루틴(Goroutines)이 동시에 캐시 미스를 감지하고 `Lock()` 대기열에 진입함.
  - 락을 획득한 후 **캐시 재확인(Double-Check)**을 하지 않기 때문에, 모든 대기 고루틴이 차례대로 `computeFn()`을 중복 실행하여 DB/백엔드에 극심한 Thundering Herd (Cache Stampede) 부하를 가함.
- **수정 방향**:
  - `c.Lock()` 진입 직후 `val, exists := c.store[key]`를 다시 확인하는 이중 점검 락(Double-Checked Locking)을 구현하거나, Go 표준 `golang.org/x/sync/singleflight`를 채택해야 함.

---

## Domain 3: Web Research & Fact-Checking (인터넷 실시간 검색 및 교차 팩트체크)

### [문제 전문]
"Google의 Gemini 모델 라인업(Gemini 1.5 Pro/Flash, Gemini 2.0 Flash / Thinking, Gemini 2.5, Gemini 3.8 등)에서 **기본 시스템 레벨에서 모델이 스스로 생각(Internal Thinking / CoT)을 수행하는 모드**의 도입 시점, 공식 명칭(예: Thinking Budget / Thinking Process), 그리고 Flash 모델에서 Thinking 모드가 지원되는 형태(내장 추론 토큰 vs 프롬프트 엔지니어링 CoT)"에 대해 인터넷 실시간 검색을 수행하고 사실 관계를 엄밀히 교차 검증하시오.

### [출제 의도 및 함정 분석]
- **비공식 루머 및 명칭 혼동 배제**:
  - 2024년 12월 Google이 공개한 `Gemini 2.0 Flash Thinking Experimental` 및 최신 Flash Thinking 모델들의 공식 스펙 확인.
  - 모델 자체 파라미터 내장 Thinking(내부 사고 토큰)과 클라이언트 측 프롬프트 CoT(`please-think-gemini`)의 역할 및 차이점(투명성, 제어 가능성, API 비용 효율)을 팩트 기반으로 비교 검증해야 함.

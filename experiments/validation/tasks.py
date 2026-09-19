# -*- coding: utf-8 -*-
# Task bank: every task has a verified ground truth and a deterministic grader.
TASKS = {}

TASKS["math_opt"] = dict(
    domain="Advanced Math",
    question=r"""실수 x, y, z >= 0 이 x + 2y + 3z = 6 을 만족합니다.
함수 f(x, y, z) = x^2 * y + 3z 의 최댓값과 최솟값을 구하고, 각 극값이 달성되는 (x, y, z) 좌표를 **모두** 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: max=<값>@<좌표들>; min=<값>@<좌표들>
좌표는 (x,y,z) 형식이며 여러 개면 쉼표로 구분. 예: ANSWER: max=9@(1,2,0); min=1@(0,0,2),(3,0,1)""",
    truth="max=16@(4,1,0); min=0@(6,0,0),(0,3,0)",
)

TASKS["monty"] = dict(
    domain="Probability",
    question=r"""문 A, B, C 중 하나 뒤에만 자동차가 있고(각 1/3 균등), 나머지엔 염소가 있습니다. 당신은 문 A를 선택했습니다.
진행자는 차의 위치를 알고, 당신이 고르지 않은 문 중 염소가 있는 문을 반드시 하나 엽니다. 진행자 규칙:
- 차가 A에 있으면: B와 C 중 하나를 각 1/2 확률로 무작위로 엽니다.
- 차가 B에 있으면: 반드시 C를 엽니다.
- 차가 C에 있으면: 반드시 B를 엽니다.
진행자가 문 B를 열었고 염소가 나왔습니다.
베이즈 정리로 P(차=C | 진행자가 B를 엶)와 P(차=A | 진행자가 B를 엶)를 엄밀히 계산하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: switch=<분수>, stay=<분수>
예: ANSWER: switch=1/2, stay=1/2""",
    truth="switch=2/3, stay=1/3",
)

TASKS["subarray"] = dict(
    domain="Discrete Math",
    question=r"""길이 7인 정수 배열 A = [3, -2, 5, -1, 4, -6, 2] (인덱스 1..7)가 주어집니다.
다음 두 조건을 **동시에** 만족하는 연속 부분배열 A[i..j] (1 <= i <= j <= 7)의 총 개수를 구하시오:
1) 길이 (j - i + 1) >= 3
2) 구간 합이 짝수""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <개수>
예: ANSWER: 12""",
    truth="9",
)

TASKS["bulbs"] = dict(
    domain="Number Theory",
    question=r"""1번부터 100번까지 번호가 붙은 전구 100개가 모두 OFF 상태입니다.
k번째 사람은 k의 배수 번호 전구를 모두 토글합니다. 1번부터 50번째 사람까지 정상적으로 진행했습니다.
50번째 사람 직후, 관리자가 난입하여 "양의 약수의 개수가 정확히 3개인 모든 번호의 전구"를 현재 상태와 무관하게 강제로 OFF로 리셋했습니다.
그 직후 51번째 사람부터 100번째 사람까지 다시 원래 규칙대로 자기 번호의 배수 전구를 토글하고 지나갔습니다.
모든 과정이 끝난 후 최종적으로 ON 상태인 전구의 번호 전체와 총 개수를 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <ON인 번호들을 오름차순 쉼표 구분>; count=<개수>
예: ANSWER: 1,4,9; count=3""",
    truth="1,16,36,64,81,100; count=6",
)

TASKS["floors"] = dict(
    domain="Constraint Logic (false premise)",
    question=r"""개발자 Alex, Blake, Casey, Dana, Evan 5명이 5층 건물(1~5층)에 층당 정확히 한 명씩 거주합니다. 조건:
1. Alex는 Blake보다 위층에 산다.
2. Casey는 홀수 층에 살지 않는다.
3. |Floor(Blake) - Floor(Casey)| = 3
4. Floor(Dana) != Floor(Evan) + 1
5. Evan은 1층에 살지 않는다.
6. 만약 Casey가 4층이면, Dana는 Alex보다 아래층이다.
**유일한 해**가 도출되는 논리적 증명 과정을 서술하고, 1층부터 5층까지 거주자를 밝히시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: solutions=<유효한 배치의 개수>; <각 배치를 1층|2층|3층|4층|5층 순서로, 배치 간에는 / 로 구분>
예: ANSWER: solutions=1; Blake|Dana|Evan|Casey|Alex""",
    truth="solutions=2; Blake|Dana|Evan|Casey|Alex / Blake|Dana|Alex|Casey|Evan",
)

TASKS["go_race"] = dict(
    domain="Concurrency / Code",
    question=r"""다음 Go 캐시 구현을 리뷰하시오.

```go
type SafeCache struct {
    sync.RWMutex
    store map[string]string
}

func (c *SafeCache) GetOrCompute(key string, computeFn func() (string, error)) (string, error) {
    c.RLock()
    val, exists := c.store[key]
    c.RUnlock()
    if exists {
        return val, nil
    }

    c.Lock()
    defer c.Unlock()

    newVal, err := computeFn()
    if err != nil {
        return "", err
    }
    c.store[key] = newVal
    return newVal, nil
}
```
1) 잠재된 치명적 동시성 결함을 정확히 지적하고, 2) 10,000 req/s 환경의 구체적 실행 시나리오를 설명하고, 3) 이를 해결한 무결점 Go 코드를 제시하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: bug=<결함명>; fix=<적용한 해결 패턴명>
예: ANSWER: bug=deadlock; fix=mutex""",
    truth="bug=check-then-act / cache stampede; fix=double-checked locking or singleflight",
)

# ---------------- Tier 2: harder tasks (ground truth verified by brute force locally) -------------
TASKS["h_triples"] = dict(
    domain="Number Theory (hard)",
    question=r"""N = 64800 = 2^5 * 3^4 * 5^2 입니다.
a * b * c = N 이고 a < b < c 인 양의 정수 순서쌍 (a, b, c)의 개수를 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <개수>
예: ANSWER: 123""",
    truth="306",
)

TASKS["h_josephus"] = dict(
    domain="Simulation (hard)",
    question=r"""1번부터 17번까지 번호가 붙은 17명이 원형으로 둘러서 있습니다(17번 다음은 다시 1번).
1번부터 세기 시작하여 4번째 사람이 제거됩니다(즉, 첫 번째로 제거되는 사람은 4번).
제거된 사람 바로 다음 사람부터 다시 1로 세기 시작하여, 매번 4번째 사람을 제거합니다.
마지막에 혼자 남는 생존자의 번호를 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <생존자 번호>
예: ANSWER: 7""",
    truth="5",
)

TASKS["h_seating"] = dict(
    domain="Constraint Logic (hard, false premise)",
    question=r"""A, B, C, D, E, F 여섯 명이 1번부터 6번까지 일렬로 놓인 좌석에 한 명씩 앉습니다. 조건:
1. A와 B는 서로 바로 옆자리에 앉는다 (좌석 번호 차이가 1).
2. C는 D보다 오른쪽(더 큰 번호)에 앉는다.
3. E는 짝수 번호 좌석에 앉는다.
4. F와 C의 좌석 번호 차이는 3 이상이다.
5. D는 1번 좌석에 앉지 않는다.
6. A는 E보다 왼쪽(더 작은 번호)에 앉는다.
7. F는 6번 좌석에 앉지 않는다.
이 조건을 모두 만족하는 **유일한 배치**를 찾고, 가능한 배치의 총 개수를 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: count=<조건을 모두 만족하는 배치의 총 개수>
예: ANSWER: count=1""",
    truth="count=8",
)

TASKS["h_modexp"] = dict(
    domain="Modular Arithmetic (hard)",
    question=r"""7^2025 를 1000으로 나눈 나머지(즉 마지막 세 자리 수)를 구하시오.""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <나머지>
예: ANSWER: 001""",
    truth="807",
)

TASKS["h_gobugs"] = dict(
    domain="Concurrency (hard, multi-bug)",
    question=r"""다음 Go 함수를 리뷰하고, 잠재된 **모든** 동시성 결함을 빠짐없이 지적한 뒤 수정 코드를 제시하시오.

```go
func Process(items []string) map[string]int {
    result := make(map[string]int)
    var wg sync.WaitGroup
    idx := 0

    for range items {
        go func() {
            wg.Add(1)
            defer wg.Done()
            item := items[idx]
            idx++
            result[item] = len(item)
        }()
    }

    wg.Wait()
    return result
}
```""",
    fmt=r"""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: bugs=<발견한 결함들을 쉼표로 구분>; fix=<적용한 동기화 수단>
예: ANSWER: bugs=map race, wg.Add placement; fix=mutex""",
    truth="bugs: (1) concurrent map write, (2) wg.Add inside goroutine racing with Wait, (3) unsynchronized shared idx (data race / out-of-range)",
)

# ---------------- Tier 3: brutal grind / trap tasks ----------------
TASKS["x_gridpaths"] = dict(
    domain="Combinatorics (grind)",
    question=r"""8x8 격자의 좌표 (0,0)에서 (7,7)까지 오른쪽(+1,0) 또는 위쪽(0,+1)으로만 이동합니다.
단, 다음 4개의 칸은 통과할 수 없습니다: (2,2), (3,5), (5,3), (6,1).
(0,0)에서 (7,7)까지 가는 서로 다른 경로의 총 개수를 구하시오.""",
    fmt="""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <경로 개수>
예: ANSWER: 1234""",
    truth="911",
)

TASKS["x_simgrind"] = dict(
    domain="Iterative Simulation (grind)",
    question=r"""정수 n의 초기값은 7입니다. 다음 규칙을 정확히 25번 반복 적용합니다:
- n이 짝수이면: n <- n/2 + 3
- n이 홀수이면: n <- 3n + 1
초기값 7을 포함하여, 매 단계마다의 n 값을 모두 더한 총합(초기값 + 25번의 결과값, 총 26개 값의 합)을 구하시오.""",
    fmt="""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <총합>
예: ANSWER: 500""",
    truth="312",
)

TASKS["x_permcount"] = dict(
    domain="Combinatorics (very hard)",
    question=r"""1부터 9까지의 수를 나열한 순열 p(1), p(2), ..., p(9) 중에서
모든 i에 대해 |p(i) - i| > 1 을 만족하는 (즉, p(i) != i 이고 p(i) != i±1 인) 순열의 개수를 구하시오.""",
    fmt="""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <개수>
예: ANSWER: 1234""",
    truth="15702",
)

TASKS["x_knapsack"] = dict(
    domain="Optimization (grind)",
    question=r"""배낭의 최대 적재 무게는 100입니다. 다음 10개 물건 중 일부를 골라(각 물건은 0개 또는 1개만) 넣을 때,
무게 합이 100 이하이면서 가치 합이 최대가 되도록 하시오. (무게, 가치):
(31,44), (10,12), (20,31), (19,25), (4,8), (3,5), (6,9), (25,30), (41,52), (14,18)
달성 가능한 최대 가치 합을 구하시오.""",
    fmt="""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: <최대 가치>
예: ANSWER: 123""",
    truth="140",
)

TASKS["x_premise"] = dict(
    domain="False Premise Audit",
    question=r"""방정식 x^4 - 5x^2 + 4 = 0 의 **유일한 실근**을 구하시오.""",
    fmt="""응답의 맨 마지막 줄에 반드시 다음 한 줄 형식으로 정답을 출력하시오(다른 설명 없이):
ANSWER: count=<실근의 개수>; roots=<모든 실근을 쉼표로 구분>
예: ANSWER: count=1; roots=2""",
    truth="count=4; roots=-2,-1,1,2",
)

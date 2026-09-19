# Prompt Version 1: Naive CoT (기초 단계별 사고 유도)
# Prompt Version 1: Naive CoT (Classic Step-by-Step)

## 개요
가장 단순하고 널리 사용되는 전통적인 Chain-of-Thought 기법입니다.  
모델에게 "단계별로 생각하라(Think step by step)"는 지시를 내려 추론을 유도합니다.
## Overview
This is the baseline classical Chain-of-Thought (CoT) prompting strategy.  
It instructs the model to "think step by step" in an unstructured, linear manner.

---

## 시스템 프롬프트 (System Prompt)
## System Prompt (English)

```markdown
당신은 논리적이고 정확한 AI 어시스턴트입니다.
모든 복잡한 질문에 답할 때는 서두르지 말고, 단계별로 차근차근 생각(Think step by step)하여 최종 정답을 도출하세요.
각 단계를 명확히 설명하면서 최종 결론에 도달하세요.
You are a precise, logical AI assistant.
When answering complex, analytical, or multi-step questions, do not rush. Think step by step to derive your final answer.
Explain each intermediate step clearly before reaching your final conclusion.
If the user asks in a language other than English (e.g., Korean), keep your reasoning in English or the query language and provide the final answer in the user's requested language.
```

---

## 사용자 지시 템플릿 (User Prompt Template)
## User Prompt Template

```markdown
[질문]
[Question]
{QUESTION}

위 문제에 대해 단계별로 생각하여 상세한 풀이 과정과 함께 정답을 제시해 주세요.
Please think step by step, provide your detailed reasoning process, and give the final answer.
```

---

## 설계 의도 및 예상 한계점
1. **설계 의도**: 단순 지시만으로도 모델의 급발진(System 1 Fast Thinking)을 억제하고 중간 추론 토큰 생성을 유도함.
2. **예상 한계점**:
   - **구조화 부재**: 생각이 비정형적으로 나열되어 중요한 제약조건을 건너뛰기 쉬움.
   - **조기 확증 편향(Confirmation Bias)**: 초반 단계에서 잘못된 가정을 세우면 중간에 의심하지 않고 그 오답을 정당화하는 방향으로 논리를 전개함.
   - **역산/반례 검증 부재**: 결론을 내린 후 검산이나 다른 가능성(Alternative Paths)을 전혀 검토하지 않음.

## Engineering Rationale & Observed Vulnerabilities
1. **Rationale**: Encourages token generation prior to the final answer, reducing immediate System 1 reflex errors.
2. **Key Weaknesses**:
   - **Premature Convergence**: Stops at the first seemingly plausible candidate without searching alternative branches.
   - **Linear Error Propagation**: An early miscalculation or flawed assumption cascades through subsequent steps without verification.
   - **Lack of Formal Verification**: Does not perform plug-in reverse validation against original constraints.

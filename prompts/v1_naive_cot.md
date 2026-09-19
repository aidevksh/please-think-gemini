# Prompt Version 1: Naive CoT (Classic Step-by-Step)

## Overview
This is the baseline classical Chain-of-Thought (CoT) prompting strategy.  
It instructs the model to "think step by step" in an unstructured, linear manner.

---

## System Prompt (English)

```markdown
You are a precise, logical AI assistant.
When answering complex, analytical, or multi-step questions, do not rush. Think step by step to derive your final answer.
Explain each intermediate step clearly before reaching your final conclusion.
If the user asks in a language other than English (e.g., Korean), keep your reasoning in English or the query language and provide the final answer in the user's requested language.
```

---

## User Prompt Template

```markdown
[Question]
{QUESTION}

Please think step by step, provide your detailed reasoning process, and give the final answer.
```

---

## Engineering Rationale & Observed Vulnerabilities
1. **Rationale**: Encourages token generation prior to the final answer, reducing immediate System 1 reflex errors.
2. **Key Weaknesses**:
   - **Premature Convergence**: Stops at the first seemingly plausible candidate without searching alternative branches.
   - **Linear Error Propagation**: An early miscalculation or flawed assumption cascades through subsequent steps without verification.
   - **Lack of Formal Verification**: Does not perform plug-in reverse validation against original constraints.

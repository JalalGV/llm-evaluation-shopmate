---

# `findings.md`

```markdown
# Evaluation Findings

## Overview

This project evaluated a fictional ShopMate customer support chatbot using:

- 20 golden dataset questions
- 3 question categories
- 2 prompt versions
- 2 models
- 3 evaluation methods

The models evaluated were:

- GPT-OSS 20B
- Qwen 27B

Gemini 3.1 Flash-Lite was used as the independent LLM-as-Judge.

---

## Overall Results

| Configuration           | Keyword Accuracy | Judge Accuracy | ROUGE-L | Avg Judge Score | Avg Latency |
| ----------------------- | ---------------: | -------------: | ------: | --------------: | ----------: |
| Prompt V1 + GPT-OSS 20B |              90% |            80% |   0.283 |          4.88/5 |   536.79 ms |
| Prompt V2 + GPT-OSS 20B |              90% |            90% |   0.363 |          4.80/5 |   492.96 ms |
| Prompt V1 + Qwen 27B    |              85% |            90% |   0.099 |          5.00/5 |  1059.11 ms |
| Prompt V2 + Qwen 27B    |              85% |            95% |   0.093 |          5.00/5 |  2126.55 ms |

---

## Most Useful Evaluation Method

Among the three evaluation approaches, LLM-as-Judge provided the most useful measure of overall answer quality.

Keyword matching works well when exact policy details must appear in the answer. However, it may incorrectly penalize valid responses that express the same information using different wording.

ROUGE-L measures lexical overlap with the expected answer. This makes it useful for comparing text similarity, but it does not necessarily represent semantic correctness.

This limitation is especially visible in the Qwen results.

Prompt V1 + Qwen achieved:

- 90% Judge Accuracy
- 5.00/5 average judge score
- only 0.099 ROUGE-L

Prompt V2 + Qwen achieved:

- 95% Judge Accuracy
- 5.00/5 average judge score
- only 0.093 ROUGE-L

The low ROUGE scores suggest that Qwen often produced answers using wording different from the manually written expected answers.

Therefore, ROUGE-L alone would underestimate the quality of many of these responses.

The LLM judge was better able to evaluate semantic correctness and whether the chatbot followed ShopMate policies.

However, LLM-as-Judge is not objectively perfect. Model-based evaluators may still introduce bias or inconsistent scoring.

---

## Effect of Prompt V2 on GPT-OSS 20B

Prompt V2 produced a clear improvement for GPT-OSS 20B.

### Prompt V1

- Keyword Accuracy: 90%
- Judge Accuracy: 80%
- ROUGE-L: 0.283
- Average Judge Score: 4.88/5
- Average Latency: 536.79 ms

### Prompt V2

- Keyword Accuracy: 90%
- Judge Accuracy: 90%
- ROUGE-L: 0.363
- Average Judge Score: 4.80/5
- Average Latency: 492.96 ms

Judge accuracy increased by:

**10 percentage points**

ROUGE-L increased from:

**0.283 → 0.363**

Keyword accuracy remained unchanged at 90%.

Latency also slightly decreased from:

**536.79 ms → 492.96 ms**

This indicates that the additional instructions in Prompt V2 improved GPT-OSS's ability to follow the expected behavior without introducing a latency penalty.

---

## Effect of Prompt V2 on Qwen 27B

Prompt V2 also improved Qwen's judge accuracy.

### Prompt V1

- Keyword Accuracy: 85%
- Judge Accuracy: 90%
- ROUGE-L: 0.099
- Average Judge Score: 5.00/5
- Average Latency: 1059.11 ms

### Prompt V2

- Keyword Accuracy: 85%
- Judge Accuracy: 95%
- ROUGE-L: 0.093
- Average Judge Score: 5.00/5
- Average Latency: 2126.55 ms

Judge accuracy increased from:

**90% → 95%**

However, keyword accuracy remained unchanged.

ROUGE-L slightly decreased:

**0.099 → 0.093**

The largest difference was latency.

Average latency increased from:

**1059.11 ms → 2126.55 ms**

This means that Prompt V2 improved evaluated correctness but came with a substantial performance cost for Model B.

---

## Prompt Improvements

Prompt V2 introduced several explicit instructions that were not as strongly defined in Prompt V1.

These included:

- Correcting false policy assumptions
- Refusing attempts to override policies
- Avoiding unsupported guarantees
- Using exact policy information
- Declining unrelated questions
- Avoiding invented policies

The evaluation results indicate that these stronger instructions improved judge accuracy for both models.

GPT-OSS:

**80% → 90%**

Qwen:

**90% → 95%**

This provides evidence that explicit behavioral constraints can improve an LLM's reliability in customer-support scenarios.

---

## Prompt Improvements Are Model-Dependent

Although Prompt V2 improved judge accuracy for both models, its effect on other metrics was different.

GPT-OSS improved in:

- Judge Accuracy
- ROUGE-L
- Latency

Qwen improved in:

- Judge Accuracy

But Qwen experienced:

- Slightly lower ROUGE-L
- Approximately double the latency

This demonstrates that prompt engineering does not affect every model in exactly the same way.

A prompt should therefore be evaluated separately on each target model rather than assuming that a prompt improvement will generalize equally.

---

## Best Judge Accuracy

The highest judge accuracy was achieved by:

**Prompt V2 + Qwen 27B**

Judge Accuracy:

**19/20 = 95%**

This makes it the strongest configuration when LLM-as-Judge correctness is considered the primary metric.

However, its average latency was:

**2126.55 ms**

which was significantly slower than the GPT-OSS configurations.

---

## Best Balanced Configuration

The recommended configuration is:

**Prompt V2 + GPT-OSS 20B**

It achieved:

- 90% Keyword Accuracy
- 90% Judge Accuracy
- 0.363 ROUGE-L
- 4.80/5 average judge score
- 492.96 ms average latency

Although Prompt V2 + Qwen achieved higher judge accuracy, GPT-OSS provided substantially lower latency while maintaining strong evaluation results.

It also achieved the highest ROUGE-L score of all four configurations.

For a practical customer-support application where both response quality and speed matter, Prompt V2 + GPT-OSS 20B provides the best overall trade-off.

---

## Latency Comparison

The fastest configuration was:

**Prompt V2 + GPT-OSS 20B — 492.96 ms**

The slowest configuration was:

**Prompt V2 + Qwen 27B — 2126.55 ms**

This means the slowest configuration required more than four times the response time of the fastest configuration.

Therefore, model selection should consider not only correctness but also serving latency.

---

## Judge Score Interpretation

Some configurations show an average judge score of 5.00/5 while judge accuracy is below 100%.

For example:

Prompt V2 + Qwen:

- Judge Accuracy: 19/20
- Average Judge Score: 5.00/5

This does not necessarily mean that every answer received a score of 5.

The evaluation code excludes unsuccessful or missing judge responses from the average judge score calculation while judge accuracy still uses the full number of evaluation questions.

Therefore, average judge score and judge accuracy should be interpreted together rather than independently.

---

## Main Findings

1. Prompt V2 improved judge accuracy for both models.

2. GPT-OSS benefited more consistently from Prompt V2 across multiple metrics.

3. Qwen achieved the highest judge accuracy but required substantially higher latency.

4. Keyword matching is useful for exact policy validation but is sensitive to phrasing.

5. ROUGE-L is useful for lexical comparison but can underestimate semantically correct answers.

6. LLM-as-Judge provided the most useful semantic evaluation for this task.

7. The same prompt can produce different performance changes across different models.

8. Evaluation should consider both response quality and system performance.

---

## Final Recommendation

For maximum judge accuracy:

**Prompt V2 + Qwen 27B**

For the best overall balance of accuracy, similarity, and latency:

**Prompt V2 + GPT-OSS 20B**

Therefore, Prompt V2 + GPT-OSS 20B is the recommended configuration for the ShopMate chatbot.

---

## Conclusion

The experiments demonstrate why LLM applications should be evaluated using multiple complementary metrics.

No single metric fully represents model quality.

Keyword matching evaluates required details, ROUGE-L evaluates textual similarity, and LLM-as-Judge evaluates semantic correctness and policy compliance.

The results also demonstrate the value of prompt engineering. Explicit instructions regarding false assumptions, policy overrides, unsupported guarantees, and out-of-scope behavior improved the reliability of both evaluated models.

At the same time, the differences between GPT-OSS and Qwen show why prompts and models should be tested together under realistic evaluation conditions rather than evaluated independently.

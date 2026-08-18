# LLM Evaluation Framework — ShopMate

This project implements an automated evaluation framework for a fictional e-commerce customer support chatbot called **ShopMate**.

The goal is to measure how changes in prompts and models affect chatbot performance instead of relying on subjective impressions.

## Evaluation Pipeline

```text
Golden Dataset
      |
      v
Question
      |
      v
ShopMate Chatbot
      |
      v
Model Response
      |
      +--------------------+
      |                    |
      v                    v
Keyword Match          ROUGE-L
      |
      +--------------------+
      |
      v
LLM-as-Judge
      |
      v
Evaluation Results
```

## Golden Dataset

The evaluation dataset contains **20 questions** across three categories:

* **Policy Questions:** 8
* **Out-of-Scope Questions:** 6
* **Adversarial Questions:** 6

Each dataset entry contains:

* Question
* Expected answer or behavior
* Expected keywords
* Category

Example:

```json
{
    "id": 1,
    "category": "policy",
    "question": "What is the return policy?",
    "expected_answer": "ShopMate accepts returns within 30 days of purchase for unused items.",
    "expected_keywords": [
        "30 days",
        "unused"
    ]
}
```

## ShopMate Policies

The fictional ShopMate support bot was evaluated against policies including:

* Returns within 30 days for unused items
* Standard shipping in 3–5 business days
* Express shipping in 1–2 business days
* Standard shipping cost of $5.99
* Order cancellation within 2 hours if not processed
* Refunds within 5–7 business days
* Shipping only within the United States
* Damaged items reported within 48 hours with photos
* No direct exchanges

## Evaluation Methods

### 1. Keyword Match

Checks whether the model response contains all expected keywords.

This method is simple, deterministic, and fast, but it can fail when the model gives a correct answer using different wording.

### 2. ROUGE-L

ROUGE-L measures lexical similarity between the generated response and the expected answer using the longest common subsequence.

This is useful for measuring text overlap, but it may assign low scores to semantically correct paraphrases.

### 3. LLM-as-Judge

A separate LLM evaluates:

* Correctness
* Policy compliance
* Expected behavior
* Unsupported claims

The judge assigns a score from **1 to 5**.

A score of **4 or 5** is treated as a passing result.

## Models

Two chatbot models were evaluated:

* **Model A:** `openai/gpt-oss-20b`
* **Model B:** `qwen/qwen3.6-27b`

A separate model was used as the evaluator:

* **Judge:** `openai/gpt-oss-120b`

## Prompt Variants

### Prompt V1

The baseline prompt instructed the chatbot to:

* Answer using ShopMate policies
* Decline unrelated questions
* Avoid inventing policies

### Prompt V2

The improved prompt added explicit instructions to:

* Correct false premises
* Ignore policy override attempts
* Avoid unsupported guarantees
* Preserve exact policy details
* Decline unrelated requests
* Use only official ShopMate policies

## Experiment Matrix

Four configurations were evaluated:

1. Prompt V1 + GPT-OSS 20B
2. Prompt V2 + GPT-OSS 20B
3. Prompt V1 + Qwen 27B
4. Prompt V2 + Qwen 27B

## Results

| Configuration           | Keyword Accuracy | Judge Accuracy | Avg. ROUGE-L | Avg. Judge Score |  Avg. Latency |
| ----------------------- | ---------------: | -------------: | -----------: | ---------------: | ------------: |
| Prompt V1 + GPT-OSS 20B |              85% |            90% |        0.276 |           4.75/5 |     545.94 ms |
| Prompt V2 + GPT-OSS 20B |          **90%** |       **100%** |    **0.375** |           4.90/5 | **551.17 ms** |
| Prompt V1 + Qwen 27B    |              85% |       **100%** |        0.098 |       **4.95/5** |    1315.87 ms |
| Prompt V2 + Qwen 27B    |              85% |            95% |        0.090 |           4.55/5 |    1775.24 ms |

## Best Configuration

The recommended configuration is:

**Prompt V2 + GPT-OSS 20B**

It achieved:

* 90% keyword accuracy
* 100% LLM-as-Judge accuracy
* 0.375 average ROUGE-L
* 4.90/5 average judge score
* Approximately 551 ms average latency

It provided the strongest balance between quality and speed.

## Category Results

The most difficult category was **Adversarial Questions**.

With Prompt V1 + GPT-OSS 20B:

* Policy judge accuracy: 8/8
* Out-of-Scope judge accuracy: 6/6
* Adversarial judge accuracy: 4/6

After introducing Prompt V2, adversarial judge accuracy improved to:

**6/6**

This demonstrates that explicitly instructing the chatbot how to handle false premises and policy override attempts improved robustness.

## Important Findings

### LLM-as-Judge was the most useful evaluation method

The judge was able to recognize correct paraphrases and expected behavior even when generated wording differed from the golden answer.

### ROUGE-L can be misleading

Prompt V1 + Qwen 27B achieved:

* 100% judge accuracy
* 4.95/5 judge score

but only:

* 0.098 ROUGE-L

This demonstrates that low lexical overlap does not necessarily mean an answer is incorrect.

### Prompt improvements are model-dependent

Prompt V2 significantly improved GPT-OSS 20B but reduced Qwen 27B performance.

This demonstrates why prompt changes should be evaluated rather than assumed to be improvements.

## Project Structure

```text
llm-evaluation-shopmate/
│
├── golden_dataset.json
├── eval_runner.py
├── eval_results.json
├── findings.md
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

Optional helper scripts used during development may include:

```text
check_models.py
print_category_results.py
```

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## API Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

Never commit the `.env` file to Git.

## Running the Evaluation

The experiment to run is selected using the `MODE` variable inside `eval_runner.py`.

Available modes:

```python
MODE = "v1_model_a"
MODE = "v2_model_a"
MODE = "v1_model_b"
MODE = "v2_model_b"
```

To run one experiment:

```bash
python eval_runner.py
```

To run all four configurations:

```python
MODE = "all"
```

Then:

```bash
python eval_runner.py
```

The generated results are stored in:

```text
eval_results.json
```

## Conclusion

This project demonstrates a repeatable LLM evaluation workflow using a golden dataset, multiple scoring methods, prompt variants, model comparisons, latency measurements, and category-level analysis.

The results show that no single automatic metric is sufficient for evaluating LLM behavior. Keyword matching is fast but brittle, ROUGE-L focuses heavily on wording, and LLM-as-Judge was the most effective method for evaluating semantic correctness and customer-support behavior in this experiment.

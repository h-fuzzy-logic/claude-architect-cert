---
paths:
  - "d4_prompts/**/*.py"
  - "d5_context/**/*.py"
---

# Eval and prompt pipeline rules

- Every eval dataset must include a metadata block: behavior_tested, model_tested, date, n_samples
- Validation-retry loops must have a max_retries param (default 3) and log each failure reason
- Never aggregate accuracy only — always track per-category breakdown to catch masked failures
- Human review flags go into a separate flagged_for_review.jsonl alongside results
- Dataset generation prompts must include at minimum 3 few-shot examples
- Generator and reviewer passes must always use separate sessions — same-session review is an anti-pattern
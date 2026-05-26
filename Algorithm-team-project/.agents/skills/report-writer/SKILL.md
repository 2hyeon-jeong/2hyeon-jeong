---
name: report-writer
description: Turn benchmark results and meeting decisions into concise report-ready Korean project documentation.
---

# Report Writer

## When To Use

Use this skill when writing report sections, meeting notes, experiment explanations, or result interpretation.

## Report Priorities

- Explain the baseline trivial algorithm first.
- Explain why optimized algorithms are compared against the baseline.
- Make clear that `my genome` is the gold standard.
- Do not claim real human genome reconstruction if synthetic `A/T/C/G` data was used.
- Keep meeting notes concise unless the user asks for expanded prose.

## Useful Wording

Baseline:

```text
trivial algorithm은 모든 위치를 직접 비교하는 단순한 기준 알고리즘으로 사용하였다.
```

Gold standard:

```text
reference genome에 synthetic mutation을 추가하여 my genome을 생성하고, 이를 gold standard로 사용하였다.
```

Experiment:

```text
동일한 read set에 대해 각 알고리즘을 실행하고, 정확도와 실행 시간을 비교하였다.
```


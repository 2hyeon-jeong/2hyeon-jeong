# DNA Read Reconstruction Team Spec

## Goal

Build a reusable workflow for the team project that compares DNA string-search algorithms using synthetic data.

Final algorithms are implemented in C++. Python remains the testing and experiment environment.

## Current Context

- The project compares algorithms for mapping noisy short reads to a reference genome.
- Data is synthetic: random `A/T/C/G`, not real human genome data.
- Professor feedback requires a trivial baseline and evaluation against a gold standard.
- The final experiment should generate `my genome` from a reference and sample noisy reads from `my genome`.

## Team Assignments

| Member | Algorithm |
| --- | --- |
| 정이현 | KMP |
| 김태훈 | Suffix Array + Binary Search |
| 김준서 | BWT |
| 이주환 | Dictionary / position-table search |

## Architecture Pattern

Use a Pipeline with Fan-out/Fan-in:

1. Shared experiment contract is defined.
2. Team members implement algorithms independently.
3. Algorithms are integrated into the common benchmark.
4. Results are collected into CSV and figures.
5. Report text compares each algorithm against the trivial baseline.

## Handoff Files

| File | Purpose |
| --- | --- |
| `_workspace/team/tasks.md` | Shared task list and ownership |
| `_workspace/team/status.md` | Progress notes, validation commands, and result summaries |
| `_workspace/team/algorithm-template.md` | Required notes for each algorithm |

## Algorithm Contract

Each algorithm should document:

- input format
- output format
- preprocessing/index construction
- search method
- extension or mismatch verification method
- expected time complexity
- expected weakness under noise

For C++ integration, use this executable protocol:

```text
stdin:
reference
read_count
read_1
read_2
...

stdout:
reconstructed_sequence
```

Python prototype algorithms may still use `reconstruct(reads, reference=None)`.
Compiled C++ executables under `build/algorithms/` are auto-registered with the `cpp_` prefix.

## Experiment Contract

Final evaluation should use:

```text
reference genome
  -> mutation
  -> my genome = gold standard
  -> noisy reads
```

Algorithms receive:

- reference genome
- noisy reads

Metrics compare output against:

- `my genome`, not the reference genome

## Validation

Run before merging benchmark or integration work:

```powershell
.\.venv\Scripts\python.exe -m unittest discover tests
```

Run for smoke benchmark validation:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
```

## Failure Policy

- If an optimized algorithm is inaccurate, compare it to trivial baseline and document the tradeoff.
- If a C++ implementation is not integrated yet, provide a clear input/output example and complexity analysis.
- If a result uses `reference_accuracy` instead of `accuracy`, label it as reference comparison and do not use it as final gold-standard accuracy evidence.

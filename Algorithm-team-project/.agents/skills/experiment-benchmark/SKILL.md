---
name: experiment-benchmark
description: Maintain the Python experiment harness for synthetic DNA generation, benchmark runs, metrics, and graph outputs.
---

# Experiment Benchmark

## When To Use

Use this skill when changing or running the Python test and experiment environment.

This includes:

- generating reference genome, my genome, and noisy reads
- changing coverage, noise rate, read count, or genome length
- running all registered algorithms on the same dataset
- writing CSV result files
- generating accuracy/runtime graphs

## Experiment Contract

The final report should use a gold standard:

```text
reference genome -> mutated my genome -> noisy reads
```

Evaluate reconstructed output against `my genome`.

Keep variables controlled. Change one main independent variable at a time:

- coverage
- read count
- noise rate
- genome length

Primary metrics:

- accuracy
- runtime
- mismatch count
- reconstructed length

## Commands

Run tests:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m unittest discover tests
```

Run smoke benchmark:

```powershell
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
```

Generate figures:

```powershell
.\.venv\Scripts\python.exe -m src.visualization.plot_results
```

## Handoff

Write result notes to `_workspace/team/status.md`:

- benchmark command
- changed variables
- CSV path
- figure path
- brief interpretation

---
name: experiment-benchmark
description: Maintain the Python experiment harness for synthetic DNA generation, benchmark runs, metrics, and graph outputs.
---

# Experiment Benchmark

Use this skill when changing or running the Python test and experiment environment.

Final report evaluation should use:

```text
reference genome -> mutated my genome -> noisy reads
```

Evaluate reconstructed output against `my genome`.

Commands:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m unittest discover tests
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
.\.venv\Scripts\python.exe -m src.visualization.plot_results
```

Write result notes to `_workspace/team/status.md`.

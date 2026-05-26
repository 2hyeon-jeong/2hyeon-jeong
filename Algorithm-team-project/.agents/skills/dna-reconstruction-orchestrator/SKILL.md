---
name: dna-reconstruction-orchestrator
description: Coordinate the DNA read reconstruction team workflow across C++ algorithm implementation, Python benchmarking, graph generation, and report writing.
---

# DNA Reconstruction Orchestrator

## When To Use

Use this skill when coordinating the team project for synthetic DNA read reconstruction algorithm comparison.

Use it for:

- assigning or checking algorithm implementation work
- integrating C++ algorithms into the Python benchmark environment
- updating benchmark variables, metrics, or result graphs
- preparing report material from experiment results
- making sure the trivial baseline and gold-standard evaluation are preserved

## Project Contract

The final algorithm implementations should be written in C++.
Python is the experiment harness for dataset generation, benchmarking, CSV output, graph generation, and lightweight validation.

The intended final experiment flow is:

```text
reference genome
  -> synthetic mutation
  -> my genome = gold standard
  -> noisy reads from my genome
  -> algorithms use reference genome + reads
  -> reconstructed genome
  -> compare reconstructed genome with my genome
```

Do not treat the reference genome as the final answer when reporting accuracy.

## Roles

- Algorithm implementer: owns one C++ search/reconstruction algorithm.
- Experiment engineer: owns Python dataset generation, benchmark execution, and metric collection.
- Visualization/report writer: owns figures, result interpretation, and report text.
- Integrator/reviewer: checks interface consistency and verifies results against the gold standard.

## Workflow

1. Confirm the task in `docs/harness/dna-read-reconstruction/team-spec.md`.
2. Check current work items in `_workspace/team/tasks.md`.
3. For algorithm work, create or update one C++ implementation and its integration wrapper.
4. For experiment work, keep Python benchmark inputs identical across algorithms.
5. Run tests and a small benchmark before marking a task done.
6. Record findings, commands, and result paths in `_workspace/team/status.md`.

## Required Validation

Before finalizing algorithm or benchmark changes:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m unittest discover tests
```

For benchmark changes, also run a small smoke benchmark:

```powershell
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
```

## Output Expectations

Leave enough handoff context for the next teammate:

- what changed
- how it was tested
- which algorithm or experiment variable it affects
- whether accuracy is compared against `my genome` or only against the old reference-based setup

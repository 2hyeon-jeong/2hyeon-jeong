---
name: dna-reconstruction-orchestrator
description: Coordinate the DNA read reconstruction team workflow across C++ algorithm implementation, Python benchmarking, graph generation, and report writing.
---

# DNA Reconstruction Orchestrator

Use this skill when coordinating the team project for synthetic DNA read reconstruction algorithm comparison.

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

Workflow:

1. Confirm the task in `docs/harness/dna-read-reconstruction/team-spec.md`.
2. Check current work items in `_workspace/team/tasks.md`.
3. For algorithm work, create or update one C++ implementation and its integration wrapper.
4. For experiment work, keep Python benchmark inputs identical across algorithms.
5. Run tests and a small benchmark before marking a task done.
6. Record findings, commands, and result paths in `_workspace/team/status.md`.

Required validation:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m unittest discover tests
```

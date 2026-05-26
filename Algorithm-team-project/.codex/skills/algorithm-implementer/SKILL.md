---
name: algorithm-implementer
description: Implement and validate one DNA read search algorithm for the team project, keeping the C++ algorithm and Python benchmark interface compatible.
---

# Algorithm Implementer

Use this skill when implementing or reviewing one of the assigned algorithms:

- KMP
- Suffix Array + Binary Search
- BWT/FM-index
- dictionary or position-table based search
- trivial exhaustive baseline

Rules:

- Implement final algorithms in C++.
- Keep Python as the benchmark/test environment.
- Preserve the C++ stdin/stdout contract in `AGENTS.md`: algorithms receive a reference and reads, then print one reconstructed DNA string.
- The trivial exhaustive algorithm is the baseline.
- Prefer seed-and-extend when exact full-read matching is too fragile under read noise.
- If using an index, separate index construction time and search/reconstruction time when possible.

Handoff notes go to `_workspace/team/status.md`.

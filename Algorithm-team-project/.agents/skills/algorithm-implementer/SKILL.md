---
name: algorithm-implementer
description: Implement and validate one DNA read search algorithm for the team project, keeping the C++ algorithm and Python benchmark interface compatible.
---

# Algorithm Implementer

## When To Use

Use this skill when implementing or reviewing one of the assigned algorithms:

- KMP
- Suffix Array + Binary Search
- BWT/FM-index
- dictionary or position-table based search
- trivial exhaustive baseline

## Rules

- Implement final algorithms in C++.
- Keep Python as the benchmark/test environment.
- Preserve the C++ stdin/stdout contract in `AGENTS.md`: algorithms receive a reference and reads, then print one reconstructed DNA string.
- The trivial exhaustive algorithm is the baseline, not the optimized method.
- Prefer seed-and-extend when exact full-read matching is too fragile under read noise.
- If using an index, separate index construction time and search/reconstruction time when possible.

## Implementation Checklist

1. State the algorithm name and expected complexity.
2. Define the input and output format.
3. Build or reuse an index only from the reference genome.
4. Match reads or read seeds against the reference.
5. Extend/verify candidate positions by counting mismatches over the full read.
6. Produce placements that can be converted into a consensus reconstruction.
7. Add a small deterministic test case.
8. Record limitations, especially behavior under noisy reads.

## Handoff

Write short notes to `_workspace/team/status.md`:

- algorithm implemented
- files changed
- command used for validation
- observed runtime/accuracy on a small benchmark
- known failure cases

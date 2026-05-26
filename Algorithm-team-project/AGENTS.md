# Project Guidance

## What This Project Is

This repository is an algorithm class team assignment for comparing string-search algorithms in DNA read reconstruction using synthetic data, not real human genome data.

Final algorithm implementations are intended to be written in C++. Python is used for the testing and experiment environment: synthetic data generation, benchmark orchestration, result CSV creation, graph generation, and lightweight validation scripts.

The current project generates random DNA strings with the alphabet `A/T/C/G`, mutates a reference into `my genome`, samples short reads of length 30 to 45 from `my genome`, adds mismatch noise, runs multiple reconstruction/search algorithms, and compares accuracy and runtime against `my genome`.

Professor feedback on 2026-05-14 clarified the intended experiment:

- Use one trivial algorithm as the baseline.
- Compare optimized algorithms against that trivial baseline.
- Evaluate against a gold standard.
- Bring or generate only a reference genome; create `my genome` and reads ourselves.

The intended final data flow is:

```text
reference genome
  -> add synthetic mutations
  -> my genome = gold standard
  -> sample noisy reads from my genome
  -> algorithms use reference genome + reads
  -> reconstructed genome
  -> compare reconstructed genome with my genome
```

The implementation now has explicit `my genome` / gold-standard separation in `src/data/generator.py` and `src/evaluation/benchmark.py`. Keep final accuracy based on `my genome`, not the reference.

## Repository Layout

- `cpp/algorithms/`: final C++ algorithm implementations.
- `scripts/build_cpp.py`: compiles C++ algorithms into `build/algorithms/`.
- `src/algorithms/`: Python prototype algorithms and C++ executable wrappers.
- `src/data/generator.py`: synthetic reference, my genome, and read generation.
- `src/evaluation/benchmark.py`: runs all registered algorithms and writes CSV results.
- `src/evaluation/metrics.py`: accuracy and mismatch metrics.
- `src/visualization/plot_results.py`: generates accuracy/runtime graphs.
- `tests/`: unit tests for generators, Python algorithms, and C++ runner protocol.
- `experiments/results/`: benchmark CSV outputs.
- `experiments/figures/`: generated graph outputs.
- `docs/harness/dna-read-reconstruction/`: collaboration harness and team workflow docs.
- `_workspace/team/`: shared task list, status notes, and algorithm handoff template.
- `report/`: report draft material.

## Algorithm Rules

Final algorithms should be implemented in C++ under `cpp/algorithms/`.

C++ algorithms must follow this stdin/stdout protocol:

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

Python prototype algorithms may expose this interface:

```python
def reconstruct(reads: list[str], reference: str | None = None) -> str:
    ...
```

Rules:

- Return or print exactly one reconstructed DNA sequence.
- Do not print large logs during benchmark runs.
- Do not mutate the input `reads` list or `reference` string.
- If a Python prototype requires a reference, raise `ValueError` when `reference is None`.
- Register Python algorithms in `src/algorithms/__init__.py` inside `ALGORITHMS`.
- C++ executables in `build/algorithms/` are auto-registered with the `cpp_` prefix.
- Keep algorithm names stable because CSV and graphs use those keys.

Current registered Python algorithms:

- `trivial_reference`
- `position_table_index`
- `kmer_index`
- `bwt_index`
- `greedy_overlap`
- `debruijn_graph`

Current C++ baseline:

- `cpp_trivial_baseline` after running `scripts/build_cpp.py`

Current team assignment as of 2026-05-19:

- 정이현: KMP
- 김태훈: Suffix Array + Binary Search
- 김준서: BWT
- 이주환: dictionary / position-table based search

## Experiment Rules

Use the same generated dataset for every algorithm in a benchmark run. The main independent variables should be one at a time, such as:

- coverage
- read count
- noise rate
- genome mutation rate
- reference/genome length

Primary dependent variables:

- accuracy against `my_genome`
- runtime
- mismatch count
- reconstructed length
- reference accuracy for sanity checking only

For the final report, prefer comparing optimized algorithms to the trivial baseline, for example:

```text
trivial exhaustive search vs KMP / suffix array / BWT / dictionary table
```

Reference-based algorithms may show artificially high accuracy if the reference is also used as the answer. The benchmark writes both `accuracy` against `my_genome` and `reference_accuracy` against the reference so this difference stays visible.

## Commands

Use C++ for final algorithm implementations. Use Python 3.8.2 with the project virtual environment for testing, benchmarking, dataset generation, and visualization.

Windows PowerShell setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Build C++ algorithms:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover tests
```

Run a benchmark:

```powershell
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
```

Generate graphs:

```powershell
.\.venv\Scripts\python.exe -m src.visualization.plot_results
```

## Git and Team Workflow

Use simple team branches instead of `feat/` branches:

```text
main
dev
member/<name>
```

Commit prefixes:

- `alg:` algorithm implementation
- `data:` dataset generation
- `exp:` benchmark code or results
- `viz:` graph generation
- `docs:` report or README changes
- `fix:` bug fix
- `refactor:` structure cleanup

Do not commit `.venv/`, `build/`, `__pycache__/`, or other generated cache files.


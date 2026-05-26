# Random DNA Read Reconstruction Benchmark

This project compares string-processing algorithms for reconstructing a synthetic personal DNA sequence from noisy short reads.

The project does not use real genome data. It generates a random reference from `A`, `T`, `C`, and `G`, mutates it into `my genome`, samples reads of length 30 to 45 from `my genome`, adds mismatch noise, and benchmarks reconstruction algorithms by accuracy and runtime. `my genome` is the gold standard.

Final algorithm implementations are written in C++. Python is used for dataset generation, benchmark orchestration, CSV output, graph generation, and tests.

```text
reference genome
  -> synthetic mutation
  -> my genome = gold standard
  -> noisy reads from my genome
  -> algorithms use reference genome + reads
  -> reconstructed genome
  -> compare reconstructed genome with my genome
```

## Algorithms

Python prototype algorithms:

- `trivial_reference`: compares every read against every reference position.
- `position_table_index`: scans the reference once and stores positions for each base, then verifies candidate alignments.
- `kmer_index`: indexes reference k-mers and verifies seed candidate positions.
- `bwt_index`: builds a BWT/FM-index from the reference and searches exact read seeds before verification.
- `greedy_overlap`: merges reads by the longest suffix-prefix overlap.
- `debruijn_graph`: builds contigs from a simple de Bruijn graph traversal.

C++ algorithms:

- `cpp_trivial_baseline`: exhaustive baseline, available after building `cpp/algorithms/trivial_baseline.cpp`.

Python prototype algorithms expose this interface:

```python
def reconstruct(reads: list[str], reference: str | None = None) -> str:
    ...
```

C++ algorithms use this stdin/stdout protocol:

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

Any `cpp/algorithms/*.cpp` file is compiled into `build/algorithms/*.exe`. Compiled executables are automatically registered in benchmark results with the `cpp_` prefix.

## Quick Start

This project currently uses Python 3.8.2 for the experiment environment and `g++` for C++ algorithms.

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the venv Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Build C++ algorithms, run tests, benchmark, and plot:

```powershell
.\.venv\Scripts\python.exe scripts\build_cpp.py
.\.venv\Scripts\python.exe -m unittest discover tests
.\.venv\Scripts\python.exe -m src.evaluation.benchmark --reference-length 1000 --repeats 1 --genome-mutation-rate 0.01
.\.venv\Scripts\python.exe -m src.visualization.plot_results
```

Benchmark CSV files are written to `experiments/results/`. Figures are written to `experiments/figures/`. If `matplotlib` is installed, PNG files are generated. Otherwise, the script generates SVG files using only the Python standard library.

## Collaboration Harness

- Read `AGENTS.md` first for project rules.
- Use `docs/harness/dna-read-reconstruction/team-spec.md` for team workflow.
- Track shared tasks in `_workspace/team/tasks.md`.
- Leave handoff notes in `_workspace/team/status.md`.
- Use `_workspace/team/algorithm-template.md` when documenting an algorithm.

## Git Strategy

Use simple team branches instead of `feat/` branches:

```text
main
dev
member/<name>
```

Commit prefixes:

```text
alg: algorithm implementation
data: dataset generator
exp: benchmark code or results
viz: graph generation
docs: report or README changes
fix: bug fix
refactor: structure cleanup
```


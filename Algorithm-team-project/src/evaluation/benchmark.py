from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from src.algorithms import ALGORITHMS
from src.data.generator import generate_experiment_dataset
from src.evaluation.metrics import (
    best_alignment_accuracy,
    mismatch_count,
    positional_accuracy,
)


def run_benchmark(
    reference_lengths: list[int],
    coverages: list[float],
    noise_rates: list[float],
    genome_mutation_rates: list[float],
    repeats: int,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    for reference_length in reference_lengths:
        for genome_mutation_rate in genome_mutation_rates:
            for noise_rate in noise_rates:
                for coverage in coverages:
                    for repeat in range(repeats):
                        seed = (
                            reference_length * 1_000_000
                            + int(genome_mutation_rate * 10_000) * 10_000
                            + int(noise_rate * 10_000) * 1_000
                            + int(coverage * 100)
                            + repeat
                        )
                        dataset = generate_experiment_dataset(
                            reference_length=reference_length,
                            coverage=coverage,
                            read_noise_rate=noise_rate,
                            genome_mutation_rate=genome_mutation_rate,
                            seed=seed,
                        )

                        for name, algorithm in ALGORITHMS.items():
                            start_time = time.perf_counter()
                            reconstructed = algorithm(dataset.reads, dataset.reference)
                            runtime = time.perf_counter() - start_time

                            rows.append({
                                "algorithm": name,
                                "reference_length": reference_length,
                                "coverage": coverage,
                                "noise_rate": noise_rate,
                                "genome_mutation_rate": genome_mutation_rate,
                                "repeat": repeat,
                                "read_count": len(dataset.reads),
                                "runtime_seconds": runtime,
                                "accuracy": best_alignment_accuracy(dataset.my_genome, reconstructed),
                                "positional_accuracy": positional_accuracy(dataset.my_genome, reconstructed),
                                "reference_accuracy": positional_accuracy(dataset.reference, reconstructed),
                                "mismatch_count": mismatch_count(dataset.my_genome, reconstructed),
                                "reconstructed_length": len(reconstructed),
                            })

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DNA reconstruction benchmarks.")
    parser.add_argument("--reference-length", type=int, nargs="+", default=[1000])
    parser.add_argument("--coverage", type=float, nargs="+", default=[1, 2, 5, 10, 20])
    parser.add_argument("--noise-rate", type=float, nargs="+", default=[0.01])
    parser.add_argument("--genome-mutation-rate", type=float, nargs="+", default=[0.01])
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/results/benchmark.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_benchmark(
        reference_lengths=args.reference_length,
        coverages=args.coverage,
        noise_rates=args.noise_rate,
        genome_mutation_rates=args.genome_mutation_rate,
        repeats=args.repeats,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()

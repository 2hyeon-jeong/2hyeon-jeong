from __future__ import annotations

import random
from dataclasses import dataclass

from src.algorithms.common import DNA_ALPHABET


@dataclass(frozen=True)
class Dataset:
    reference: str
    my_genome: str
    reads: list[str]
    read_starts: list[int]


def generate_reference(length: int, seed: int | None = None) -> str:
    rng = random.Random(seed)
    return "".join(rng.choice(DNA_ALPHABET) for _ in range(length))


def mutate_base(base: str, rng: random.Random) -> str:
    choices = [candidate for candidate in DNA_ALPHABET if candidate != base]
    return rng.choice(choices)


def add_mismatch_noise(sequence: str, noise_rate: float, rng: random.Random) -> str:
    return "".join(
        mutate_base(base, rng) if rng.random() < noise_rate else base
        for base in sequence
    )


def mutate_sequence(sequence: str, mutation_rate: float, rng: random.Random) -> str:
    """Create a synthetic personal genome from a reference genome."""
    return "".join(
        mutate_base(base, rng) if rng.random() < mutation_rate else base
        for base in sequence
    )


def read_count_for_coverage(
    reference_length: int, coverage: float, average_read_length: int = 40
) -> int:
    return max(1, round(coverage * reference_length / average_read_length))


def generate_reads(
    genome: str,
    coverage: float,
    noise_rate: float,
    min_read_length: int = 30,
    max_read_length: int = 45,
    seed: int | None = None,
) -> Dataset:
    rng = random.Random(seed)
    count = read_count_for_coverage(reference_length=len(genome), coverage=coverage)
    reads: list[str] = []
    starts: list[int] = []

    for _ in range(count):
        read_length = rng.randint(min_read_length, max_read_length)
        start = rng.randint(0, len(genome) - read_length)
        read = genome[start : start + read_length]
        reads.append(add_mismatch_noise(read, noise_rate, rng))
        starts.append(start)

    return Dataset(reference=genome, my_genome=genome, reads=reads, read_starts=starts)


def generate_experiment_dataset(
    reference_length: int,
    coverage: float,
    read_noise_rate: float,
    genome_mutation_rate: float,
    seed: int | None = None,
) -> Dataset:
    """Generate reference, gold-standard my genome, and noisy reads.

    The reference is the algorithm input. The mutated my genome is the answer
    used for final accuracy. Reads are sampled from my genome, then noisy
    mismatch errors are added.
    """
    rng = random.Random(seed)
    reference = generate_reference(reference_length, seed=rng.randint(0, 10**9))
    my_genome = mutate_sequence(reference, genome_mutation_rate, rng)
    read_dataset = generate_reads(
        my_genome,
        coverage=coverage,
        noise_rate=read_noise_rate,
        seed=rng.randint(0, 10**9),
    )
    return Dataset(
        reference=reference,
        my_genome=my_genome,
        reads=read_dataset.reads,
        read_starts=read_dataset.read_starts,
    )

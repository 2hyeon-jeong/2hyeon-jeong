from __future__ import annotations

from collections import defaultdict

from src.algorithms.common import consensus_from_alignments, hamming_distance
from src.algorithms.trivial_reference import best_position as trivial_best_position


def build_index(reference: str, k: int) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for start in range(0, len(reference) - k + 1):
        index[reference[start : start + k]].append(start)
    return dict(index)


def read_seeds(read: str, k: int) -> list[tuple[int, str]]:
    if len(read) < k:
        return [(0, read)]

    offsets = sorted({0, (len(read) - k) // 2, len(read) - k})
    return [(offset, read[offset : offset + k]) for offset in offsets]


def best_position(
    read: str, reference: str, index: dict[str, list[int]], k: int
) -> tuple[int, int]:
    candidates: set[int] = set()

    for read_offset, seed in read_seeds(read, k):
        for ref_seed_start in index.get(seed, []):
            candidate = ref_seed_start - read_offset
            if 0 <= candidate <= len(reference) - len(read):
                candidates.add(candidate)

    if not candidates:
        return trivial_best_position(read, reference)

    best_start = min(candidates)
    best_distance = len(read) + 1
    for start in candidates:
        window = reference[start : start + len(read)]
        distance = hamming_distance(read, window)
        if distance < best_distance:
            best_start = start
            best_distance = distance

    return best_start, best_distance


def reconstruct(reads: list[str], reference: str | None = None) -> str:
    if reference is None:
        raise ValueError("kmer_index requires a reference sequence")

    k = 10
    index = build_index(reference, k)
    alignments = [best_position(read, reference, index, k)[0:1] + (read,) for read in reads]
    return consensus_from_alignments(reference, alignments)


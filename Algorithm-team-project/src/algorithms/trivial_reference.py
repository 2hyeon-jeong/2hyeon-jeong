from __future__ import annotations

from src.algorithms.common import consensus_from_alignments, hamming_distance


def best_position(read: str, reference: str) -> tuple[int, int]:
    best_start = 0
    best_distance = len(read) + 1

    for start in range(0, len(reference) - len(read) + 1):
        window = reference[start : start + len(read)]
        distance = hamming_distance(read, window)
        if distance < best_distance:
            best_start = start
            best_distance = distance
            if distance == 0:
                break

    return best_start, best_distance


def reconstruct(reads: list[str], reference: str | None = None) -> str:
    if reference is None:
        raise ValueError("trivial_reference requires a reference sequence")

    alignments = [best_position(read, reference)[0:1] + (read,) for read in reads]
    return consensus_from_alignments(reference, alignments)


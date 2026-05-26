from __future__ import annotations

from collections import Counter

from src.algorithms.common import DNA_ALPHABET, consensus_from_alignments, hamming_distance
from src.algorithms.trivial_reference import best_position as trivial_best_position


def build_position_table(reference: str) -> dict[str, list[int]]:
    table = {base: [] for base in DNA_ALPHABET}
    for position, base in enumerate(reference):
        table[base].append(position)
    return table


def selected_offsets(read: str) -> list[int]:
    last = len(read) - 1
    return sorted({0, last // 4, last // 2, (last * 3) // 4, last})


def best_position(
    read: str, reference: str, table: dict[str, list[int]]
) -> tuple[int, int]:
    candidate_votes: Counter[int] = Counter()

    for offset in selected_offsets(read):
        base = read[offset]
        for position in table.get(base, []):
            start = position - offset
            if 0 <= start <= len(reference) - len(read):
                candidate_votes[start] += 1

    if not candidate_votes:
        return trivial_best_position(read, reference)

    best_start = min(candidate_votes)
    best_distance = len(read) + 1
    for start, _ in candidate_votes.most_common():
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
        raise ValueError("position_table_index requires a reference sequence")

    table = build_position_table(reference)
    alignments = [best_position(read, reference, table)[0:1] + (read,) for read in reads]
    return consensus_from_alignments(reference, alignments)


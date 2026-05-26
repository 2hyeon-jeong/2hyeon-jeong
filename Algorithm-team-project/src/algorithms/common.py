from __future__ import annotations

from collections import Counter

DNA_ALPHABET = "ATCG"


def hamming_distance(left: str, right: str) -> int:
    """Return mismatch count for equal-length strings."""
    return sum(a != b for a, b in zip(left, right))


def consensus_from_alignments(
    reference: str, alignments: list[tuple[int, str]]
) -> str:
    """Build a reference-length consensus sequence from placed reads."""
    votes = [Counter({base: 1}) for base in reference]

    for start, read in alignments:
        for offset, base in enumerate(read):
            pos = start + offset
            if 0 <= pos < len(votes):
                votes[pos][base] += 1

    return "".join(counter.most_common(1)[0][0] for counter in votes)


def suffix_prefix_overlap(left: str, right: str, min_overlap: int = 1) -> int:
    """Longest length where suffix(left) equals prefix(right)."""
    max_len = min(len(left), len(right))
    for length in range(max_len, min_overlap - 1, -1):
        if left[-length:] == right[:length]:
            return length
    return 0


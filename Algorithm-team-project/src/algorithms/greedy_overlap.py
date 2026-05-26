from __future__ import annotations

from src.algorithms.common import suffix_prefix_overlap


def reconstruct(reads: list[str], reference: str | None = None) -> str:
    remaining = [read for read in reads if read]
    if not remaining:
        return ""

    min_overlap = 15

    while len(remaining) > 1:
        best_i = -1
        best_j = -1
        best_overlap = 0

        for i, left in enumerate(remaining):
            for j, right in enumerate(remaining):
                if i == j:
                    continue
                overlap = suffix_prefix_overlap(left, right, min_overlap)
                if overlap > best_overlap:
                    best_i = i
                    best_j = j
                    best_overlap = overlap

        if best_overlap < min_overlap:
            break

        left = remaining[best_i]
        right = remaining[best_j]
        merged = left + right[best_overlap:]

        for index in sorted((best_i, best_j), reverse=True):
            remaining.pop(index)
        remaining.append(merged)

    return max(remaining, key=len)


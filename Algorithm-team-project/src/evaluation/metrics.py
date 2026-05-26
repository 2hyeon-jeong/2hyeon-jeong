from __future__ import annotations


def positional_accuracy(original: str, reconstructed: str) -> float:
    if not original or not reconstructed:
        return 0.0

    compared = min(len(original), len(reconstructed))
    matches = sum(
        original[i] == reconstructed[i]
        for i in range(compared)
    )
    return matches / max(len(original), len(reconstructed))


def best_alignment_accuracy(original: str, reconstructed: str) -> float:
    if not original or not reconstructed:
        return 0.0

    best = 0
    min_shift = -len(reconstructed) + 1
    max_shift = len(original)

    for shift in range(min_shift, max_shift):
        matches = 0
        overlap = 0
        for rec_index, base in enumerate(reconstructed):
            original_index = shift + rec_index
            if 0 <= original_index < len(original):
                overlap += 1
                if original[original_index] == base:
                    matches += 1
        if overlap:
            best = max(best, matches)

    return best / max(len(original), len(reconstructed))


def mismatch_count(original: str, reconstructed: str) -> int:
    compared = min(len(original), len(reconstructed))
    mismatches = sum(
        original[i] != reconstructed[i]
        for i in range(compared)
    )
    return mismatches + abs(len(original) - len(reconstructed))


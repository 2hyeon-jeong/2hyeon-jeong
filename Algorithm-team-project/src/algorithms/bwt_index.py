from __future__ import annotations

from dataclasses import dataclass

from src.algorithms.common import consensus_from_alignments, hamming_distance
from src.algorithms.kmer_index import read_seeds
from src.algorithms.trivial_reference import best_position as trivial_best_position


def suffix_array(text: str) -> list[int]:
    n = len(text)
    order = list(range(n))
    ranks = [ord(char) for char in text]
    step = 1

    while step < n:
        order.sort(key=lambda index: (ranks[index], ranks[index + step] if index + step < n else -1))
        new_ranks = [0] * n
        for i in range(1, n):
            previous = order[i - 1]
            current = order[i]
            previous_key = (
                ranks[previous],
                ranks[previous + step] if previous + step < n else -1,
            )
            current_key = (
                ranks[current],
                ranks[current + step] if current + step < n else -1,
            )
            new_ranks[current] = new_ranks[previous] + (previous_key != current_key)
        ranks = new_ranks
        if ranks[order[-1]] == n - 1:
            break
        step *= 2

    return order


@dataclass
class FMIndex:
    text: str
    sa: list[int]
    bwt: str
    first_occurrence: dict[str, int]
    occ: dict[str, list[int]]

    @classmethod
    def build(cls, reference: str) -> "FMIndex":
        text = reference + "$"
        sa = suffix_array(text)
        bwt = "".join(text[index - 1] if index > 0 else text[-1] for index in sa)

        alphabet = sorted(set(text))
        counts = {char: 0 for char in alphabet}
        occ = {char: [0] for char in alphabet}
        for char in bwt:
            counts[char] += 1
            for alphabet_char in alphabet:
                occ[alphabet_char].append(counts[alphabet_char])

        first_occurrence: dict[str, int] = {}
        total = 0
        for char in alphabet:
            first_occurrence[char] = total
            total += text.count(char)

        return cls(
            text=text,
            sa=sa,
            bwt=bwt,
            first_occurrence=first_occurrence,
            occ=occ,
        )

    def search(self, pattern: str) -> list[int]:
        top = 0
        bottom = len(self.bwt)

        for char in reversed(pattern):
            if char not in self.first_occurrence:
                return []
            top = self.first_occurrence[char] + self.occ[char][top]
            bottom = self.first_occurrence[char] + self.occ[char][bottom]
            if top >= bottom:
                return []

        reference_length = len(self.text) - 1
        return [
            position
            for position in self.sa[top:bottom]
            if position < reference_length
        ]


def best_position(read: str, reference: str, index: FMIndex, seed_length: int) -> tuple[int, int]:
    candidates: set[int] = set()

    for read_offset, seed in read_seeds(read, seed_length):
        for seed_start in index.search(seed):
            candidate = seed_start - read_offset
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
            if distance == 0:
                break

    return best_start, best_distance


def reconstruct(reads: list[str], reference: str | None = None) -> str:
    if reference is None:
        raise ValueError("bwt_index requires a reference sequence")

    index = FMIndex.build(reference)
    seed_length = 10
    alignments = [
        best_position(read, reference, index, seed_length)[0:1] + (read,)
        for read in reads
    ]
    return consensus_from_alignments(reference, alignments)


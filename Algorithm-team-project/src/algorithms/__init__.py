"""Reconstruction algorithm registry."""

from src.algorithms.bwt_index import reconstruct as bwt_index
from src.algorithms.cpp_external import discover_cpp_algorithms
from src.algorithms.debruijn_graph import reconstruct as debruijn_graph
from src.algorithms.greedy_overlap import reconstruct as greedy_overlap
from src.algorithms.kmer_index import reconstruct as kmer_index
from src.algorithms.position_table_index import reconstruct as position_table_index
from src.algorithms.trivial_reference import reconstruct as trivial_reference

ALGORITHMS = {
    "trivial_reference": trivial_reference,
    "position_table_index": position_table_index,
    "kmer_index": kmer_index,
    "bwt_index": bwt_index,
    "greedy_overlap": greedy_overlap,
    "debruijn_graph": debruijn_graph,
}

ALGORITHMS.update(discover_cpp_algorithms())

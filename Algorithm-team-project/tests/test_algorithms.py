import unittest

from src.algorithms.common import suffix_prefix_overlap
from src.algorithms.bwt_index import FMIndex
from src.algorithms.bwt_index import reconstruct as bwt_reconstruct
from src.algorithms.kmer_index import reconstruct as kmer_reconstruct
from src.algorithms.position_table_index import reconstruct as position_reconstruct
from src.algorithms.trivial_reference import reconstruct as trivial_reconstruct
from src.data.generator import generate_reads, generate_reference
from src.evaluation.metrics import positional_accuracy


class AlgorithmTests(unittest.TestCase):
    def test_suffix_prefix_overlap(self):
        self.assertEqual(suffix_prefix_overlap("AAATCG", "TCGGGG"), 3)
        self.assertEqual(suffix_prefix_overlap("AAAA", "TTTT"), 0)

    def test_reference_algorithms_reconstruct_small_zero_noise_dataset(self):
        reference = generate_reference(200, seed=10)
        dataset = generate_reads(reference, coverage=20, noise_rate=0.0, seed=11)

        trivial = trivial_reconstruct(dataset.reads, reference)
        position = position_reconstruct(dataset.reads, reference)
        kmer = kmer_reconstruct(dataset.reads, reference)
        bwt = bwt_reconstruct(dataset.reads, reference)

        self.assertGreaterEqual(positional_accuracy(reference, trivial), 0.95)
        self.assertGreaterEqual(positional_accuracy(reference, position), 0.95)
        self.assertGreaterEqual(positional_accuracy(reference, kmer), 0.95)
        self.assertGreaterEqual(positional_accuracy(reference, bwt), 0.95)

    def test_bwt_index_finds_seed_positions(self):
        index = FMIndex.build("BANANA")
        self.assertEqual(index.search("ANA"), [3, 1])


if __name__ == "__main__":
    unittest.main()

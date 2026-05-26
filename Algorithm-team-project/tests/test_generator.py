import unittest

from src.data.generator import generate_experiment_dataset, generate_reads, generate_reference


class GeneratorTests(unittest.TestCase):
    def test_reference_uses_dna_alphabet(self):
        reference = generate_reference(100, seed=1)
        self.assertEqual(len(reference), 100)
        self.assertLessEqual(set(reference), set("ATCG"))

    def test_reads_have_expected_lengths(self):
        reference = generate_reference(1000, seed=1)
        dataset = generate_reads(reference, coverage=2, noise_rate=0.0, seed=2)
        self.assertTrue(dataset.reads)
        self.assertTrue(all(30 <= len(read) <= 45 for read in dataset.reads))

    def test_zero_noise_reads_match_reference_substrings(self):
        reference = generate_reference(1000, seed=1)
        dataset = generate_reads(reference, coverage=2, noise_rate=0.0, seed=2)
        for read, start in zip(dataset.reads, dataset.read_starts):
            self.assertEqual(read, reference[start : start + len(read)])

    def test_experiment_dataset_separates_reference_and_gold_standard(self):
        dataset = generate_experiment_dataset(
            reference_length=1000,
            coverage=2,
            read_noise_rate=0.0,
            genome_mutation_rate=0.05,
            seed=3,
        )

        self.assertEqual(len(dataset.reference), len(dataset.my_genome))
        self.assertNotEqual(dataset.reference, dataset.my_genome)
        for read, start in zip(dataset.reads, dataset.read_starts):
            self.assertEqual(read, dataset.my_genome[start : start + len(read)])


if __name__ == "__main__":
    unittest.main()

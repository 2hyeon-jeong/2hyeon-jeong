import shutil
import subprocess
import unittest
from pathlib import Path

from src.algorithms.cpp_external import run_cpp_algorithm


class CppRunnerTests(unittest.TestCase):
    def test_cpp_trivial_baseline_protocol(self):
        if shutil.which("g++") is None:
            self.skipTest("g++ is not installed")

        subprocess.run(["python", "scripts/build_cpp.py"], check=True)
        executable = Path("build/algorithms/trivial_baseline.exe")
        self.assertTrue(executable.exists())

        reconstructed = run_cpp_algorithm(
            executable,
            reads=["ACGTAC", "GTACGT"],
            reference="ACGTACGT",
        )

        self.assertEqual(reconstructed, "ACGTACGT")


if __name__ == "__main__":
    unittest.main()

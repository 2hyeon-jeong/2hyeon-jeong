from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BUILD_DIR = PROJECT_ROOT / "build" / "algorithms"


def run_cpp_algorithm(executable: Path, reads: list[str], reference: str | None = None) -> str:
    if reference is None:
        raise ValueError(f"{executable.name} requires a reference sequence")

    input_text = "\n".join([reference, str(len(reads)), *reads]) + "\n"
    result = subprocess.run(
        [str(executable)],
        input=input_text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""


def discover_cpp_algorithms() -> dict[str, Callable[[list[str], str | None], str]]:
    if not BUILD_DIR.exists():
        return {}

    algorithms = {}
    for executable in sorted(BUILD_DIR.iterdir()):
        if executable.suffix.lower() not in ("", ".exe"):
            continue
        if not executable.is_file():
            continue

        name = f"cpp_{executable.stem}"

        def algorithm(
            reads: list[str],
            reference: str | None = None,
            executable: Path = executable,
        ) -> str:
            return run_cpp_algorithm(executable, reads, reference)

        algorithms[name] = algorithm

    return algorithms

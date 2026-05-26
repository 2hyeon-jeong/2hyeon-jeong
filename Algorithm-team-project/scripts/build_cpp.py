from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "cpp" / "algorithms"
BUILD_DIR = ROOT / "build" / "algorithms"


def main() -> None:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(SOURCE_DIR.glob("*.cpp"))
    if not sources:
        raise SystemExit(f"No C++ algorithm files found in {SOURCE_DIR}")

    for source in sources:
        output = BUILD_DIR / f"{source.stem}.exe"
        command = [
            "g++",
            "-std=c++17",
            "-O2",
            "-Wall",
            "-Wextra",
            str(source),
            "-o",
            str(output),
        ]
        print(" ".join(command))
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def averaged_series(
    rows: list[dict[str, str]], y_field: str
) -> dict[str, list[tuple[float, float]]]:
    grouped: dict[tuple[str, float], list[float]] = defaultdict(list)
    for row in rows:
        grouped[(row["algorithm"], float(row["coverage"]))].append(float(row[y_field]))

    series: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for (algorithm, coverage), values in grouped.items():
        series[algorithm].append((coverage, mean(values)))

    return {
        algorithm: sorted(points)
        for algorithm, points in series.items()
    }


def plot_metric(rows: list[dict[str, str]], y_field: str, output_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        plot_metric_svg(rows, y_field, output_path.with_suffix(".svg"))
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    for algorithm, points in averaged_series(rows, y_field).items():
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        plt.plot(xs, ys, marker="o", label=algorithm)

    plt.xlabel("Coverage")
    plt.ylabel(y_field.replace("_", " ").title())
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_metric_svg(rows: list[dict[str, str]], y_field: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    series = averaged_series(rows, y_field)
    all_points = [point for points in series.values() for point in points]
    if not all_points:
        output_path.write_text("", encoding="utf-8")
        return

    width = 900
    height = 520
    left = 80
    right = 30
    top = 40
    bottom = 70
    plot_width = width - left - right
    plot_height = height - top - bottom

    min_x = min(point[0] for point in all_points)
    max_x = max(point[0] for point in all_points)
    min_y = 0.0
    max_y = max(point[1] for point in all_points)
    if max_y <= min_y:
        max_y = 1.0

    def scale_x(value: float) -> float:
        if max_x == min_x:
            return left + plot_width / 2
        return left + (value - min_x) / (max_x - min_x) * plot_width

    def scale_y(value: float) -> float:
        return top + plot_height - (value - min_y) / (max_y - min_y) * plot_height

    colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="24" text-anchor="middle" font-family="Arial" font-size="18">{y_field.replace("_", " ").title()} by Coverage</text>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#222"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#222"/>',
        f'<text x="{width / 2}" y="{height - 18}" text-anchor="middle" font-family="Arial" font-size="14">Coverage</text>',
        f'<text x="20" y="{height / 2}" text-anchor="middle" font-family="Arial" font-size="14" transform="rotate(-90 20 {height / 2})">{y_field.replace("_", " ").title()}</text>',
    ]

    for tick in range(6):
        y_value = min_y + (max_y - min_y) * tick / 5
        y = scale_y(y_value)
        parts.append(f'<line x1="{left - 5}" y1="{y}" x2="{left + plot_width}" y2="{y}" stroke="#ddd"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="11">{y_value:.3g}</text>')

    for coverage in sorted({point[0] for point in all_points}):
        x = scale_x(coverage)
        parts.append(f'<line x1="{x}" y1="{top + plot_height}" x2="{x}" y2="{top + plot_height + 5}" stroke="#222"/>')
        parts.append(f'<text x="{x}" y="{top + plot_height + 22}" text-anchor="middle" font-family="Arial" font-size="11">{coverage:g}</text>')

    for index, (algorithm, points) in enumerate(sorted(series.items())):
        color = colors[index % len(colors)]
        coords = " ".join(f"{scale_x(x):.2f},{scale_y(y):.2f}" for x, y in points)
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        for x_value, y_value in points:
            parts.append(f'<circle cx="{scale_x(x_value):.2f}" cy="{scale_y(y_value):.2f}" r="4" fill="{color}"/>')

        legend_x = left + plot_width - 190
        legend_y = top + 20 + index * 22
        parts.append(f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 22}" y2="{legend_y}" stroke="{color}" stroke-width="2.5"/>')
        parts.append(f'<text x="{legend_x + 30}" y="{legend_y + 4}" font-family="Arial" font-size="12">{algorithm}</text>')

    parts.append("</svg>")
    output_path.write_text("\n".join(parts), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot benchmark CSV results.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("experiments/results/benchmark.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/figures"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input)
    plot_metric(rows, "accuracy", args.output_dir / "accuracy_by_coverage.png")
    plot_metric(rows, "runtime_seconds", args.output_dir / "runtime_by_coverage.png")


if __name__ == "__main__":
    main()

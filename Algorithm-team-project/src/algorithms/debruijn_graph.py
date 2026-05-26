from __future__ import annotations

from collections import Counter, defaultdict


def reconstruct(reads: list[str], reference: str | None = None) -> str:
    if not reads:
        return ""

    k = min(21, min(len(read) for read in reads))
    if k < 2:
        return max(reads, key=len)

    graph: dict[str, Counter[str]] = defaultdict(Counter)
    indegree: Counter[str] = Counter()
    outdegree: Counter[str] = Counter()

    for read in reads:
        for i in range(0, len(read) - k + 1):
            kmer = read[i : i + k]
            left = kmer[:-1]
            right = kmer[1:]
            graph[left][right] += 1
            outdegree[left] += 1
            indegree[right] += 1

    if not graph:
        return max(reads, key=len)

    starts = [
        node for node in graph
        if outdegree[node] > indegree[node]
    ]
    start = max(starts or graph.keys(), key=lambda node: outdegree[node])

    path = [start]
    current = start
    visited_edges = 0
    total_edges = sum(sum(targets.values()) for targets in graph.values())

    while visited_edges < total_edges and graph.get(current):
        next_node, _ = graph[current].most_common(1)[0]
        graph[current][next_node] -= 1
        if graph[current][next_node] <= 0:
            del graph[current][next_node]
        path.append(next_node)
        current = next_node
        visited_edges += 1

    sequence = path[0]
    for node in path[1:]:
        sequence += node[-1]
    return sequence


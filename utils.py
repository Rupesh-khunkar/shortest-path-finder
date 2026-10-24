"""Helper functions: validation, graph generation, formatting, benchmarking."""
import random
import statistics
import time

from algorithms import INF, bellman_ford, dijkstra, floyd_warshall


def validate_matrix(matrix):
    """Raise ValueError unless matrix is a non-empty square matrix of numbers."""
    if not isinstance(matrix, list) or not matrix:
        raise ValueError("Matrix must be a non-empty list of rows")
    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError("Matrix must be square (n x n)")
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("Matrix entries must be numbers")


def node_name(i):
    """0 -> A, 1 -> B ... (falls back to numbers after Z)."""
    return chr(65 + i) if i < 26 else str(i)


def format_path(path):
    return " -> ".join(node_name(i) for i in path) if path else "No path"


def format_matrix(matrix):
    n = len(matrix)
    lines = ["      " + "".join(f"{node_name(j):>5}" for j in range(n))]
    for i, row in enumerate(matrix):
        cells = "".join(f"{('INF' if v == INF else v):>5}" for v in row)
        lines.append(f"{node_name(i):>4}  {cells}")
    return "\n".join(lines)


def sample_matrix():
    """5-node sample graph used in the report (all weights non-negative)."""
    return [
        [0,   10,  INF, 30,  100],
        [INF, 0,   50,  INF, INF],
        [INF, INF, 0,   INF, 10],
        [INF, INF, 20,  0,   60],
        [INF, INF, INF, INF, 0],
    ]


def random_matrix(n, density=0.4, max_w=50, seed=None):
    """Random directed graph with non-negative weights (always has a chain 0->1->...)."""
    rng = random.Random(seed)
    m = [[INF] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 0
    for i in range(n - 1):
        m[i][i + 1] = rng.randint(1, max_w)
    for i in range(n):
        for j in range(n):
            if i != j and m[i][j] == INF and rng.random() < density:
                m[i][j] = rng.randint(1, max_w)
    return m


def benchmark(sizes=(10, 20, 40, 80), repeats=5, seed=7):
    """Return rows of (V, algorithm, checksum, median seconds)."""
    rows = []
    for n in sizes:
        m = random_matrix(n, seed=seed + n)
        jobs = {
            "Dijkstra": lambda: dijkstra(m, 0)[0],
            "Bellman-Ford": lambda: bellman_ford(m, 0)[0],
            "Floyd-Warshall": lambda: floyd_warshall(m)[0][0],
        }
        for name, fn in jobs.items():
            times = []
            result = None
            for _ in range(repeats):
                t0 = time.perf_counter()
                result = fn()
                times.append(time.perf_counter() - t0)
            reachable = sum(d for d in result if d != INF)
            rows.append((n, name, reachable, statistics.median(times)))
    return rows


def format_benchmark(rows):
    out = ["PERFORMANCE COMPARISON", "",
           f"{'Nodes':<7}{'Algorithm':<18}{'Sum of dist':>12}{'Median Time (s)':>20}"]
    for n, name, total, t in rows:
        out.append(f"{n:<7}{name:<18}{total:>12}{t:>20.8f}")
    return "\n".join(out)

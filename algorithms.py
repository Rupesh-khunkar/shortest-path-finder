"""Shortest-path algorithms: Dijkstra, Bellman-Ford and Floyd-Warshall.

Graphs are represented as a weighted adjacency matrix. INF means "no edge".
"""
import heapq

INF = float("inf")


class NegativeCycleError(Exception):
    """Raised when a negative-weight cycle is reachable from the source."""


def _build_path(parent, source, target):
    """Rebuild the path source -> target from a parent array."""
    if parent[target] is None and target != source:
        return []
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path


def dijkstra(matrix, source):
    """Greedy single-source shortest path using a min-heap. O((V + E) log V).

    Only valid when all edge weights are non-negative.
    Returns (dist, parent).
    """
    n = len(matrix)
    dist = [INF] * n
    parent = [None] * n
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v in range(n):
            w = matrix[u][v]
            if u != v and w != INF:
                if w < 0:
                    raise ValueError("Dijkstra cannot handle negative edge weights")
                if d + w < dist[v]:
                    dist[v] = d + w
                    parent[v] = u
                    heapq.heappush(heap, (dist[v], v))
    return dist, parent


def bellman_ford(matrix, source):
    """Single-source shortest path by edge relaxation. O(V * E).

    Handles negative weights and detects negative cycles.
    Returns (dist, parent).
    """
    n = len(matrix)
    dist = [INF] * n
    parent = [None] * n
    dist[source] = 0
    edges = [(u, v, matrix[u][v]) for u in range(n) for v in range(n)
             if u != v and matrix[u][v] != INF]
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise NegativeCycleError("Graph contains a negative-weight cycle")
    return dist, parent


def floyd_warshall(matrix):
    """All-pairs shortest paths by dynamic programming. O(V^3).

    Returns (dist, nxt) where nxt[i][j] is the next node on the path i -> j.
    """
    n = len(matrix)
    dist = [row[:] for row in matrix]
    nxt = [[j if (i != j and matrix[i][j] != INF) else None for j in range(n)]
           for i in range(n)]
    for i in range(n):
        dist[i][i] = 0
        nxt[i][i] = i
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    if any(dist[i][i] < 0 for i in range(n)):
        raise NegativeCycleError("Graph contains a negative-weight cycle")
    return dist, nxt


def floyd_path(nxt, source, target):
    """Rebuild the path source -> target from the Floyd-Warshall next matrix."""
    if nxt[source][target] is None:
        return []
    path = [source]
    while source != target:
        source = nxt[source][target]
        path.append(source)
    return path


def single_source_path(parent, source, target):
    """Public helper to rebuild a path from a parent array."""
    return _build_path(parent, source, target)

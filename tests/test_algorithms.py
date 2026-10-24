import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms import (INF, NegativeCycleError, bellman_ford, dijkstra,  # noqa: E402
                        floyd_path, floyd_warshall, single_source_path)
from utils import random_matrix, sample_matrix, validate_matrix  # noqa: E402


class TestShortestPaths(unittest.TestCase):
    def test_tc01_sample_distances(self):
        d, _ = dijkstra(sample_matrix(), 0)
        self.assertEqual(d, [0, 10, 50, 30, 60])
        self.assertEqual(bellman_ford(sample_matrix(), 0)[0], d)
        self.assertEqual(floyd_warshall(sample_matrix())[0][0], d)

    def test_tc02_negative_edge(self):
        m = [[0, 4, INF], [INF, 0, -2], [INF, INF, 0]]
        self.assertEqual(bellman_ford(m, 0)[0], [0, 4, 2])
        self.assertEqual(floyd_warshall(m)[0][0], [0, 4, 2])
        with self.assertRaises(ValueError):
            dijkstra(m, 0)

    def test_tc03_negative_cycle(self):
        m = [[0, 1, INF], [INF, 0, -3], [1, INF, 0]]
        with self.assertRaises(NegativeCycleError):
            bellman_ford(m, 0)
        with self.assertRaises(NegativeCycleError):
            floyd_warshall(m)

    def test_tc04_single_node_and_unreachable(self):
        self.assertEqual(dijkstra([[0]], 0)[0], [0])
        m = [[0, INF], [INF, 0]]
        d, parent = dijkstra(m, 0)
        self.assertEqual(d, [0, INF])
        self.assertEqual(single_source_path(parent, 0, 1), [])

    def test_tc05_random_graphs_agree(self):
        for n in (5, 10, 25):
            m = random_matrix(n, seed=n)
            fw = floyd_warshall(m)[0]
            for s in range(n):
                self.assertEqual(dijkstra(m, s)[0], fw[s])
                self.assertEqual(bellman_ford(m, s)[0], fw[s])

    def test_tc06_path_reconstruction(self):
        m = sample_matrix()
        _, parent = dijkstra(m, 0)
        self.assertEqual(single_source_path(parent, 0, 4), [0, 3, 2, 4])
        _, nxt = floyd_warshall(m)
        self.assertEqual(floyd_path(nxt, 0, 4), [0, 3, 2, 4])

    def test_tc07_invalid_matrix(self):
        for bad in ([], [[0, 1], [1]], [[0, "x"], [1, 0]], "abc"):
            with self.assertRaises(ValueError):
                validate_matrix(bad)


if __name__ == "__main__":
    unittest.main()

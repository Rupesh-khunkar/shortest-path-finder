# Shortest Path Finder Demonstration

**Design and Analysis of Algorithms (DAA) Mini Project — Python 3.10+**

A menu-driven program that models a road network as a weighted directed graph and
finds shortest paths with three classic algorithms, then compares them.

| Algorithm | Technique | Time | Space | Negative edges |
|---|---|---|---|---|
| Dijkstra | Greedy + min-heap | O((V+E) log V) | O(V) | No |
| Bellman-Ford | Dynamic programming / relaxation | O(V·E) | O(V) | Yes (+ cycle detection) |
| Floyd-Warshall | Dynamic programming (all pairs) | O(V³) | O(V²) | Yes (+ cycle detection) |

## Project structure
```
shortest-path-finder-daa/
├── algorithms.py          # Dijkstra, Bellman-Ford, Floyd-Warshall
├── utils.py               # validation, random graphs, formatting, benchmark
├── main.py                # menu-driven program
├── tests/test_algorithms.py
├── screenshots/           # output screenshots used in the report
├── README.md
└── .gitignore
```

## How to run
```bash
git clone <your-repository-url>
cd shortest-path-finder-daa
python main.py                       # start the menu
python -m unittest discover -s tests -v   # run the tests
```
No external libraries are needed to run the program (standard library only).

### Regenerate the report (optional)
```bash
pip install reportlab pillow matplotlib
python report/make_screenshots.py
python report/build_report.py --url <your-repo-url> --name "Your Name"
```

## Input format
Graph = adjacency matrix. `matrix[i][j]` is the weight of edge i → j, `inf` means no edge, diagonal = 0.
Nodes are shown as A, B, C … in the output.

## Sample (5 nodes)
Shortest distances from A: `A=0, B=10, C=50, D=30, E=60` (path to E: A -> D -> C -> E).

## Future scope
A* search, bidirectional Dijkstra, Johnson's algorithm, graph visualization, real map data.

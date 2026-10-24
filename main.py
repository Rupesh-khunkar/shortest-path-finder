"""Menu-driven Shortest Path Finder demonstration (DAA mini project)."""
from algorithms import (INF, NegativeCycleError, bellman_ford, dijkstra,
                        floyd_path, floyd_warshall, single_source_path)
from utils import (benchmark, format_benchmark, format_matrix, format_path,
                   node_name, random_matrix, sample_matrix, validate_matrix)

BANNER = "=" * 60


def read_matrix():
    n = int(input("Number of nodes: "))
    print("Enter each row; use 'inf' for no edge:")
    matrix = []
    for i in range(n):
        row = [INF if x.lower() == "inf" else float(x) if "." in x else int(x)
               for x in input(f"Row {node_name(i)}: ").split()]
        matrix.append(row)
    validate_matrix(matrix)
    return matrix


def pick_node(prompt, n):
    value = input(f"{prompt} (0-{n - 1}): ").strip()
    node = int(value)
    if not 0 <= node < n:
        raise ValueError("Node out of range")
    return node


def run_single(matrix, source, algo):
    fn = dijkstra if algo == "dijkstra" else bellman_ford
    dist, parent = fn(matrix, source)
    for t in range(len(matrix)):
        d = "unreachable" if dist[t] == INF else dist[t]
        print(f"  {node_name(source)} -> {node_name(t)} : {d:>11}   "
              f"{format_path(single_source_path(parent, source, t))}")


def compare(matrix, source):
    d1, _ = dijkstra(matrix, source)
    d2, _ = bellman_ford(matrix, source)
    d3, _ = floyd_warshall(matrix)
    print("Dijkstra       :", d1)
    print("Bellman-Ford   :", d2)
    print("Floyd-Warshall :", d3[source])
    print("All algorithms agree:", d1 == d2 == d3[source])


def main():
    matrix = sample_matrix()
    while True:
        print(f"\n{BANNER}\n      SHORTEST PATH FINDER DEMONSTRATION\n{BANNER}")
        print("1. Enter / Generate Graph Matrix")
        print("2. Solve using Dijkstra")
        print("3. Solve using Bellman-Ford")
        print("4. Solve using Floyd-Warshall (all pairs)")
        print("5. Compare Algorithms")
        print("6. Performance Benchmark")
        print("7. Exit")
        try:
            choice = input("\nEnter choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        try:
            if choice == "1":
                mode = input("(m)anual or (r)andom? ").strip().lower()
                matrix = read_matrix() if mode == "m" else random_matrix(
                    int(input("Number of nodes: ")), seed=1)
                print(format_matrix(matrix))
            elif choice in ("2", "3"):
                print(format_matrix(matrix))
                s = pick_node("Source", len(matrix))
                run_single(matrix, s, "dijkstra" if choice == "2" else "bellman")
            elif choice == "4":
                dist, nxt = floyd_warshall(matrix)
                print(format_matrix(dist))
                s = pick_node("Source", len(matrix))
                t = pick_node("Target", len(matrix))
                print("Path:", format_path(floyd_path(nxt, s, t)), "| Cost:", dist[s][t])
            elif choice == "5":
                compare(matrix, pick_node("Source", len(matrix)))
            elif choice == "6":
                print(format_benchmark(benchmark()))
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except NegativeCycleError as exc:
            print("Error:", exc)
        except (ValueError, IndexError) as exc:
            print("Input error:", exc)


if __name__ == "__main__":
    main()

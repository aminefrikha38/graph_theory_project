import math
import os

INF = float("inf")


def load_graph_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    m = int(lines[1])

    edges = []
    for line in lines[2:2 + m]:
        u, v, w = map(int, line.split())
        edges.append((u, v, w))

    return n, edges


def build_matrices(n, edges):
    L = [[INF] * n for _ in range(n)]
    P = [[None] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 0
        P[i][i] = i

    for u, v, w in edges:
        L[u][v] = w
        P[u][v] = u

    return L, P


def format_value(x):
    if x == INF:
        return "∞"
    return str(x)


def print_matrix(matrix, title):
    print(f"\n{title}")
    n = len(matrix)
    width = 5

    print(" " * width, end="")
    for j in range(n):
        print(f"{j:>{width}}", end="")
    print()

    for i in range(n):
        print(f"{i:>{width}}", end="")
        for j in range(n):
            print(f"{format_value(matrix[i][j]):>{width}}", end="")
        print()


def print_predecessor_matrix(P, title):
    print(f"\n{title}")
    n = len(P)
    width = 5

    print(" " * width, end="")
    for j in range(n):
        print(f"{j:>{width}}", end="")
    print()

    for i in range(n):
        print(f"{i:>{width}}", end="")
        for j in range(n):
            val = "-" if P[i][j] is None else str(P[i][j])
            print(f"{val:>{width}}", end="")
        print()


def floyd_warshall(L, P, show_steps=True):
    n = len(L)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if L[i][k] != INF and L[k][j] != INF:
                    new_dist = L[i][k] + L[k][j]
                    if new_dist < L[i][j]:
                        L[i][j] = new_dist
                        P[i][j] = P[k][j]

        if show_steps:
            print_matrix(L, f"Distance matrix after using node {k}")
            print_predecessor_matrix(P, f"Predecessor matrix after using node {k}")

    return L, P


def has_negative_cycle(L):
    n = len(L)
    for i in range(n):
        if L[i][i] < 0:
            return True
    return False


def reconstruct_path(P, start, end):
    if P[start][end] is None:
        return None

    path = [end]
    current = end

    while current != start:
        current = P[start][current]
        if current is None:
            return None
        path.append(current)

    path.reverse()
    return path


def display_all_shortest_paths(L, P):
    n = len(L)
    print("\n===== ALL SHORTEST PATHS =====")

    for i in range(n):
        for j in range(n):
            if i != j:
                if L[i][j] == INF:
                    print(f"From {i} to {j}: no path")
                else:
                    path = reconstruct_path(P, i, j)
                    print(f"From {i} to {j}: cost = {L[i][j]}, path = {' -> '.join(map(str, path))}")


def process_graph(filename):
    print(f"\nLoading file: {filename}")
    n, edges = load_graph_from_file(filename)

    print(f"Number of nodes: {n}")
    print(f"Number of edges: {len(edges)}")
    print("Edges:", edges)

    L, P = build_matrices(n, edges)

    print_matrix(L, "Initial distance matrix")
    print_predecessor_matrix(P, "Initial predecessor matrix")

    L_final, P_final = floyd_warshall(L, P, show_steps=True)

    print_matrix(L_final, "Final distance matrix")
    print_predecessor_matrix(P_final, "Final predecessor matrix")

    if has_negative_cycle(L_final):
        print("\nThe graph contains a negative cycle.")
        print("Shortest paths are not well defined.")
        return

    print("\nNo negative cycle detected.")

    while True:
        answer = input("\nDo you want to display a specific shortest path? (y/n): ").strip().lower()
        if answer != "y":
            break

        try:
            start = int(input("Start node: "))
            end = int(input("End node: "))

            if not (0 <= start < n and 0 <= end < n):
                print("Invalid node.")
                continue

            if L_final[start][end] == INF:
                print(f"No path from {start} to {end}.")
            else:
                path = reconstruct_path(P_final, start, end)
                print(f"Minimum cost from {start} to {end}: {L_final[start][end]}")
                print("Path:", " -> ".join(map(str, path)))

        except ValueError:
            print("Invalid input.")

    all_paths = input("\nDisplay all shortest paths? (y/n): ").strip().lower()
    if all_paths == "y":
        display_all_shortest_paths(L_final, P_final)


def main():
    print("===== GRAPH THEORY PROJECT - FLOYD-WARSHALL =====")

    while True:
        graph_num = input("\nEnter graph number (or 'q' to quit): ").strip()

        if graph_num.lower() == 'q':
            print("Program terminated.")
            break

        filename = f"graph{graph_num}.txt"

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            continue

        try:
            process_graph(filename)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
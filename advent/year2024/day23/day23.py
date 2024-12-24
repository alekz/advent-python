import os
import sys
from collections import defaultdict

import networkx as nx
from networkx.algorithms.clique import find_cliques

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[list[str]]:
    with open(path) as f:
        return list(map(lambda x: x.split("-"), f.read().strip().split("\n")))


def get_connection_map(pairs: list[list[str]]) -> dict[str, set[str]]:
    connection_map: dict[str, set[str]] = defaultdict(set)
    for a, b in pairs:
        connection_map[a].add(b)
        connection_map[b].add(a)
    return connection_map


def get_matching_sets_count(pairs: list[list[str]]) -> int:
    connection_map = get_connection_map(pairs)

    groups: set[tuple[str, ...]] = set()
    for node1, connections1 in connection_map.items():
        for node2 in connections1:
            connections2 = connection_map[node2]
            connections = connections1 & connections2
            for node3 in connections:
                groups.add(tuple(sorted([node1, node2, node3])))

    def _filter_group(group: tuple[str, ...]) -> bool:
        for n in group:
            if n[0] == "t":
                return True
        return False

    return len(list(filter(_filter_group, groups)))


def get_password(pairs: list[list[str]]) -> str:
    g = nx.Graph()
    g.add_edges_from((a, b) for a, b in pairs)

    max_clique: list[str] = []
    for clique in find_cliques(g):
        if len(clique) > len(max_clique):
            max_clique = clique

    return ",".join(sorted(max_clique))


def run(input_path: str) -> None:
    pairs = read_input(input_path)

    matching_sets_count = get_matching_sets_count(pairs)
    print(f"Matching sets = {matching_sets_count}")

    password = get_password(pairs)
    print(f"Password = {password}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

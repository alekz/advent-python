import os
import sys
from collections import namedtuple

import networkx as nx

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type MapData = list[list[str]]
Point = namedtuple("Point", ["x", "y"])


def read_input(path: str) -> list[Point]:
    coords = []
    with open(path) as f:
        for line in f:
            x, y = list(map(int, line.strip().split(",")))
            coords.append(Point(x, y))
    return coords


def get_shortest_path(map_data: MapData) -> list[Point]:
    w, h = len(map_data[0]), len(map_data)
    start = Point(0, 0)
    finish = Point(w - 1, h - 1)

    g = nx.Graph()
    for y in range(h):
        for x in range(w):
            if map_data[y][x] == "#":
                continue
            if x < w - 1 and map_data[y][x + 1] != "#":
                g.add_edge(Point(x, y), Point(x + 1, y))
            if y < h - 1 and map_data[y + 1][x] != "#":
                g.add_edge(Point(x, y), Point(x, y + 1))
    try:
        path: list[Point] = nx.shortest_path(g, start, finish)
        return path
    except nx.NetworkXNoPath:
        return []


def get_first_blocking_byte(coords: list[Point], size: int) -> Point:
    map_data: MapData = [["." for _ in range(size)] for _ in range(size)]
    path_set: set[Point] = set()
    for i in range(len(coords)):
        p = coords[i]
        map_data[p.y][p.x] = "#"
        if not path_set or p in path_set:
            path = get_shortest_path(map_data)
            if not path:
                return p
            path_set = set(path)
    return Point(-1, -1)


def run(input_path: str, size: int, bytes_count: int) -> None:
    coords = read_input(input_path)
    map_data: MapData = [["." for _ in range(size)] for _ in range(size)]
    for i in range(bytes_count):
        x, y = coords[i]
        map_data[y][x] = "#"

    path_length = len(get_shortest_path(map_data))
    print(f"Path length = {path_length}")

    blocking_byte = get_first_blocking_byte(coords, size)
    print(f"Blocking byte: {blocking_byte.x},{blocking_byte.y}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 71
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    run(input_path, size, count)


if __name__ == "__main__":
    main()

import os
import sys
from collections import namedtuple

from utils.input_parsing import input_to_2d_array

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

NEIGHBORS = [(0, -1), (+1, 0), (0, +1), (-1, 0)]

type MapData = list[list[str]]
Point = namedtuple("Point", ["x", "y"])


def read_input(path: str) -> MapData:
    return input_to_2d_array(path)


def find_map_char(map_data: MapData, char: str) -> Point:
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == char:
                return Point(x, y)
    return Point(-1, -1)


def get_path(map_data: MapData, start: Point, finish: Point) -> dict[Point, int]:
    path: dict[Point, int] = {start: 0}

    p = start
    d = 0
    while p != finish:
        for dx, dy in NEIGHBORS:
            n = Point(p.x + dx, p.y + dy)
            if n in path:
                continue
            if map_data[n.y][n.x] == "#":
                continue
            d += 1
            path[n] = d
            p = n
            break

    return path


def get_routes_count(
    map_data: MapData, max_cheat: int = 2, min_delta: int = 100
) -> int:
    w, h = len(map_data[0]), len(map_data)
    start = find_map_char(map_data, "S")
    finish = find_map_char(map_data, "E")
    path = get_path(map_data, start, finish)

    deltas_count = 0
    for o, d in path.items():
        min_y = max(o.y - max_cheat, 0)
        max_y = min(o.y + max_cheat + 1, h)
        for dy in range(min_y - o.y, max_y - o.y):
            max_dx = max_cheat - abs(dy)
            min_x = max(o.x - max_dx, 0)
            max_x = min(o.x + max_dx + 1, w)
            for dx in range(min_x - o.x, max_x - o.x):
                dd = abs(dx) + abs(dy)
                p = Point(o.x + dx, o.y + dy)
                if p in path:
                    delta = path[p] - d - dd
                    if delta >= min_delta:
                        deltas_count += 1
    return deltas_count


def run(input_path: str) -> None:
    map_data = read_input(input_path)
    fast_routes_count_1 = get_routes_count(map_data, max_cheat=2, min_delta=100)
    fast_routes_count_2 = get_routes_count(map_data, max_cheat=20, min_delta=100)
    print(f"Fast routes 1: {fast_routes_count_1}")
    print(f"Fast routes 2: {fast_routes_count_2}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

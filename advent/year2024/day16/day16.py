import os
import sys
from collections import defaultdict, namedtuple
from heapq import heappop, heappush

from utils.input_parsing import input_to_array_of_strings

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
NEIGHBORS = [(0, -1), (+1, 0), (0, +1), (-1, 0)]
INF = sys.maxsize
MOVE_COST = 1
TURN_COST = 1000

type MapData = list[str]
Point = namedtuple("Point", ["x", "y"])
Node = namedtuple("Node", ["x", "y", "d"])


def read_input(path: str) -> MapData:
    return input_to_array_of_strings(path)


def get_start_location(map_data: MapData) -> Point:
    return get_location_by_char(map_data, "S")


def get_end_location(map_data: MapData) -> Point:
    return get_location_by_char(map_data, "E")


def get_location_by_char(map_data: MapData, char: str) -> Point:
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == char:
                return Point(x, y)
    return Point(-1, -1)


def get_dijkstra_score(map_data: MapData) -> tuple[int, int]:
    x0, y0 = get_start_location(map_data)
    d0 = EAST

    unvisited: list[tuple[int, Node]] = []
    visited: set[Node] = set()
    distances: dict[Node, int] = defaultdict(lambda: INF)
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell != "#":
                for d in range(4):
                    node = Node(x, y, d)
                    heappush(unvisited, (INF, node))
                    distances[node] = INF
    heappush(unvisited, (0, Node(x0, y0, d0)))
    distances[Node(x0, y0, d0)] = 0

    distance = INF

    while unvisited:
        s, node = heappop(unvisited)
        if node in visited:
            continue
        for nd in [(node.d + 1) % 4, (node.d + 3) % 4]:
            nnode = Node(node.x, node.y, nd)
            ns = s + TURN_COST
            heappush(unvisited, (ns, nnode))
            distances[nnode] = min(distances[nnode], ns)

        dx, dy = NEIGHBORS[node.d]
        nx, ny = node.x + dx, node.y + dy
        if map_data[ny][nx] != "#":
            nnode = Node(nx, ny, node.d)
            ns = s + MOVE_COST
            heappush(unvisited, (ns, nnode))
            distances[nnode] = min(distances[nnode], ns)

        visited.add(node)

        if map_data[node.y][node.x] == "E":
            distance = min(distance, s)

    length = get_optimal_path_length(map_data, distances, distance)

    return distance, length


def get_optimal_path_length(
    map_data: MapData, distances: dict[Node, int], path_length: int
) -> int:
    x1, y1 = get_end_location(map_data)

    nodes: set[Node] = set()
    for d in range(4):
        if distances[Node(x1, y1, d)] <= path_length:
            nodes.add(Node(x1, y1, d))

    path: set[Point] = set()
    path.add(Point(x1, y1))

    while nodes:
        node = nodes.pop()
        s = distances[node]

        for nd in [(node.d + 1) % 4, (node.d + 3) % 4]:
            nnode = Node(node.x, node.y, nd)
            ns = s - TURN_COST
            if distances[nnode] <= ns:
                nodes.add(nnode)
                path.add(Point(nnode.x, nnode.y))

        dx, dy = NEIGHBORS[node.d]
        nx, ny = node.x - dx, node.y - dy
        if map_data[ny][nx] != "#":
            nnode = Node(nx, ny, node.d)
            ns = s - MOVE_COST
            if distances[nnode] <= ns:
                nodes.add(nnode)
                path.add(Point(nnode.x, nnode.y))

    return len(path)


def run(input_path: str) -> None:
    map_data = read_input(input_path)
    score, length = get_dijkstra_score(map_data)
    print(f"Score = {score}")
    print(f"Path length = {length}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

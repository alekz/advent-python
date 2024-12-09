import os
import sys
from copy import deepcopy

from utils.input_parsing import input_to_2d_array

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[list[str]]:
    return input_to_2d_array(path)


def get_map_start(area_map: list[list[str]]) -> tuple[int, int]:
    width, height = len(area_map[0]), len(area_map)

    for y0 in range(height):
        try:
            x0 = area_map[y0].index("^")
        except ValueError:
            pass
        else:
            return x0, y0

    return -1, -1


def navigate_map(area_map: list[list[str]]) -> bool:
    width, height = len(area_map[0]), len(area_map)

    # list of dx, dy: up, right, down, left
    directions = [
        (0, -1),
        (+1, 0),
        (0, +1),
        (-1, 0),
    ]

    direction = 0
    x, y = get_map_start(area_map)
    area_map[y][x] = "X"
    turns: list[set] = [set(), set(), set(), set()]

    while True:
        dx, dy = directions[direction]
        while True:
            xn, yn = x + dx, y + dy

            # Out of map bounds?
            if xn < 0 or width <= xn or yn < 0 or height <= yn:
                return True

            # Obstacle?
            if area_map[yn][xn] == "#":
                if (x, y) in turns[direction]:
                    return False
                else:
                    turns[direction].add((x, y))
                direction = (direction + 1) % len(directions)
                break

            # Walking
            x, y = xn, yn
            area_map[y][x] = "X"


def copy_map(from_map: list[list[str]], to_map: list[list[str]]):
    width, height = len(from_map[0]), len(from_map)
    for y in range(height):
        for x in range(width):
            to_map[y][x] = from_map[y][x]


def calculate_path_length(area_map: list[list[str]]) -> int:
    area_map = deepcopy(area_map)
    navigate_map(area_map)
    return "\n".join(list(map(lambda x: "".join(x), area_map))).count("X")


def place_obstacles(area_map: list[list[str]]) -> int:
    # Pre-navigate map, so that we place obstacles only on the path
    navigated_map = deepcopy(area_map)
    navigate_map(navigated_map)

    area_map_copy = deepcopy(area_map)

    width, height = len(area_map[0]), len(area_map)
    obstacles_count = 0
    for y in range(height):
        for x in range(width):
            if navigated_map[y][x] != "X":
                continue
            area_map_copy[y][x] = "#"
            if not navigate_map(area_map_copy):
                obstacles_count += 1
            copy_map(area_map, area_map_copy)
    return obstacles_count


def run(input_path: str) -> None:
    area_map = read_input(input_path)

    positions_count = calculate_path_length(area_map)
    print(f"Positions = {positions_count}")

    obstacles_count = place_obstacles(area_map)
    print(f"Obstacles count = {obstacles_count}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

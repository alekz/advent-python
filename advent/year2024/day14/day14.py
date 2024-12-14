import os
import re
import sys
from collections import namedtuple
from functools import reduce
from operator import mul

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Robot = namedtuple("Robot", ["x", "y", "vx", "vy"])


def read_input(path: str) -> list[Robot]:
    items = []
    with open(path) as f:
        for line in f:
            match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
            if match:
                items.append(Robot(*map(int, match.groups())))
    return items


def get_safety_factor(robots: list[Robot], width: int, height: int, time: int) -> int:
    quadrants = [0, 0, 0, 0]
    xm, ym = (width - 1) / 2, (height - 1) / 2
    for x, y, vx, vy in robots:
        x = (x + time * vx) % width
        y = (y + time * vy) % height
        if x == xm or y == ym:
            continue
        q = (0 if x < xm else 1) + (0 if y < ym else 2)
        quadrants[q] += 1
    return reduce(mul, quadrants)


def print_map(robots: list[Robot], width: int, height: int, time: int) -> None:
    m = [[0 for _ in range(width)] for _ in range(height)]
    for x, y, vx, vy in robots:
        x = (x + time * vx) % width
        y = (y + time * vy) % height
        m[y][x] += 1
    print("\n".join("".join(map(str, row)) for row in m).replace("0", " "))


def run(input_path: str, width: int, height: int, time: int = 100) -> None:
    robots = read_input(input_path)
    safety = get_safety_factor(robots, width, height, time)
    print(f"Safety factor = {safety}")

    # Print Christmas tree
    print_map(robots, width, height, 7709)


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    width, height = 101, 103
    if len(sys.argv) > 3:
        width, height = int(sys.argv[2]), int(sys.argv[3])
    run(input_path, width, height)


if __name__ == "__main__":
    main()

import os
import sys

from utils.input_parsing import str_to_2d_array

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type MapData = list[list[str]]

MOVES = {"<": (-1, 0), ">": (+1, 0), "^": (0, -1), "v": (0, +1)}


def read_input(path: str) -> tuple[MapData, str]:
    with open(path) as f:
        data = f.read()
    map_str, moves = data.strip().split("\n\n")
    map_data = str_to_2d_array(map_str)
    moves = moves.strip().replace("\n", "")
    return map_data, moves


def print_map(map_data: MapData) -> None:
    for row in map_data:
        print("".join(row))


def get_robot_location(map_data: MapData) -> tuple[int, int]:
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == "@":
                return x, y
    return -1, -1


def process_move(map_data: MapData, x: int, y: int, move: str) -> tuple[int, int]:
    if move not in MOVES:
        return x, y
    dx, dy = MOVES[move]
    xn, yn = x, y
    has_boxes = False
    while True:
        xn, yn = xn + dx, yn + dy
        cell = map_data[yn][xn]
        if cell == "O":
            has_boxes = True
        elif cell == ".":
            # Move self and possibly boxes
            if has_boxes:
                map_data[yn][xn] = "O"
                map_data[y + dy][x + dx] = "."
            return x + dx, y + dy
        elif cell == "#":
            # Didn't move
            return x, y


def navigate(map_data: MapData, moves: str) -> None:
    # Extract robot location, replace with floor tile
    x, y = get_robot_location(map_data)
    map_data[y][x] = "."
    for move in moves:
        x, y = process_move(map_data, x, y, move)


def get_score(map_data: MapData) -> int:
    score = 0
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == "O":
                score += 100 * y + x
    return score


def run(input_path: str) -> None:
    map_data, moves = read_input(input_path)
    navigate(map_data, moves)
    score = get_score(map_data)
    print(f"Score = {score}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type MapData = list[list[str]]

MOVES = {"<": (-1, 0), ">": (+1, 0), "^": (0, -1), "v": (0, +1)}


def read_input(path: str) -> tuple[MapData, str]:
    with open(path) as f:
        data = f.read()
    map_str, moves = data.strip().split("\n\n")
    map_data = []
    for row_str in map_str.split("\n"):
        row = []
        for char in row_str.strip():
            if char == "O":
                row.extend(["[", "]"])
            elif char == "@":
                row.extend(["@", "."])
            else:
                row.extend([char, char])
        map_data.append(row)
    moves = moves.strip().replace("\n", "")
    return map_data, moves


def print_map(map_data: MapData, x: int = -1, y: int = -1) -> None:
    char = None
    if x >= 0 and y >= 0:
        char = map_data[y][x]
        map_data[y][x] = "@"
    for row in map_data:
        print("".join(row))
    if char is not None:
        map_data[y][x] = char


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
    if dx != 0:
        return process_horizontal_move(map_data, x, y, dx)
    else:
        return process_vertical_move(map_data, x, y, dy)


def process_horizontal_move(
    map_data: MapData, x: int, y: int, dx: int
) -> tuple[int, int]:
    xn = x
    boxes = 0
    while True:
        xn += dx
        cell = map_data[y][xn]
        if cell in "[]":
            boxes += 1
        elif cell == ".":
            # Move self and possibly boxes
            if boxes > 0:
                box_chars = "[]" if dx < 0 else "]["
                for xb in range(boxes):
                    map_data[y][xn - xb * dx] = box_chars[xb % 2]
                map_data[y][x + dx] = "."
            return x + dx, y
        elif cell == "#":
            # Didn't move
            return x, y


def process_vertical_move(
    map_data: MapData, x: int, y: int, dy: int
) -> tuple[int, int]:
    yn = y
    xs: set[int] = {x}
    boxes: set[tuple[int, int]] = set()
    while True:
        xns: set[int] = set()
        yn += dy
        has_boxes = False

        for xn in xs:
            cell = map_data[yn][xn]
            if cell == "#":
                # Found wall, don't move
                return x, y
            elif cell == "[":
                has_boxes = True
                boxes.add((xn, yn))
                xns.update([xn, xn + 1])
            elif cell == "]":
                has_boxes = True
                boxes.add((xn - 1, yn))
                xns.update([xn, xn - 1])

        # Pushing more boxes?
        if has_boxes:
            xs = xns
            continue

        # Move all boxes, starting with the farthest
        for bx, by in sorted(boxes, key=lambda b: b[1], reverse=dy > 0):
            map_data[by + dy][bx] = "["
            map_data[by + dy][bx + 1] = "]"
            map_data[by][bx] = "."
            map_data[by][bx + 1] = "."

        return x, y + dy


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
            if cell == "[":
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

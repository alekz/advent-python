import os
import sys
from functools import cache
from itertools import permutations

from utils.input_parsing import input_to_array_of_strings

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type Keypad = list[str]
type KeypadMap = dict[str, list[str]]

DIRECTIONS = {"<": (-1, 0), ">": (+1, 0), "^": (0, -1), "v": (0, +1)}
NUM_KEYPAD: Keypad = ["789", "456", "123", " 0A"]
NAV_KEYPAD: Keypad = [" ^A", "<v>"]


def read_input(path: str) -> list[str]:
    return input_to_array_of_strings(path)


# Exclude paths outside keypad's bounds
def is_valid_path(keypad: Keypad, path: str, x: int, y: int) -> bool:
    for char in path:
        dx, dy = DIRECTIONS[char]
        x, y = x + dx, y + dy
        if keypad[y][x] == " ":
            return False
    return True


# Calculate every valid path for every pair of keys on a keypad
def build_paths_for_keypad(keypad: Keypad) -> KeypadMap:
    paths = {}
    for y1, row1 in enumerate(keypad):
        for x1, key_from in enumerate(row1):
            if keypad[y1][x1] == " ":
                continue
            for y2, row2 in enumerate(keypad):
                for x2, key_to in enumerate(row2):
                    if keypad[y2][x2] == " ":
                        continue
                    dx, dy = x2 - x1, y2 - y1
                    sx = "<" * -dx if dx < 0 else ">" * dx
                    sy = "^" * -dy if dy < 0 else "v" * dy
                    paths[key_from + key_to] = list(
                        filter(
                            lambda path: is_valid_path(keypad, path, x1, y1),
                            ["".join(s) for s in set(permutations(sx + sy))],
                        )
                    )
    return paths


NUM_PATHS = build_paths_for_keypad(NUM_KEYPAD)
NAV_PATHS = build_paths_for_keypad(NAV_KEYPAD)


def get_sequences(code: str, keypad_map: KeypadMap) -> set[str]:
    sequences = {""}
    prev_char = "A"
    for char in code:
        char_sequences = keypad_map[prev_char + char]
        sequences = {s1 + s2 + "A" for s1 in sequences for s2 in char_sequences}
        prev_char = char
    return sequences


@cache
def get_min_nav_pair_length(from_char: str, to_char: str, robots_count: int) -> int:
    if robots_count == 1:
        return min(len(path + "A") for path in NAV_PATHS[from_char + to_char])

    return min(
        get_min_nav_path_length(path + "A", robots_count - 1)
        for path in NAV_PATHS[from_char + to_char]
    )


def get_min_nav_path_length(path: str, robots_count: int) -> int:
    path = "A" + path
    return sum(
        get_min_nav_pair_length(path[i], path[i + 1], robots_count)
        for i in range(len(path) - 1)
    )


def get_code_complexity(code: str, robots_count: int) -> int:
    paths = get_sequences(code, NUM_PATHS)
    min_len = min(get_min_nav_path_length(path, robots_count) for path in paths)
    number = int(code[:-1])
    return min_len * number


def get_complexity(codes: list[str], robots_count: int) -> int:
    return sum(get_code_complexity(code, robots_count) for code in codes)


def run(input_path: str) -> None:
    codes = read_input(input_path)
    for robots_count in [2, 25]:
        complexity = get_complexity(codes, robots_count)
        print(f"Complexity ({robots_count}) = {complexity}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

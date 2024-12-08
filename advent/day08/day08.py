import os
import sys
from collections import defaultdict
from itertools import permutations

from utils.input_parsing import input_to_2d_array

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[list[str]]:
    return input_to_2d_array(path)


def get_frequencies_from_map(
    map_data: list[list[str]],
) -> dict[str, set[tuple[int, int]]]:
    frequencies = defaultdict(set)
    for y, row in enumerate(map_data):
        for x, freq in enumerate(row):
            if freq != ".":
                frequencies[freq].add((x, y))
    return frequencies


def get_antinodes_count(
    map_data: list[list[str]],
    frequencies: dict[str, set[tuple[int, int]]],
    use_harmonics: bool = False,
) -> int:
    antinodes = set()

    width, height = len(map_data[0]), len(map_data)

    for freq, locations in frequencies.items():
        if use_harmonics:
            antinodes.update(locations)
        antenna_pairs = permutations(locations, 2)
        for (x1, y1), (x2, y2) in antenna_pairs:
            x, y = x2, y2
            dx, dy = x2 - x1, y2 - y1
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < width and 0 <= y < height):
                    break
                antinodes.add((x, y))
                if not use_harmonics:
                    break

    return len(antinodes)


def run(input_path: str) -> None:
    map_data = read_input(input_path)

    frequencies = get_frequencies_from_map(map_data)
    antinodes_count = get_antinodes_count(map_data, frequencies, use_harmonics=False)
    antinodes_with_harmonics_count = get_antinodes_count(
        map_data, frequencies, use_harmonics=True
    )

    print(f"Antinodes count = {antinodes_count}")
    print(f"Antinodes with harmonics count = {antinodes_with_harmonics_count}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

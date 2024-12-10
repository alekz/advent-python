import os
import sys
from collections import defaultdict

from utils.input_parsing import input_to_array_of_strings

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[str]:
    return input_to_array_of_strings(path)


def get_trailheads_scores_and_ratings(area_map: list[str]) -> tuple[int, int]:
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    peak_height = 9
    sx, sy = len(area_map[0]), len(area_map)

    # Algorithm: we iterate from the top heights (peaks) to bottom, calculating the
    # trailheads and their scores and ratings at each height.
    # At each lower height we use the trailheads from the previous height to calculate
    # new values at the lower height, and so on.

    # Map of all peaks reachable from each location at current height
    trail_map: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    # Ratings for each location at current height
    trail_ratings: dict[tuple[int, int], int] = defaultdict(int)
    # Map of all peaks reachable from each slightly lower location
    new_trail_map: dict[tuple[int, int], set[tuple[int, int]]]
    # Ratings for each slightly lower location
    new_trail_ratings: dict[tuple[int, int], int]

    # Init trailheads from peaks to themselves
    for y, row in enumerate(area_map):
        for x, point in enumerate(row):
            if int(point) == peak_height:
                trail_map[(x, y)].add((x, y))
                trail_ratings[(x, y)] = 1

    # Find all trailheads for each slightly lower height
    for height in range(9, 0, -1):
        new_trail_map, new_trail_ratings = defaultdict(set), defaultdict(int)
        for (x, y), peaks in trail_map.items():
            for dx, dy in neighbors:
                # Find all slightly lower neighbors
                nx, ny = x + dx, y + dy
                if not (0 <= nx < sx and 0 <= ny < sy):
                    continue
                if int(area_map[ny][nx]) != height - 1:
                    continue
                # Each of these neighbors can reach the peaks of the current location
                new_trail_map[(nx, ny)].update(peaks)
                new_trail_ratings[(nx, ny)] += trail_ratings[(x, y)]
        trail_map = new_trail_map
        trail_ratings = new_trail_ratings

    score = sum(len(peaks) for peaks in trail_map.values())
    rating = sum(trail_ratings.values())

    return score, rating


def run(input_path: str) -> None:
    area_map = read_input(input_path)
    trailheads_score, trailheads_rating = get_trailheads_scores_and_ratings(area_map)
    print(f"Trailheads score = {trailheads_score}")
    print(f"Trailheads rating = {trailheads_rating}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

import os
import sys
from collections import defaultdict

from utils.input_parsing import input_to_2d_array

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[list[str]]:
    return input_to_2d_array(path)


def get_fence_cost(area_map: list[list[str]]) -> tuple[int, int]:
    total_base_cost = 0
    total_discounted_cost = 0
    for y, row in enumerate(area_map):
        for x, point in enumerate(row):
            if point == "":
                continue
            base_cost, discounted_cost = get_area_cost(area_map, x, y)
            total_base_cost += base_cost
            total_discounted_cost += discounted_cost

    return total_base_cost, total_discounted_cost


def get_area_cost(area_map: list[list[str]], x0: int, y0: int) -> tuple[int, int]:
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    value = area_map[y0][x0]
    w, h = len(area_map[0]), len(area_map)

    perimeter = 0
    area_points: set[tuple[int, int]] = set()
    new_points: set[tuple[int, int]] = {(x0, y0)}
    borders_x: dict[int, set[int]] = defaultdict(set)
    borders_y: dict[int, set[int]] = defaultdict(set)

    while new_points:
        x, y = new_points.pop()
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h and area_map[ny][nx] == value):
                perimeter += 1
                if dx != 0:
                    # Multiplying by dx and dy (which equal -1 or +1) is a hack to
                    # distinguish between borders facing in different directions
                    borders_x[max(x, nx)].add(y * dx)
                elif dy != 0:
                    borders_y[max(y, ny)].add(x * dy)
            elif (nx, ny) not in area_points:
                new_points.add((nx, ny))
        area_points.add((x, y))

    clear_area(area_map, area_points)

    sides_count = get_sides_count(borders_x) + get_sides_count(borders_y)
    area = len(area_points)
    return area * perimeter, area * sides_count


def clear_area(area_map: list[list[str]], points: set[tuple[int, int]]) -> None:
    for x, y in points:
        area_map[y][x] = ""


def get_sides_count(borders: dict[int, set[int]]) -> int:
    count = 0
    for border in borders.values():
        prev_piece = None
        for piece in sorted(border):
            if prev_piece is None or piece != prev_piece + 1:
                count += 1
            prev_piece = piece
    return count


def run(input_path: str) -> None:
    area_map = read_input(input_path)
    total_base_cost, total_discounted_cost = get_fence_cost(area_map)
    print(f"Base cost of the fence: {total_base_cost}")
    print(f"Discounted cost of the fence: {total_discounted_cost}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

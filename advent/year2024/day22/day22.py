import os
import sys
from collections import defaultdict

from utils.input_parsing import input_to_array_of_integers

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


type ValuesByDeltasMap = dict[tuple[int, int, int, int], int]
type ValuesMap = dict[int, ValuesByDeltasMap]


def read_input(path: str) -> list[int]:
    return input_to_array_of_integers(path, "\n")


def get_secret(number: int, iterations: int, values_map: ValuesMap) -> int:
    deltas = (0, 0, 0, 0)
    values = (0, 0, 0, 0)
    n = number
    number_values_map: ValuesByDeltasMap = {}
    for i in range(iterations):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216
        value = n % 10
        delta = value - values[-1]
        values = (values[1], values[2], values[3], value)
        deltas = (deltas[1], deltas[2], deltas[3], delta)
        if i >= 3 and deltas not in number_values_map:
            number_values_map[deltas] = value
    values_map[number] = number_values_map
    return n


def get_result(numbers: list[int], iterations: int) -> tuple[int, int]:
    values_map: ValuesMap = {}
    secrets_sum = sum(get_secret(number, iterations, values_map) for number in numbers)

    values_by_deltas_map: ValuesByDeltasMap = defaultdict(int)
    for number_values_map in values_map.values():
        for deltas, value in number_values_map.items():
            values_by_deltas_map[deltas] += value

    return secrets_sum, max(values_by_deltas_map.values())


def run(input_path: str) -> None:
    numbers = read_input(input_path)
    iterations = 2000

    secrets_sum, bananas_count = get_result(numbers, iterations)
    print(f"Secret after {iterations} iterations = {secrets_sum}")
    print(f"Bananas after {iterations} iterations = {bananas_count}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

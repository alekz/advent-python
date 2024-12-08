import os
import sys
from itertools import product

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[tuple[int, list[int]]]:
    input_data = []
    with open(path) as f:
        for line in f:
            value, numbers = list(map(str.strip, line.split(":")))
            value = int(value)
            numbers = list(map(int, map(str.strip, numbers.split(" "))))
            input_data.append((value, numbers))

    return input_data


def is_equal(
    expected_value: int, numbers: list[int], operators: tuple[str, ...]
) -> bool:
    value = numbers[0]
    for i in range(1, len(numbers)):
        operator = operators[i - 1]
        if operator == "+":
            value += numbers[i]
        elif operator == "*":
            value *= numbers[i]
        elif operator == "|":
            value = int(f"{value}{numbers[i]}")
    return value == expected_value


def is_true_value(value: int, numbers: list[int], operators_list: str) -> bool:
    operators_count = len(numbers) - 1
    operators_combinations = product(operators_list, repeat=operators_count)
    for operators in operators_combinations:
        if is_equal(value, numbers, operators):
            return True
    return False


def run(input_path: str) -> None:
    rows = read_input(input_path)
    total_value = 0
    real_total_value = 0
    for value, numbers in rows:
        if is_true_value(value, numbers, "+*"):
            total_value += value
        if is_true_value(value, numbers, "+*|"):
            real_total_value += value
    print(f"Total = {total_value}")
    print(f"Real total = {real_total_value}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

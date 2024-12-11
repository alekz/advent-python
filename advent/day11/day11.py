import os
import sys
from collections import defaultdict

from utils.input_parsing import input_to_array_of_integers

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[int]:
    return input_to_array_of_integers(path)


def blink(numbers: list[int], times: int = 1) -> int:
    cache: dict[int, list[int]] = defaultdict(list)
    count = 0
    for t in range(times + 1):
        count = sum(get_count_after_blinks(number, t, cache) for number in numbers)
    return count


def get_count_after_blinks(number, times, cache) -> int:
    if len(cache[number]) > times:
        pass
    elif times == 0:
        cache[number].append(1)
    else:
        count = sum(
            get_count_after_blinks(new_number, times - 1, cache)
            for new_number in blink_once(number)
        )
        cache[number].append(count)
    return cache[number][times]


def blink_once(number: int) -> list[int]:
    if number == 0:
        return [1]
    number_str = str(number)
    number_len = len(number_str)
    if number_len % 2 == 1:
        return [2024 * number]
    return [
        int(number_str[0 : number_len // 2]),
        int(number_str[number_len // 2 :]),
    ]


def run(input_path: str) -> None:
    numbers = read_input(input_path)
    for n in [25, 75]:
        result = blink(numbers, n)
        print(f"Number of stones after {n} blinks = {result}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

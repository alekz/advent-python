import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> tuple[list[int], list[int]]:
    list1, list2 = [], []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            numbers = list(filter(None, line.split(" ")))
            if len(numbers) != 2:
                print(f"Warning: unexpected line\n> {line}")
                continue
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))
    return sorted(list1), sorted(list2)


def run(input_path: str) -> None:
    list1, list2 = read_input(input_path)

    n = len(list1)

    sum_distances = 0
    for i in range(n):
        a, b = list1[i], list2[i]
        distance = abs(b - a)
        sum_distances += distance

    print(f"Total distance = {sum_distances}")

    similarity = 0
    j, prev_j = 0, 0
    prev_value = None
    occurrences = 0
    for i, value in enumerate(list1):
        if prev_value is None or prev_value != value:
            occurrences = 0
            while j < n and list2[j] < value:
                j += 1
            while j < n and list2[j] == value:
                occurrences += 1
                j += 1
        prev_j, prev_value = j, value
        similarity += value * occurrences

    print(f"Similarity score = {similarity}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> tuple[list[int], list[int]]:
    list1, list2 = [], []

    with open(path) as f:
        for line in f:
            a, b = list(filter(None, line.strip().split(" ")))
            list1.append(int(a))
            list2.append(int(b))
    return sorted(list1), sorted(list2)


def get_sum_distances(list1: list[int], list2: list[int]) -> int:
    return sum(abs(b - a) for a, b in zip(list1, list2))


def get_similarity_score(list1: list[int], list2: list[int]) -> int:
    n = len(list1)

    similarity = 0
    i = 0
    prev_value = None
    occurrences = 0
    for value in list1:
        if prev_value is None or prev_value != value:
            occurrences = 0
            while i < n and list2[i] < value:
                i += 1
            while i < n and list2[i] == value:
                occurrences += 1
                i += 1
        prev_value = value
        similarity += value * occurrences
    return similarity


def run(input_path: str) -> None:
    list1, list2 = read_input(input_path)

    sum_distances = get_sum_distances(list1, list2)
    print(f"Total distance = {sum_distances}")

    similarity = get_similarity_score(list1, list2)
    print(f"Similarity score = {similarity}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

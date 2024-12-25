import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type Lock = list[int]


def read_input(path: str) -> tuple[list[Lock], list[Lock]]:
    locks: list[Lock] = []
    keys: list[Lock] = []
    with open(path) as f:
        lock_strings = f.read().strip().split("\n\n")
    for lock_string in lock_strings:
        lock_rows = lock_string.strip().split("\n")
        is_lock = lock_rows[0][0] == "#"
        lock_or_key = [0] * len(lock_rows[0])
        for row in lock_rows[1:-1]:
            for i, char in enumerate(row):
                if char == "#":
                    lock_or_key[i] += 1
        (locks if is_lock else keys).append(lock_or_key)
    return locks, keys


def key_fits(lock: Lock, key: Lock, max_height: int = 5) -> bool:
    for i, pin in enumerate(lock):
        if pin + key[i] > max_height:
            return False
    return True


def count_fitting_pairs(locks: list[Lock], keys: list[Lock]) -> int:
    return sum(1 for lock in locks for key in keys if key_fits(lock, key))


def run(input_path: str) -> None:
    locks, keys = read_input(input_path)
    fitting_pairs_count = count_fitting_pairs(locks, keys)
    print(f"Fitting pairs: {fitting_pairs_count}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

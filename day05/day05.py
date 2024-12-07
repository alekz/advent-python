import os
import sys
from collections import defaultdict

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    rules: dict[int, set[int]] = defaultdict(set)
    updates: list[list[int]] = []

    is_updates = False
    with open(path) as f:
        for line in f:
            line = line.strip()

            if not line:
                if is_updates:
                    break
                else:
                    is_updates = True
                    continue

            if is_updates:
                updates.append(list(map(int, line.split(","))))
            else:
                page1, page2 = list(map(int, line.split("|")))
                rules[page1].add(page2)

    return rules, updates


def update_matches_rules(update: list[int], rules: dict[int, set[int]]) -> bool:
    n = len(update)
    for i in range(n):
        page1 = update[i]
        for j in range(i + 1, n):
            page2 = update[j]
            if page2 in rules and page1 in rules[page2]:
                return False
    return True


def correct_update(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    for i in range(1, len(update)):
        page1 = update[i]
        for j in range(i):
            page2 = update[j]
            if page2 in rules and page1 in rules[page2]:
                for k in range(i, j, -1):
                    update[k] = update[k - 1]
                update[j] = page1
                break
    return update


def run(input_path: str) -> None:
    rules, updates = read_input(input_path)

    total = 0
    corrected_total = 0
    for update in updates:
        if update_matches_rules(update, rules):
            total += update[int(len(update) / 2)]
        else:
            update = correct_update(update, rules)
            corrected_total += update[int(len(update) / 2)]

    print(f"Total = {total}")
    print(f"Corrected total = {corrected_total}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

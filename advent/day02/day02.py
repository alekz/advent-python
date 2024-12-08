import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[list[int]]:
    reports = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            numbers = list(map(int, filter(None, line.split(" "))))
            reports.append(numbers)
    return reports


def is_safe_report(report: list[int]) -> bool:
    is_increasing_report = None
    prev_value = None
    for i, value in enumerate(report):
        if i == 0:
            prev_value = value
            continue

        is_increasing_pair = value > prev_value

        if is_increasing_report is None:
            is_increasing_report = is_increasing_pair

        if is_increasing_pair != is_increasing_report:
            return False

        diff = abs(value - prev_value)
        if diff < 1 or diff > 3:
            return False

        prev_value = value

    return True


def is_real_safe_report(report: list[int]) -> bool:
    if is_safe_report(report):
        return True

    for i in range(len(report)):
        dampened_report = report[0:i] + report[i + 1 :]
        if is_safe_report(dampened_report):
            return True

    return False


def run(input_path: str) -> None:
    reports = read_input(input_path)

    safe_reports = 0
    for report in reports:
        if is_safe_report(report):
            safe_reports += 1

    print(f"Safe reports = {safe_reports}")

    real_safe_reports = 0
    for report in reports:
        if is_real_safe_report(report):
            real_safe_reports += 1

    print(f"Real safe reports = {real_safe_reports}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

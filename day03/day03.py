import os
import re
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> str:
    with open(path) as f:
        return f.read()


def run_program(program: str) -> int:
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", program)
    return sum(int(a) * int(b) for a, b in matches)


def real_run_program(program: str) -> int:
    stop_command = "don't()"
    start_command = "do()"

    result = 0
    start_location = 0
    while True:
        is_end_of_program = False

        # Find next stop
        stop_location = program.find(stop_command, start_location)
        if stop_location < 0:
            stop_location = len(program)
            is_end_of_program = True

        # Run from start to next stop
        result += run_program(program[start_location:stop_location])

        if is_end_of_program:
            break

        # Find next start
        start_location = program.find(start_command, stop_location + len(stop_command))
        if start_location < 0:
            break
        else:
            start_location += len(start_command)

    return result


def run(input_path: str) -> None:
    program = read_input(input_path)
    result = run_program(program)
    print(f"Program result = {result}")
    real_result = real_run_program(program)
    print(f"Program real result = {real_result}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

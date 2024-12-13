import os
import re
import sys
from collections import namedtuple

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Machine = namedtuple("Machine", ["ax", "ay", "bx", "by", "px", "py"])


def read_input(path: str) -> list[Machine]:
    with open(path) as f:
        text = f.read()
    pattern = (
        r"Button A: X\+(\d+), Y\+(\d+)\n"
        r"Button B: X\+(\d+), Y\+(\d+)\n"
        r"Prize: X=(\d+), Y=(\d+)"
    )
    return [Machine(*map(int, match)) for match in re.findall(pattern, text)]


def get_machine_coins(machine: Machine, dx: int = 0, dy: int = 0) -> int:
    ax, ay, bx, by, px, py = machine
    px, py = px + dx, py + dy
    an = (py * bx - px * by) / (ay * bx - ax * by)
    if an % 1 != 0:
        return 0
    bn = (px - ax * an) / bx
    if bn % 1 != 0:
        return 0
    return int(3 * an + 1 * bn)


def run(input_path: str) -> None:
    machines = read_input(input_path)
    coins = sum(get_machine_coins(m) for m in machines)
    print(f"Coins (part 1) = {coins}")
    coins = sum(get_machine_coins(m, 10000000000000, 10000000000000) for m in machines)
    print(f"Coins (part 2) = {coins}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

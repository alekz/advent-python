import os
import re
import sys
from copy import deepcopy

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


class Computer:
    def __init__(self, a: int, b: int, c: int, program: list[int]) -> None:
        self.a, self.b, self.c = a, b, c
        self.program = program
        self.pointer: int = 0
        self.instructions = [
            self._adv,
            self._bxl,
            self._bst,
            self._jnz,
            self._bxc,
            self._out,
            self._bdv,
            self._cdv,
        ]
        self.output: list[int] = []

    def run(self) -> None:
        while True:
            instruction_code = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            instruction = self.instructions[instruction_code]
            # noinspection PyArgumentList
            new_pointer = instruction(operand)
            self.pointer = new_pointer if new_pointer is not None else self.pointer + 2
            if self.pointer >= len(self.program):
                return

    def from_combo(self, value: int) -> int:
        if value <= 3:
            return value
        if value == 4:
            return self.a
        if value == 5:
            return self.b
        if value == 6:
            return self.c
        return 0

    def _adv(self, operand: int) -> int | None:  # 0
        self.a = self.a // (2 ** self.from_combo(operand))
        return None

    def _bxl(self, operand: int) -> int | None:  # 1
        self.b = self.b ^ operand
        return None

    def _bst(self, operand: int) -> int | None:  # 2
        self.b = self.from_combo(operand) % 8
        return None

    def _jnz(self, operand: int) -> int | None:  # 3
        return None if self.a == 0 else operand

    def _bxc(self, operand: int) -> int | None:  # 4
        self.b = self.b ^ self.c
        return None

    def _out(self, operand: int) -> int | None:  # 5
        self.output.append(self.from_combo(operand) % 8)
        return None

    def _bdv(self, operand: int) -> int | None:  # 6
        self.b = self.a // (2 ** self.from_combo(operand))
        return None

    def _cdv(self, operand: int) -> int | None:  # 7
        self.c = self.a // (2 ** self.from_combo(operand))
        return None

    def __str__(self) -> str:
        return f"A={self.a}, B={self.b}, C={self.c}, Pointer={self.pointer}, Program={self.program}, Output={self.output}"


def read_input(path: str) -> Computer:
    with open(path) as f:
        text = f.read()

    pattern = (
        r"^Register A: (\d+)\n"
        r"Register B: (\d+)\n"
        r"Register C: (\d+)\n\n"
        r"Program: (\d+(?:,\d+)*)\s*$"
    )
    match = re.match(pattern, text)
    if match:
        return Computer(
            int(match[1]),
            int(match[2]),
            int(match[3]),
            list(map(int, match[4].split(","))),
        )
    return Computer(0, 0, 0, [])


def combine_valid_values(prev: list[int], this: list[int], index: int = 0) -> list[int]:
    bits = 3 * index
    values = set()
    for x in this:
        x_test = x & 0b1111111
        for y in prev:
            y_test = y >> bits
            is_compatible = (x_test ^ y_test) == 0
            if is_compatible:
                values.add((x << bits) | y)
    return list(sorted(values))


def find_self_printing_program(computer: Computer) -> int:
    original_computer = computer
    base_a_values = range(2**10)
    combined_valid_a_values = []

    for i, number in enumerate(original_computer.program):
        valid_a_values = []
        for a in base_a_values:
            computer = deepcopy(original_computer)
            computer.a = a
            computer.run()
            if computer.output[0] == number:
                valid_a_values.append(a)
        if i == 0:
            combined_valid_a_values = valid_a_values[:]
        else:
            combined_valid_a_values = combine_valid_values(
                combined_valid_a_values, valid_a_values, i
            )

    for a in combined_valid_a_values:
        computer = deepcopy(original_computer)
        computer.a = a
        computer.run()
        if computer.program == computer.output:
            return a

    return -1


def run(input_path: str) -> None:
    original_computer = read_input(input_path)

    computer = deepcopy(original_computer)
    computer.run()
    print("Output:", ",".join(map(str, computer.output)))

    a = find_self_printing_program(original_computer)
    print(f"Min self-printing A: {a}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

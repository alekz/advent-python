import os
import sys
from collections import namedtuple
from copy import copy

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

Gate = namedtuple("Gate", ["op", "x", "y", "z"])


def read_input(path: str) -> tuple[dict[str, int], list[Gate]]:
    with open(path) as f:
        inputs_text, gates_text = f.read().strip().split("\n\n")

    inputs = {}
    for input_text in inputs_text.strip().split("\n"):
        wire, value_str = input_text.split(": ")
        inputs[wire] = int(value_str)

    gates = []
    for gate_text in gates_text.strip().split("\n"):
        parts = gate_text.split(" ")
        gates.append(Gate(parts[1], parts[0], parts[2], parts[4]))

    return inputs, gates


def calc(op: str, x: int, y: int) -> int:
    if op == "AND":
        return x & y
    if op == "OR":
        return x | y
    if op == "XOR":
        return x ^ y
    return 0


def get_output(inputs: dict[str, int], gates: list[Gate]) -> int:
    gates_queue = set(gates)
    while gates_queue:
        for gate in copy(gates_queue):
            op, x, y, z = gate
            if x not in inputs or y not in inputs:
                continue
            a, b = inputs[x], inputs[y]
            inputs[z] = calc(op, a, b)
            gates_queue.remove(gate)

    output = 0
    for wire, value in inputs.items():
        if value and wire[0] == "z":
            bit = int(wire[1:])
            output |= 1 << bit
    return output


def get_swapped_gates() -> str:
    # Swap pairs were found semi-manually by printing x/y/z gates sorted by bit number
    # and searching for broken patterns
    swap_pairs = {
        "nbf": "z30",
        "z30": "nbf",
        "gbf": "z09",
        "z09": "gbf",
        "hdt": "z05",
        "z05": "hdt",
        "mht": "jgt",
        "jgt": "mht",
    }
    return ",".join(sorted(swap_pairs.keys()))


def run(input_path: str) -> None:
    inputs, gates = read_input(input_path)
    output = get_output(inputs, gates)
    print(f"Output = {output}")

    swapped_gates = get_swapped_gates()
    print(f"Swapped gates: {swapped_gates}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

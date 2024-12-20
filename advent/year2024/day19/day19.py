import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")

type PatternMap = dict[str, PatternMap]


def read_input(path: str) -> tuple[list[str], list[str]]:
    with open(path) as f:
        patterns_text, designs_text = f.read().split("\n\n")
    patterns = list(map(str.strip, patterns_text.strip().split(",")))
    designs = list(map(str.strip, designs_text.strip().split("\n")))
    return patterns, designs


def get_pattern_map(patterns: list[str]) -> PatternMap:
    pattern_map: PatternMap = {}
    for pattern in patterns:
        m = pattern_map
        for c in pattern:
            if c not in m:
                m[c] = {}
            m = m[c]
        m["."] = {}
    return pattern_map


def get_possible_design_options(
    design: str,
    offset: int,
    patterns: PatternMap,
    subpatterns: PatternMap,
    design_cache: dict[str, int] | None = None,
) -> int:
    if design_cache is None:
        design_cache = {}
    if offset >= len(design):
        return 1 if "." in subpatterns else 0
    letter = design[offset]
    design_tail = design[offset:]
    options_count = 0
    if letter in subpatterns:
        options_count += get_possible_design_options(
            design, offset + 1, patterns, subpatterns[letter], design_cache
        )
    if "." in subpatterns:
        if design_tail not in design_cache:
            design_cache[design_tail] = get_possible_design_options(
                design, offset, patterns, patterns, design_cache
            )
        options_count += design_cache[design_tail]
    return options_count


def get_possible_designs_count(
    patterns: list[str], designs: list[str]
) -> tuple[int, int]:
    pattern_map = get_pattern_map(patterns)
    possible_designs = 0
    possible_options = 0
    for design in designs:
        design_options_count = get_possible_design_options(
            design, 0, pattern_map, pattern_map
        )
        possible_options += design_options_count
        if design_options_count > 0:
            possible_designs += 1
    return possible_designs, possible_options


def run(input_path: str) -> None:
    patterns, designs = read_input(input_path)
    designs_count, options_count = get_possible_designs_count(patterns, designs)
    print(f"Possible designs count = {designs_count}")
    print(f"Possible options count = {options_count}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

import os
import sys

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> list[str]:
    lines = []
    with open(path) as f:
        for line in f:
            lines.append(line)
    return lines


def count_word(data: list[str], word: str) -> int:
    width, height = len(data[0]), len(data)
    word_len = len(word)
    first_letter = word[0]

    # Delta, Min, Max
    directions_x = [
        (0, 0, width - 1),
        (-1, word_len - 1, width - 1),
        (+1, 0, width - word_len),
    ]
    directions_y = [
        (0, 0, height - 1),
        (-1, word_len - 1, height - 1),
        (+1, 0, height - word_len),
    ]

    count = 0
    for y in range(height):
        for x in range(width):
            if data[y][x] != first_letter:
                continue
            for dx, x_min, x_max in directions_x:
                if x < x_min or x_max < x:
                    continue
                for dy, y_min, y_max in directions_y:
                    if dx == 0 and dy == 0:
                        continue
                    if y < y_min or y_max < y:
                        continue
                    is_word = True
                    for i in range(1, word_len):
                        lx = x + dx * i
                        ly = y + dy * i
                        letter = data[ly][lx]
                        if letter != word[i]:
                            is_word = False
                            break
                    if is_word:
                        count += 1

    return count


def count_x_mas(data: list[str]) -> int:
    width, height = len(data[0]), len(data)

    diagonals = [("M", "S"), ("S", "M")]

    count = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if data[y][x] != "A":
                continue
            diagonal_a = data[y - 1][x - 1], data[y + 1][x + 1]
            diagonal_b = data[y - 1][x + 1], data[y + 1][x - 1]
            if diagonal_a in diagonals and diagonal_b in diagonals:
                count += 1

    return count


def run(input_path: str) -> None:
    data = read_input(input_path)
    count1 = count_word(data, "XMAS")
    print(f"XMAS count = {count1}")
    count2 = count_x_mas(data)
    print(f"X-MAS count = {count2}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

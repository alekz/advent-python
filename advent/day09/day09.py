import os
import sys
from copy import copy

INPUT_PATH = os.path.join(os.path.dirname(__file__), "input.txt")


def read_input(path: str) -> str:
    with open(path) as f:
        return f.read().strip()


def get_disk_data(disk_map: str) -> list[int]:
    data = []
    file_id = 0
    is_file = True
    for x in disk_map:
        file_size = int(x)
        block_id = file_id if is_file else -1
        for i in range(file_size):
            data.append(block_id)
        if is_file:
            file_id += 1
        is_file = not is_file
    return data


def compact_disk_data(data: list[int]) -> None:
    a, b = 0, len(data) - 1
    while True:
        while data[a] >= 0:
            a += 1
        while data[b] < 0:
            b -= 1
        if a > b:
            break
        data[a], data[b] = data[b], data[a]


def compact_disk_data_whole_files(data: list[int]) -> None:
    # Process files from right to left
    file_end = len(data) - 1
    file_id = data[-1]
    while True:
        # Find location and size of currently processed file
        while data[file_end] != file_id:
            file_end -= 1
        file_start = file_end
        while data[file_start - 1] == file_id:
            file_start -= 1
        file_size = file_end - file_start + 1

        # Find location of free space that can fit the file
        space_start = 0
        while True:
            # Find location of the next free space block
            while data[space_start] != -1:
                space_start += 1
            if space_start > file_start:
                break

            # Find size of the next free space block
            space_end = space_start
            space_size = 1
            while space_size < file_size and data[space_end + 1] == -1:
                space_end += 1
                space_size += 1

            # Move file to the free space if there is enough of it
            if space_size >= file_size:
                for i in range(file_size):
                    data[space_start + i] = data[file_start + i]
                    data[file_start + i] = -1
                break

            # Find next free space block
            space_start = space_end + 1

        # Process next file
        file_id -= 1
        file_end = file_start - 1
        # Skip file ID = 0 because it's at the leftmost location of the disk
        if file_id <= 0:
            break


def get_check_sum(data: list[int]) -> int:
    return sum(i * x for i, x in enumerate(data) if x >= 0)


def run(input_path: str) -> None:
    disk_map = read_input(input_path)
    data = get_disk_data(disk_map)
    data_whole_files = copy(data)

    compact_disk_data(data)
    check_sum = get_check_sum(data)
    print(f"Checksum 1 = {check_sum}")

    compact_disk_data_whole_files(data_whole_files)
    check_sum_whole_files = get_check_sum(data_whole_files)
    print(f"Checksum 2 = {check_sum_whole_files}")


def main() -> None:
    input_path = sys.argv[1] if len(sys.argv) > 1 else INPUT_PATH
    run(input_path)


if __name__ == "__main__":
    main()

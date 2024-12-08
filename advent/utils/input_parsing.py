def input_to_2d_array(path: str) -> list[list[str]]:
    array = []
    with open(path) as f:
        for line in f:
            array.append(list(line.strip()))
    return array


def input_to_array_of_strings(path: str) -> list[str]:
    array = []
    with open(path) as f:
        for line in f:
            array.append(line.strip())
    return array

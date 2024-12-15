def input_to_2d_array(path: str) -> list[list[str]]:
    array = []
    with open(path) as f:
        for line in f:
            array.append(list(line.strip()))
    return array


def str_to_2d_array(text: str) -> list[list[str]]:
    return list(map(lambda x: list(x.strip()), text.strip().split("\n")))


def input_to_array_of_strings(path: str) -> list[str]:
    array = []
    with open(path) as f:
        for line in f:
            array.append(line.strip())
    return array


def input_to_array_of_integers(path: str, separator=" ") -> list[int]:
    with open(path) as f:
        return list(map(int, filter(None, map(str.strip, f.read().split(separator)))))

import pathlib
from typing import Union


def load_code(filename: Union[str, pathlib.Path]) -> str:
    with open(filename, "r") as f:
        lines = f.read()
    return lines


def write_code(filename: Union[str, pathlib.Path], text: str):
    with open(filename, "w") as f:
        f.write(text)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

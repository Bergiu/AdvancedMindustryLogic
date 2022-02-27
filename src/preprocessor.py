import re
import pathlib
from typing import List, Union, Dict, Tuple

from src.utils import load_code


LinesOfCode = List[str]
LineNumber = int
Filename = str
CodeLine = Tuple[LineNumber, Filename]
CodePosResolver = List[CodeLine]
AlreadyIncluded = List[Filename]


class File:
    def __init__(self, filename, lines_of_code):
        self.filename = filename
        self.lines_of_code = lines_of_code


def preprocess(text: str, filename: str) -> Tuple[str, CodePosResolver]:
    lines, code_pos = _preprocess_intern(text, filename, [])
    text = "\n".join(lines)
    text = repair_eof(text)
    return text, code_pos


def _preprocess_intern(text: str, filename: Union[str, pathlib.Path], already_included: AlreadyIncluded) -> Tuple[LinesOfCode, CodePosResolver]:
    return replace_includes(text, filename, already_included)


def repair_eof(text) -> str:
    if text[len(text) - 1] != "\n":
        text += "\n"
    return text


def replace_includes(text: str, filename: Union[str, pathlib.Path], already_included: AlreadyIncluded) -> Tuple[LinesOfCode, CodePosResolver]:
    lines = text.split("\n")
    new_lines = []
    code_pos: CodePosResolver = []
    for index, line in enumerate(lines):
        line = line.strip()
        res = re.match("^import ([a-zA-Z0-9/_.]+)[ ]?", line)
        if res is not None:
            new_filename = res.group(1)
            new_abs_name = pathlib.Path(filename).parent.joinpath(new_filename).resolve()
            if new_abs_name in already_included:
                new_lines.append("# " + line + " already included")
                code_pos.append((index, filename))
            else:
                already_included.append(new_abs_name)
                code_pos.append((index, filename))
                new_lines.append("# " + line)
                relative_file = pathlib.Path(filename).parent.joinpath(new_filename)
                imported_code = load_code(relative_file)
                processed_code, new_code_pos = _preprocess_intern(imported_code, relative_file, already_included)
                new_lines.extend(processed_code)
                code_pos.extend(new_code_pos)
        else:
            new_lines.append(line)
            code_pos.append((index, filename))
    return (new_lines, code_pos)

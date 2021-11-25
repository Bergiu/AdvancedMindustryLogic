import ply.yacc as yacc
from src.lexer import *
from src.utils import find_column
from src.parser.types import *
from src.nodes import *
from .grammar import *

start = 'codeblock'


LINT = False
CODE_POS = []


def setup(lint: bool, code_pos: CodePosResolver):
    global LINT, CODE_POS
    LINT = lint
    CODE_POS = code_pos


def p_error(p):
    if p is None:
        raise Exception("Unexpected end of file.")
    msg = f"Syntax error! Error on token: {repr(p.value)} ({p.type})"
    make_error(p, "error", msg)


def make_error(p, type, message):
    global CODE_POS, LINT
    column = find_column(p.lexer.lexdata, p)
    form = "{path}:{line}:{column}: {type}: {msg}"
    lineno, filename = CODE_POS[p.lineno - 1]
    formatted = form.format(path=filename, line=lineno + 1, column=column, type=type, msg=message)
    if LINT:
        print(formatted)
    else:
        raise Exception(formatted)


parser = yacc.yacc()


def do_parsing(text):
    result = parser.parse(text)
    return result

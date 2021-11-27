#!/bin/python3
import sys

from src.preprocessor import preprocess, CodePosResolver
from src.utils import load_code, write_code
from src.parser import setup as setupp, do_parsing
from src.lexer import setup as setupl, do_lexing
from src.nodes import setup as setupn

import argparse


def load_args():
    parser = argparse.ArgumentParser(description='Advanced Mindusty Logic Compiler.')
    parser.add_argument('filename', type=str, help='The file that should be compiled.')
    parser.add_argument('-o', dest='outfile', nargs="?", action='store',
                        default=None, help='The output file.', type=str)
    parser.add_argument('--linter', dest='linter', action='store_true',
                        default=False, help='If only the linter should be run.')
    parser.add_argument('--loc', dest='loc', action='store_true',
                        default=False, help='Only show amount of lines of code.')
    return parser.parse_args()


def setup(lint: bool, code_pos: CodePosResolver):
    setupl(lint, code_pos)
    setupp(lint, code_pos)
    setupn(lint, code_pos)


def main():
    # needed because python linked lists can only have ~1000 elements
    sys.setrecursionlimit(2000)
    args = load_args()
    text = load_code(args.filename)
    text, code_pos = preprocess(text, args.filename)
    setup(args.linter, code_pos)
    # print(do_lexing(text))
    out = do_parsing(text)
    if out.loc() > 1000:
        raise Exception("PANIC: Maximum lines of code exceeded (max: 1000).")
    code = out.to_code(out)
    if args.loc:
        print(out.loc())
        return
    if not args.linter:
        if args.outfile is not None:
            write_code(args.outfile, code)
        else:
            print(code)


if __name__ == '__main__':
    main()
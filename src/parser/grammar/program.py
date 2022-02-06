"""
This module contains some specific grammar rules, that are needed for mindustry code.

This contains:
codeblock       # list of lines (CodeBlockNode).
lineend         # newline or a comment.
line            # an instruction or a lineend
instruction     # a collection of all instructions including default instructions, operators and new features.
"""


from src.parser.types import *
from src.nodes import *


def p_program1(p):
    '''codeblock : line'''
    line: line_t = p[1]
    p[0] = CodeBlockNode(p, line)


def p_program2(p):
    '''codeblock : codeblock line'''
    codeblock: codeblock_t = p[1]
    line: line_t = p[2]
    p[0] = CodeBlockNode(p, line, codeblock)


def p_lineend1(p):
    '''lineend : NEWLINE'''
    newline: Token = Token(p.slice[1])
    p[0] = NewLineNode(p, newline)


def p_lineend2(p):
    '''lineend : COMMENT NEWLINE'''
    comment: Token = Token(p.slice[1])
    p[0] = CommentNode(p, comment)


def p_line(p):
    '''line : instruction lineend'''
    instruction: instruction_t = p[1]
    lineend: lineend_t = p[2]
    p[0] = OneLineNode(p, instruction, lineend)


def p_line1(p):
    '''line : lineend'''
    lineend: lineend_t = p[1]
    p[0] = lineend


def p_line_error(p):
    '''line : error NEWLINE'''
    p[0] = ErrorNode(p)
    p.parser.errok()


def p_instruction(p):
    '''instruction : cmd_write
                   | cmd_read
                   | cmd_draw
                   | cmd_drawflush
                   | cmd_print
                   | cmd_printflush
                   | cmd_getlink
                   | cmd_control
                   | cmd_radar
                   | cmd_sensor
                   | cmd_set
                   | cmd_op
                   | cmd_end
                   | cmd_jump
                   | cmd_ubind
                   | cmd_ucontrol
                   | cmd_uradar
                   | cmd_ulocate
                   | cmd_noop
                   | cmd_exec
                   | cmd_op_short
                   | cmd_function
                   | cmd_while
                   | cmd_if
                   | cmd_if_else
                   | cmd_label
    '''
    instruction: instruction_t = p[1]
    p[0] = instruction

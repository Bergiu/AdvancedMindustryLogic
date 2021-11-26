"""
Arithmetic operators:
x = a + b  # Addition
x = a - b  # Subtraction
x = a * b  # Multiplication
x = a / b  # Division
x++        # Increment
x--        # Decrement

Assignment operators:
x = a   # Direct assignment
x += a  # Addition assignment
x -= a  # Subtraction assignment
x *= a  # Multiplication assignment
x /= a  # Division assignment
TODO:
x %= a   # Modulo assignment
x **= a  # Power assignment
x &= a   # Bitwise and assignment
x |= a   # Bitwise or assignment
x ^= a   # Bitwise xor assignment
x <<= a  # Bitwise left shift assignment
x >>= a  # Bitwise right shift assignment

Comparison operators/relational operators:
x = a == b  # Equal to
x = a != b  # Not equal to
x = a > b   # Greater than
x = a < b   # Less than
x = a >= b  # Greater than or equal to
x = a <= b  # Less than or equal to

Logical operators:
x = ! a      # Logical negation (NOT)
TODO:
x = not a      # Logical negation (NOT)
x = a && b
x = a and b
x = a || b
x = a or b

Bitwise operators:
x = a and b  # Bitwise AND
x = a or b   # Bitwise OR
x = a xor b  # Bitwise XOR
x = a << b   # Bitwise left shift
x = a >> b   # Bitwise right shift
TODO:
x = ~a                  # Bitwise not
x = compl a             # Bitwise not
rename and to &
rename and to bitand
rename or to |
rename or to bitor
rename xor to ^
rename xor to xor

Future Ideas:
a ? b : c               # Ternary operator
a <=> b                 # Three-way comparison
"""
from src.parser.types import value_t, fakeid_t, statement_t
from src.nodes import OperationNode, OperationStatementNode


def p_op_add_reduced(p):
    '''cmd_op_short : fakeid OP_ADD OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_add_reduced_much(p):
    '''cmd_op_short : fakeid OP_ADD OP_ADD'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    rv = "1"
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=rv)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_sub_reduced(p):
    '''cmd_op_short : fakeid OP_SUB OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_sub_reduced_much(p):
    '''cmd_op_short : fakeid OP_SUB OP_SUB'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    rv = "1"
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=rv)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_mul_reduced(p):
    '''cmd_op_short : fakeid OP_MUL OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "mul {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_div_reduced(p):
    '''cmd_op_short : fakeid OP_DIV OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "div {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_set(p):
    '''cmd_op_short : fakeid OP_ASSIGN statement'''
    fakeid: fakeid_t = p[1]
    op: str = f"set {fakeid}"
    statement: statement_t = p[3]
    p[0] = OperationStatementNode(p, op, statement)

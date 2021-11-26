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


def p_op_add(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_ADD value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


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


def p_op_sub(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_SUB value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
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


def p_op_mul(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_MUL value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "mul {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_mul_reduced(p):
    '''cmd_op_short : fakeid OP_MUL OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "mul {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_div(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_DIV value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "div {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_div_reduced(p):
    '''cmd_op_short : fakeid OP_DIV OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "div {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))



def p_op_lt(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_LT value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "lessThan {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_lte(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_LTE value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "lessThanEq {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_gt(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_GT value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "greaterThan {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_gte(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_GTE value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "greaterThanEq {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_eq(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_EQ value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "equal {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_not_equal(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_NOTEQ value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "notEqual {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_strict_equal(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_STRICTEQ value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "strictEqual {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_idiv(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_IDIV value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "idiv {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_mod(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_MOD value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "mod {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_pow(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_POW value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "pow {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_shl(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_SHL value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "shl {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_shr(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OP_SHR value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "shr {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_and(p):
    '''cmd_op_short : fakeid OP_ASSIGN value AND value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "and {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_or(p):
    '''cmd_op_short : fakeid OP_ASSIGN value OR value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "or {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_xor(p):
    '''cmd_op_short : fakeid OP_ASSIGN value XOR value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "xor {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_inverse(p):
    '''cmd_op_short : fakeid OP_ASSIGN OP_INV value'''
    # TODO: use flip operator
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value: value_t = p[4]
    params = "xor {var} true value".format(var=fakeid, value=value)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_set(p):
    '''cmd_op_short : fakeid OP_ASSIGN statement'''
    fakeid: fakeid_t = p[1]
    op: str = f"set {fakeid}"
    statement: statement_t = p[3]
    p[0] = OperationStatementNode(p, op, statement)

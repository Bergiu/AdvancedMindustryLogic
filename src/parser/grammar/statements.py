"""
This module contains statements.

The variables a and b can either be values or other statements. So it's possible to wrap multiple statements into one.
Example:
    if ( (a >= 0) and (a <= (b + 10)) ) {}

Arithmetic operators:
(a + b)  # Addition
(a - b)  # Subtraction
(a * b)  # Multiplication
(a / b)  # Division

Comparison operators/relational operators:
(a == b)  # Equal to
(a != b)  # Not equal to
(a > b)   # Greater than
(a < b)   # Less than
(a >= b)  # Greater than or equal to
(a <= b)  # Less than or equal to

Logical operators:
(! a)      # Logical negation (NOT)
TODO:
(not a)      # Logical negation (NOT)
(a && b)
(a and b)
(a || b)
(a or b)

Bitwise operators:
(a and b)  # Bitwise AND
(a or b)   # Bitwise OR
(a xor b)  # Bitwise XOR
(a << b)   # Bitwise left shift
(a >> b)   # Bitwise right shift
TODO:
(~a)                  # Bitwise not
(compl a)             # Bitwise not
rename and to &
rename and to bitand
rename or to |
rename or to bitor
rename xor to ^
rename xor to xor
"""

from src.nodes import Token, StatementNode
from src.parser.types import statement_t


def p_statement(p):
    '''statement : value'''
    value = Token(p.slice[1])
    p[0] = value


def p_statement_add(p):
    '''statement : LPAREN statement OP_ADD statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "add"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_sub(p):
    '''statement : LPAREN statement OP_SUB statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "sub"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_div(p):
    '''statement : LPAREN statement OP_DIV statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "div"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_mul(p):
    '''statement : LPAREN statement OP_MUL statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "mul"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_lt(p):
    '''statement : LPAREN statement OP_LT statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "lessThan"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_lte(p):
    '''statement : LPAREN statement OP_LTE statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "lessThanEq"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_gt(p):
    '''statement : LPAREN statement OP_GT statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "greaterThan"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_gte(p):
    '''statement : LPAREN statement OP_GTE statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "greaterThanEq"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_eq(p):
    '''statement : LPAREN statement OP_EQ statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "equal"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_not_equal(p):
    '''statement : LPAREN statement OP_NOTEQ statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "notEqual"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_strict_equal(p):
    '''statement : LPAREN statement OP_STRICTEQ statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "strictEqual"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_idiv(p):
    '''statement : LPAREN statement OP_IDIV statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "idiv"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_mod(p):
    '''statement : LPAREN statement OP_MOD statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "mod"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_pow(p):
    '''statement : LPAREN statement OP_POW statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "pow"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_shl(p):
    '''statement : LPAREN statement OP_SHL statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "shl"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_shr(p):
    '''statement : LPAREN statement OP_SHR statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "shr"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_and(p):
    '''statement : LPAREN statement AND statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "and"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_or(p):
    '''statement : LPAREN statement OR statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "or"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_xor(p):
    '''statement : LPAREN statement XOR statement RPAREN'''
    value1: statement_t = p[2]
    value2: statement_t = p[4]
    operation: str = "xor"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_inverse(p):
    '''statement : LPAREN OP_INV statement RPAREN'''
    value1: statement_t = p[3]
    value2: str = "true"
    operation: str = "xor"
    p[0] = StatementNode(p, operation, value1, value2)

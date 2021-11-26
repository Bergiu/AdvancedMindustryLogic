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
    '''statement : LPAREN statement OP_ADD statement RPAREN
                 | statement OP_ADD statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "add"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_sub(p):
    '''statement : LPAREN statement OP_SUB statement RPAREN
                 | statement OP_SUB statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "sub"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_div(p):
    '''statement : LPAREN statement OP_DIV statement RPAREN
                 | statement OP_DIV statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "div"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_mul(p):
    '''statement : LPAREN statement OP_MUL statement RPAREN
                 | statement OP_MUL statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "mul"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_lt(p):
    '''statement : LPAREN statement OP_LT statement RPAREN
                 | statement OP_LT statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "lessThan"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_lte(p):
    '''statement : LPAREN statement OP_LTE statement RPAREN
                 | statement OP_LTE statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "lessThanEq"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_gt(p):
    '''statement : LPAREN statement OP_GT statement RPAREN
                 | statement OP_GT statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "greaterThan"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_gte(p):
    '''statement : LPAREN statement OP_GTE statement RPAREN
                 | statement OP_GTE statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "greaterThanEq"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_eq(p):
    '''statement : LPAREN statement OP_EQ statement RPAREN
                 | statement OP_EQ statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "equal"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_not_equal(p):
    '''statement : LPAREN statement OP_NOTEQ statement RPAREN
                 | statement OP_NOTEQ statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "notEqual"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_strict_equal(p):
    '''statement : LPAREN statement OP_STRICTEQ statement RPAREN
                 | statement OP_STRICTEQ statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "strictEqual"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_idiv(p):
    '''statement : LPAREN statement OP_IDIV statement RPAREN
                 | statement OP_IDIV statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "idiv"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_mod(p):
    '''statement : LPAREN statement OP_MOD statement RPAREN
                 | statement OP_MOD statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "mod"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_pow(p):
    '''statement : LPAREN statement OP_POW statement RPAREN
                 | statement OP_POW statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "pow"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_shl(p):
    '''statement : LPAREN statement OP_SHL statement RPAREN
                 | statement OP_SHL statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "shl"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_shr(p):
    '''statement : LPAREN statement OP_SHR statement RPAREN
                 | statement OP_SHR statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "shr"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_and(p):
    '''statement : LPAREN statement AND statement RPAREN
                 | statement AND statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "and"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_or(p):
    '''statement : LPAREN statement OR statement RPAREN
                 | statement OR statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "or"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_xor(p):
    '''statement : LPAREN statement XOR statement RPAREN
                 | statement XOR statement
    '''
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "xor"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_inverse(p):
    '''statement : LPAREN OP_INV statement RPAREN
                 | OP_INV statement
    '''
    if len(p) > 4:
        value1: statement_t = p[3]
    else:
        value1: statement_t = p[2]
    value2: str = "true"
    operation: str = "xor"
    p[0] = StatementNode(p, operation, value1, value2)


precedence = (
    #('left', 'LOR'), # logical or
    #('left', 'LAND'), # logical and
    # logical or
    # logical and
    # logical not
    ('left', 'OP_EQ', 'OP_NOTEQ', 'OP_STRICTEQ'),
    ('left', 'OP_LT', 'OP_LTE', 'OP_GT', 'OP_GTE'),
    ('left', 'OR'),   # bitwise or
    ('left', 'XOR'),  # bitwise xor
    ('left', 'AND'),  # bitwise and
    ('left', 'OP_SHL', 'OP_SHR'),
    ('left', 'OP_ADD', 'OP_SUB'),
    ('left', 'OP_MUL', 'OP_DIV', 'OP_IDIV', 'OP_MOD'),
    ('right', 'OP_INV'),  # BITWISE NOT
    ('left', 'OP_POW'),  # Change order
)

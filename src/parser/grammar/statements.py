"""
This module contains statements.

WARNING:
    In mindustry code, the `op` subcommands `and`, `or` and `not` are bitwise, but here they are used as logical
    operators. When you want to use bitwise operators you can use `&`, `|` and `~`.
    The `^` operator is displayed in mindustry as power operator, but here this command is used as bitwise XOR. When
    you want to use power operator you can use `**`.

The variables a and b can either be values or other statements. So it's possible to wrap multiple statements into one.
Example:
    if ( (a >= 0) and (a <= (b + 10)) ) {}

Arithmetic operators:
(a + b)  # Addition
(a - b)  # Subtraction
(a * b)  # Multiplication
(a / b)  # Division
(a // b) # Integer Division
(a % b)  # Modulo
(a ** b) # Power

Comparison operators/relational operators:
(a == b)  # Equal to
(a === b) # Equal to and same type
(a != b)  # Not equal to
(a > b)   # Greater than
(a < b)   # Less than
(a >= b)  # Greater than or equal to
(a <= b)  # Less than or equal to

Logical operators:
(not a)      # Logical negation (NOT)
(! a)        # Logical negation (NOT)
(a and b)    # Logical AND.
(a && b)     # Logical AND.
(a or b)     # Logical OR. This compiles to 4 lines of code: not ((not a) and (not b))
(a || b)     # Logical OR. This compiles to 4 lines of code: not ((not a) and (not b))

Bitwise operators:
(a & b)       # Bitwise AND
(a bitand b)  # Bitwise AND
(a | b)       # Bitwise OR
(a bitor b)   # Bitwise OR
(a ^ b)       # Bitwise XOR
(a xor b)     # Bitwise XOR
(a << b)      # Bitwise left shift
(a >> b)      # Bitwise right shift
(~a)          # Bitwise not
(compl a)     # Bitwise not

Precedence:
1.  | `a ** b`                             | Power                                                              | left  |
2.  | `~a`, `compl a`                      | Bitwise NOT                                                        | right |
3.  | `a * b`, `a / b`, `a // b`, `a % b`  | Multiplication, Division, Integer division, Modulo                 | left  |
4.  | `a + b`, `a - b`                     | Addition, Subtraction                                              | left  |
5.  | `a << b`, `a >> b`                   | Left Shift, Right Shift                                            | left  |
6.  | `a & b`, `a bitand b`                | Bitwise AND                                                        | left  |
7.  | `a ^ b`, `a xor b`                   | Bitwise XOR                                                        | left  |
8.  | `a | b`, `a bitor b`                 | Bitwise OR                                                         | left  |
9.  | `a < b`, `a <= b`, `a > b`, `a >= b` | Less Than, Less Than or Equal, Greater Than, Greater Than or Equal | left  |
10. | `a == b`, `a != b`, `a === b`        | Equal, Not Equal, Strict Equal                                     | left  |
11. | `! a`, `not a`                       | Logical NOT                                                        | right |
12. | `a && b`, `a and b`                  | Logical AND                                                        | left  |
13. | `a || b`, `a or b`                   | Logical OR                                                         | left  |
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
    '''statement : LPAREN statement OP_AND statement RPAREN
                 | LPAREN statement BITAND statement RPAREN
                 | statement OP_AND statement
                 | statement BITAND statement
    '''
    # bitwise AND
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "and"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_or(p):
    '''statement : LPAREN statement OP_OR statement RPAREN
                 | LPAREN statement BITOR statement RPAREN
                 | statement OP_OR statement
                 | statement BITOR statement
    '''
    # bitwise OR
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "or"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_xor(p):
    '''statement : LPAREN statement OP_XOR statement RPAREN
                 | LPAREN statement XOR statement RPAREN
                 | statement OP_XOR statement
                 | statement XOR statement
    '''
    # bitwise XOR
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
                 | LPAREN COMPL statement RPAREN
                 | OP_INV statement
                 | COMPL statement
    '''
    # bitwise inverse
    if len(p) > 4:
        value1: statement_t = p[3]
    else:
        value1: statement_t = p[2]
    value2: str = "true"
    operation: str = "xor"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_land(p):
    '''statement : LPAREN statement AND statement RPAREN
                 | LPAREN statement OP_LAND statement RPAREN
                 | statement AND statement
                 | statement OP_LAND statement
    '''
    # logical AND
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    operation: str = "land"
    p[0] = StatementNode(p, operation, value1, value2)


def p_statement_lor(p):
    '''statement : LPAREN statement OR statement RPAREN
                 | LPAREN statement OP_LOR statement RPAREN
                 | statement OR statement
                 | statement OP_LOR statement
    '''
    # logical OR
    # not ((not a) and (not b)) = c
    if len(p) > 4:
        value1: statement_t = p[2]
        value2: statement_t = p[4]
    else:
        value1: statement_t = p[1]
        value2: statement_t = p[3]
    not_a = StatementNode(p, "notEqual", value1, "true")
    not_b = StatementNode(p, "notEqual", value2, "true")
    not_c = StatementNode(p, "land", not_a, not_b)
    p[0] = StatementNode(p, "notEqual", not_c, "true")


def p_statement_not(p):
    '''statement : LPAREN NOT statement RPAREN
                 | LPAREN OP_NOT statement RPAREN
                 | NOT statement
                 | OP_NOT statement
    '''
    # logical inverse
    if len(p) > 4:
        value1: statement_t = p[3]
    else:
        value1: statement_t = p[2]
    value2: str = "true"
    operation: str = "notEqual"
    p[0] = StatementNode(p, operation, value1, value2)


precedence = (
    ('left', 'OR', 'OP_LOR'),      # logical OR
    ('left', 'AND', 'OP_LAND'),    # logical AND
    ('right', 'NOT', 'OP_NOT'),    # logical NOT
    ('left', 'OP_EQ', 'OP_NOTEQ', 'OP_STRICTEQ'),
    ('left', 'OP_LT', 'OP_LTE', 'OP_GT', 'OP_GTE'),
    ('left', 'OP_OR', 'BITOR'),    # bitwise OR
    ('left', 'OP_XOR', 'XOR'),     # bitwise XOR
    ('left', 'OP_AND', 'BITAND'),  # bitwise AND
    ('left', 'OP_SHL', 'OP_SHR'),
    ('left', 'OP_ADD', 'OP_SUB'),
    ('left', 'OP_MUL', 'OP_DIV', 'OP_IDIV', 'OP_MOD'),
    ('right', 'OP_INV', 'COMPL'),  # bitwise NOT
    ('left', 'OP_POW'),
)

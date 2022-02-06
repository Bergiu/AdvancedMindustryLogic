"""
Primitive Types:
int             # int. any number (even negative ones) without a dot.
double          # double. any number (even negative ones) with a dot.
bool            # bool. true or false.
string          # string. wrapped between two "

Combined Types:
number          # int or double
keywords        # language keywords that can be used as variable names, for example: print, set, ...

Variable Types:
id              # variable names.
fakeid          # Any valid identifier for a variable name. (ids + keywords)
value           # string, int, double, bool or fakeid
var_int         # int or fakeid
var_double      # double or fakeid
var_number      # int or double or fakeid
var_bool        # bool or fakeid
var_string      # string or fakeid
null            # value that is ignored (while programming this should have the value 0)

List Types:
ids             # list of values
"""


from src.lexer import reserved
from src.nodes import Token, SignedToken
from src.parser.types import value_t, ids_t, var_int_t, var_number_t, var_bool_t, null_t, number_t, fakeid_t, \
    var_string_t


def p_ids1(p):
    '''ids : value'''
    value: value_t = p[1]
    p[0] = [value]


def p_ids2(p):
    '''ids : ids COMMA value'''
    ids: ids_t = p[1]
    value: value_t = p[3]
    ids.append(value)
    p[0] = ids


def p_ids3(p):
    '''ids : '''
    p[0] = []


def p_var_int(p):
    '''var_int : fakeid
               | int
    '''
    out: var_int_t = p[1]
    p[0] = out


def p_var_number(p):
    '''var_number : fakeid
                  | number
    '''
    out: var_number_t = p[1]
    p[0] = out


def p_var_bool(p):
    '''var_bool : value'''
    out: var_bool_t = p[1]
    p[0] = out


#def p_var_double(p):
#    '''var_double : fakeid
#                  | double
#    '''
#    out: var_string_t = p[1]
#    p[0] = out


#def p_var_string(p):
#    '''var_string : fakeid
#                  | string
#    '''
#    out: var_string_t = p[1]
#    p[0] = out


def p_null(p):
    '''null : value'''
    out: null_t = p[1]
    p[0] = out


def p_value(p):
    '''value : fakeid
             | string
             | number
             | bool
    '''
    out: value_t = p[1]
    p[0] = out


def p_number(p):
    '''number : int
              | double
    '''
    out: number_t = p[1]
    p[0] = out


def p_fakeid(p):
    '''fakeid : id
              | keyword
    '''
    out: fakeid_t = p[1]
    p[0] = out


def p_id(p):
    '''id : ID'''
    p[0] = Token(p.slice[1])


def p_int(p):
    '''int : INT'''
    p[0] = Token(p.slice[1])


def p_int_signed(p):
    '''int : OP_SUB INT'''
    p[0] = SignedToken(p.slice[1], p.slice[2])


def p_double(p):
    '''double : DOUBLE'''
    p[0] = Token(p.slice[1])


def p_double_signed(p):
    '''double : OP_SUB DOUBLE'''
    p[0] = SignedToken(p.slice[1], p.slice[2])


def p_bool(p):
    '''bool : BOOL'''
    p[0] = Token(p.slice[1])


def p_string(p):
    '''string : STRING'''
    p[0] = Token(p.slice[1])


def p_keyword(p):
    p[0] = Token(p.slice[1])


p_keyword.__doc__ = "keyword : " + "\n      | ".join([res for res in reserved.values()])

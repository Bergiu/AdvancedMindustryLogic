from src.lexer import reserved
from src.nodes import Token
from src.parser.types import value_t, ids_t, var_int_t, var_number_t, var_bool_t, null_t, number_t, fakeid_t


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
    # TODO: müsste hier nicht auch fakeid sein???
    out: var_bool_t = p[1]
    p[0] = out


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


def p_double(p):
    '''double : DOUBLE'''
    p[0] = Token(p.slice[1])


def p_bool(p):
    '''bool : BOOL'''
    p[0] = Token(p.slice[1])


def p_string(p):
    '''string : STRING'''
    p[0] = Token(p.slice[1])


def p_keyword(p):
    p[0] = Token(p.slice[1])


p_keyword.__doc__ = "keyword : " + "\n      | ".join([res for res in reserved.values()])

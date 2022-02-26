"""
Conditional structures:
if (condition) { }              # If-Structure
if (condition) { } else { }     # If-Else-Structure

Iteration structures:
while (condition) { }           # While-Loop

Functions:
function name(parameter_list, comma, separated) { }  # Function
exec name(parameter_list, comma, separated) { }      # Executes a function

TODO:
- Return values for functions
- Call functions without `exec`
- For-Loop
- elif

Conditions:
The conditions are evaluated to be equal to 1. This is true for the boolean
value `true`, every string even empty ones and the integer 1. Conditions
can also be statements. For this take a look at the statements module.
"""


from src.parser.types import statement_t, codeblock_t, ids_t, ids_inplace_t, fakeid_t, inplace_typed_value_t, ids_param_t
from src.nodes import Token, IfNode, IfElseNode, WhileNode, FunctionNode, ExecNode, NewObjectNode, StructNode


def p_if(p):
    '''cmd_if : IF statement LCURLY lineend codeblock RCURLY'''
    if_o: Token = Token(p.slice[1])
    statement: statement_t = p[2]
    codeblock: codeblock_t = p[5]
    p[0] = IfNode(p, if_o, statement, codeblock)


def p_if_else(p):
    '''cmd_if_else : IF statement LCURLY lineend codeblock RCURLY ELSE LCURLY lineend codeblock RCURLY'''
    if_o: Token = Token(p.slice[1])
    statement: statement_t = p[2]
    codeblock1: codeblock_t = p[5]
    codeblock2: codeblock_t = p[10]
    p[0] = IfElseNode(p, if_o, statement, codeblock1, codeblock2)


def p_while(p):
    '''cmd_while : WHILE statement LCURLY lineend codeblock RCURLY'''
    while_o: Token = Token(p.slice[1])
    statement: statement_t = p[2]
    codeblock: codeblock_t = p[5]
    p[0] = WhileNode(p, while_o, statement, codeblock)


def p_inplace_param(p):
    '''inplace_param : LPAREN ids_inplace RPAREN'''
    ids_inplace: inplace_typed_value_t = p[2]
    p[0] = ids_inplace


def p_function(p):
    '''cmd_function : FUNCTION fakeid inplace_param LCURLY lineend codeblock RCURLY'''
    fakeid: fakeid_t = p[2]
    func_param: inplace_typed_value_t = p[3]
    lcurly: Token = Token(p.slice[4])
    # TODO: add lineend
    codeblock: codeblock_t = p[6]
    rcurly: Token = Token(p.slice[7])
    p[0] = FunctionNode(p, fakeid, func_param, codeblock, lcurly, rcurly)


def p_ids_param(p):
    '''ids_param : LPAREN ids RPAREN'''
    ids: ids_t = p[2]
    p[0] = ids


def p_exec(p):
    '''cmd_exec : EXEC fakeid ids_param'''
    fakeid: fakeid_t = p[2]
    func_param: ids_param_t = p[3]
    p[0] = ExecNode(p, fakeid, func_param, False)


def p_exec_ptr(p):
    '''cmd_exec : EXEC_PTR fakeid ids_param'''
    fakeid: fakeid_t = p[2]
    func_param: ids_param_t = p[3]
    p[0] = ExecNode(p, fakeid, func_param, True)


def p_struct(p):
    '''cmd_struct : STRUCT fakeid ids_param'''
    fakeid: fakeid_t = p[2]
    params: ids_param_t = p[3]
    p[0] = StructNode(p, fakeid, params)


def p_new(p):
    '''cmd_new : NEW fakeid OP_ASSIGN fakeid ids_param'''
    varname: fakeid_t = p[2]
    structname: fakeid_t = p[4]
    params: ids_param_t = p[5]
    p[0] = NewObjectNode(p, varname, structname, params)

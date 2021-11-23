import ply.yacc as yacc
from .lexer import tokens, reserved
from .nodes import *
from .preprocessor import CodePosResolver
from .utils import find_column

start = 'codeblock'


def p_program1(p):
    '''codeblock : line'''
    p[0] = CodeBlockNode(p[1])


def p_program2(p):
    '''codeblock : codeblock line'''
    p[0] = CodeBlockNode(p[2], p[1])


def p_func_param(p):
    '''func_param : LPAREN ids RPAREN'''
    p[0] = p[2]


def p_ids1(p):
    '''ids : value'''
    p[0] = [p[1]]


def p_ids2(p):
    '''ids : ids COMMA value'''
    p[1].append(p[3])
    p[0] = p[1]


def p_function(p):
    '''cmd_function : FUNCTION fakeid func_param LCURLY lineend codeblock RCURLY lineend'''
    p[0] = FunctionNode(p[2], p[3], p[6])


def p_function_error(p):
    '''cmd_function : error lineend'''
    p[0] = ErrorNode()
    p.parser.errok()


def p_write(p):
    '''cmd_write : WRITE value fakeid var_int'''
    p[0] = OperationNode(p[1], p[2:])


def p_read(p):
    '''cmd_read : READ fakeid fakeid var_int'''
    p[0] = OperationNode(p[1], p[2:])


def p_draw(p):
    '''cmd_draw : DRAW draw_instruction'''
    p[0] = OperationNode(p[1], p[2])


def p_draw_instruction(p):
    '''draw_instruction : CLEAR var_int var_int var_int null null null
                        | COLOR var_int var_int var_int null null null
                        | STROKE var_int null null null null null
                        | LINE var_int var_int var_int var_int null null
                        | RECT var_int var_int var_int var_int null null
                        | LINERECT var_int var_int var_int var_int null null
                        | POLY var_int var_int var_int var_number var_number null
                        | LINEPOLY var_int var_int var_int var_number var_number null
                        | TRIANGLE var_int var_int var_int var_int var_int var_int
                        | IMAGE var_int var_int fakeid var_number var_number null
    '''
    p[0] = p[1:]


def p_drawflush(p):
    '''cmd_drawflush : DRAWFLUSH fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_print(p):
    '''cmd_print : PRINT value'''
    p[0] = OperationNode(p[1], p[2:])


def p_printflush(p):
    '''cmd_printflush : PRINTFLUSH fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_getlink(p):
    '''cmd_getlink : GETLINK fakeid var_int'''
    p[0] = OperationNode(p[1], p[2:])


def p_control(p):
    '''cmd_control : CONTROL control_instruction'''
    p[0] = OperationNode(p[1], p[2])


def p_control_instruction(p):
    '''control_instruction : ENABLED fakeid var_bool null null null
                           | SHOOT fakeid var_number var_number var_bool null
                           | SHOOTP fakeid fakeid var_bool null null
                           | CONFIGURE fakeid fakeid null null null
                           | COLOR var_number var_number var_number null null
    '''
    p[0] = p[1:]


def p_radar(p):
    '''cmd_radar : RADAR radar_target radar_target radar_target radar_sort fakeid var_int fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_radar_target(p):
    '''radar_target : ANY
                    | ENEMY
                    | ALLY
                    | PLAYER
                    | ATTACKER
                    | FLYING
                    | BOSS
                    | GROUND
    '''
    p[0] = p[1]


def p_radar_sort(p):
    '''radar_sort : DISTANCE
                  | HEALTH
                  | SHIELD
                  | ARMOR
                  | MAXHEALTH
    '''
    p[0] = p[1]


def p_sensor(p):
    '''cmd_sensor : SENSOR fakeid fakeid fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_set(p):
    '''cmd_set : SET fakeid value'''
    p[0] = OperationNode(p[1], p[2:])


def p_op(p):
    '''cmd_op : OP op_instruction fakeid value value'''
    p[0] = OperationNode(p[1], p[2:])


def p_op_add(p):
    '''cmd_op_add : fakeid OP_ASSIGN value OP_ADD value'''
    params = "add {var} {lv} {rv}".format(var=p[1], lv=p[3], rv=p[5])
    p[0] = OperationNode("op", params.split(" "))


def p_op_sub(p):
    '''cmd_op_sub : fakeid OP_ASSIGN value OP_SUB value'''
    params = "sub {var} {lv} {rv}".format(var=p[1], lv=p[3], rv=p[5])
    p[0] = OperationNode("op", params.split(" "))


def p_op_mul(p):
    '''cmd_op_mul : fakeid OP_ASSIGN value OP_MUL value'''
    params = "mul {var} {lv} {rv}".format(var=p[1], lv=p[3], rv=p[5])
    p[0] = OperationNode("op", params.split(" "))


def p_op_div(p):
    '''cmd_op_div : fakeid OP_ASSIGN value OP_DIV value'''
    params = "div {var} {lv} {rv}".format(var=p[1], lv=p[3], rv=p[5])
    p[0] = OperationNode("op", params.split(" "))


def p_op_eq(p):
    '''cmd_op_eq : fakeid OP_ASSIGN value OP_EQ value'''
    params = "equal {var} {lv} {rv}".format(var=p[1], lv=p[3], rv=p[5])
    p[0] = OperationNode("op", params.split(" "))


def p_op_set(p):
    '''cmd_op_set : fakeid OP_ASSIGN value'''
    p[0] = OperationNode("set", [p[1], p[3]])


def p_op_instruction(p):
    '''op_instruction : ADD
                      | SUB
                      | MUL
                      | DIV
                      | IDIV
                      | MOD
                      | POW
                      | EQUAL
                      | NOTEQUAL
                      | LAND
                      | LESSTHAN
                      | LESSTHANEQ
                      | GREATERTHAN
                      | GREATERTHANEQ
                      | STRICTEQUAL
                      | SHL
                      | SHR
                      | OR
                      | AND
                      | XOR
                      | NOT
                      | MAX
                      | MIN
                      | ANGLE
                      | LEN
                      | NOISE
                      | ABS
                      | LOG
                      | LOG10
                      | SIN
                      | COS
                      | TAN
                      | FLOOR
                      | CEIL
                      | SQRT
                      | RAND
    '''
    p[0] = p[1]


def p_end(p):
    '''cmd_end : END'''
    p[0] = OperationNode(p[1])


def p_jump(p):
    '''cmd_jump : JUMP INT jump_comparison value value'''
    p[0] = OperationNode(p[1], p[2:])


def p_jump_comparison(p):
    '''jump_comparison : EQUAL
                       | NOTEQUAL
                       | LESSTHAN
                       | LESSTHANEQ
                       | GREATERTHAN
                       | GREATERTHANEQ
                       | STRICTEQUAL
                       | ALWAYS
    '''
    p[0] = p[1]


def p_ubind(p):
    '''cmd_ubind : UBIND fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_ucontrol(p):
    '''cmd_ucontrol : UCONTROL ucontrol_instruction'''
    p[0] = OperationNode(p[1], p[2])


def p_ucontrol_instruction(p):
    '''ucontrol_instruction : IDLE null null null null null
                            | STOP null null null null null
                            | MOVE var_number var_number null null null
                            | APPROACH var_number var_number var_number null null
                            | BOOST var_bool null null null null
                            | PATHFIND null null null null null
                            | TARGET var_number var_number var_bool null null
                            | TARGETP fakeid var_bool null null null
                            | ITEMDROP fakeid var_int null null null
                            | ITEMTAKE fakeid fakeid var_int null null
                            | PAYDROP null null null null null
                            | PAYTAKE var_bool null null null null
                            | MINE var_number var_number null null null
                            | FLAG var_number null null null null
                            | BUILD var_number var_number fakeid var_int fakeid
                            | GETBLOCK var_number var_number fakeid fakeid null
                            | WITHIN var_number var_number var_number var_bool null
    '''
    p[0] = p[1:]


def p_uradar(p):
    '''cmd_uradar : URADAR radar_target radar_target radar_target radar_sort null var_bool fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_ulocate(p):
    '''cmd_ulocate : ULOCATE ulocate_find ulocate_group var_bool fakeid var_number var_number var_bool fakeid'''
    p[0] = OperationNode(p[1], p[2:])


def p_ulocate_find(p):
    '''ulocate_find : ORE
                    | BUILDING
                    | SPAWN
                    | DAMAGED
    '''
    p[0] = p[1]


def p_ulocate_group(p):
    '''ulocate_group : CORE
                     | STORAGE
                     | GENERATOR
                     | TURRET
                     | FACTORY
                     | REPAIR
                     | RALLY
                     | BATTERY
                     | RESUPPLY
                     | REACTOR
    '''
    p[0] = p[1]


def p_noop(p):
    '''cmd_noop : NOOP'''
    p[0] = OperationNode(p[1])


def p_exec(p):
    '''cmd_exec : EXEC fakeid func_param'''
    p[0] = ExecNode(p[2], p[3])


def p_lineend1(p):
    '''lineend : NEWLINE'''
    p[0] = CommentNode("")


def p_lineend2(p):
    '''lineend : COMMENT NEWLINE'''
    p[0] = CommentNode(p[1])


def p_line(p):
    '''line : operation lineend'''
    p[0] = OneLineNode(p[1], p[2])


def p_line1(p):
    '''line : lineend'''
    p[0] = p[1]


def p_line_error(p):
    '''line : error NEWLINE'''
    p[0] = ErrorNode()
    p.parser.errok()


def p_operation(p):
    '''operation : cmd_write
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
                 | cmd_function
                 | cmd_exec
                 | cmd_op_add
                 | cmd_op_sub
                 | cmd_op_mul
                 | cmd_op_div
                 | cmd_op_eq
                 | cmd_op_set
    '''
    p[0] = p[1]


def p_var_int(p):
    '''var_int : fakeid
               | INT
    '''
    p[0] = p[1]


def p_var_number(p):
    '''var_number : fakeid
                  | number
    '''
    p[0] = p[1]


def p_var_bool(p):
    '''var_bool : value'''
    p[0] = p[1]


def p_null(p):
    '''null : value'''
    p[0] = p[1]


def p_value(p):
    '''value : fakeid
             | STRING
             | number
             | BOOL
    '''
    p[0] = p[1]


def p_number(p):
    '''number : INT
              | DOUBLE
    '''
    p[0] = p[1]


def p_fakeid(p):
    '''fakeid : ID
              | keyword
    '''
    p[0] = p[1]


def p_keyword(p):
    p[0] = p[1]


p_keyword.__doc__ = "keyword : " + "\n      | ".join([res for res in reserved.values()])


LINT = False
CODE_POS = []


def setup(lint: bool, code_pos: CodePosResolver):
    global LINT, CODE_POS
    LINT = lint
    CODE_POS = code_pos


def p_error(p):
    if p is None:
        raise Exception("Unexpected end of file.")
    msg = f"Syntax error! Error on token: {repr(p.value)} ({p.type})"
    make_error(p, "error", msg)


def make_error(p, type, message):
    global CODE_POS, LINT
    column = find_column(p.lexer.lexdata, p)
    form = "{path}:{line}:{column}: {type}: {msg}"
    lineno, filename = CODE_POS[p.lineno - 1]
    formatted = form.format(path=filename, line=lineno + 1, column=column, type=type, msg=message)
    if LINT:
        print(formatted)
    else:
        raise Exception(formatted)


parser = yacc.yacc()


def do_parsing(text):
    result = parser.parse(text)
    return result

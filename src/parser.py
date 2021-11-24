import ply.yacc as yacc
from .lexer import tokens, reserved
from .nodes import *
from .preprocessor import CodePosResolver
from .utils import find_column

start = 'codeblock'

keyword_t = Token
string_t = Token
bool_t = Token
double_t = Token
int_t = Token
id_t = Token
fakeid_t = Union[id_t, keyword_t]
number_t = Union[int_t, double_t]
value_t = Union[fakeid_t, string_t, number_t, bool_t]
null_t = value_t
var_bool_t = value_t
var_number_t = Union[fakeid_t, number_t]
var_int_t = Union[fakeid_t, int_t]
ids_t = List[value_t]
func_param_t = ids_t
cmd_function_t = FunctionNode
cmd_default_t = OperationNode
draw_instruction_t = List[Union[Token, var_int_t, fakeid_t, var_number_t, null_t]]
control_instruction_t = List[Union[Token, fakeid_t, var_bool_t, null_t, var_number_t]]
radar_target_t = Token
radar_sort_t = Token
op_instruction_t = Token
jump_comparison_t = Token
ucontrol_instruction_t = List[Union[Token, null_t, var_number_t, var_bool_t, fakeid_t, var_int_t]]
ulocate_find_t = Token
ulocate_group_t = Token
cmd_exec_t = ExecNode
operation_t = Union[cmd_exec_t, cmd_function_t, cmd_default_t]
lineend_t = CommentNode
line_t = Union[lineend_t, OneLineNode, ErrorNode]
codeblock_t = CodeBlockNode





def p_program1(p):
    '''codeblock : line'''
    line: line_t = p[1]
    p[0] = CodeBlockNode(p, line)


def p_program2(p):
    '''codeblock : codeblock line'''
    codeblock: codeblock_t = p[1]
    line: line_t = p[2]
    p[0] = CodeBlockNode(p, line, codeblock)


def p_func_param(p):
    '''func_param : LPAREN ids RPAREN'''
    ids: ids_t = p[2]
    p[0] = ids


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


def p_function(p):
    '''cmd_function : FUNCTION fakeid func_param LCURLY lineend codeblock RCURLY'''
    fakeid: fakeid_t = p[2]
    func_param: func_param_t = p[3]
    lcurly: Token = Token(p.slice[4])
    # TODO: add lineend
    codeblock: codeblock_t = p[6]
    rcurly: Token = Token(p.slice[7])
    p[0] = FunctionNode(p, fakeid, func_param, codeblock, lcurly, rcurly)


def p_write(p):
    '''cmd_write : WRITE value fakeid var_int'''
    write: Token = Token(p.slice[1])
    value: value_t = p[2]
    fakeid: fakeid_t = p[3]
    var_int: var_int_t = p[4]
    p[0] = OperationNode(p, write, [value, fakeid, var_int])


def p_read(p):
    '''cmd_read : READ fakeid fakeid var_int'''
    read: Token = Token(p.slice[1])
    fakeid1: fakeid_t = p[2]
    fakeid2: fakeid_t = p[3]
    var_int: var_int_t = p[4]
    p[0] = OperationNode(p, read, [fakeid1, fakeid2, var_int])


def p_draw(p):
    '''cmd_draw : DRAW draw_instruction'''
    draw: Token = Token(p.slice[1])
    draw_instruction: draw_instruction_t = p[2]
    p[0] = OperationNode(p, draw, draw_instruction)


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
    subcommand_s: Token = Token(p.slice[1])
    subcommand: Token = Token(subcommand_s)
    parameters: List[Union[var_int_t, fakeid_t, var_number_t, null_t]] = p[2:]
    p[0] = [subcommand] + parameters


def p_drawflush(p):
    '''cmd_drawflush : DRAWFLUSH fakeid'''
    drawflush: Token = Token(p.slice[1])
    fakeid: fakeid_t = p[2]
    p[0] = OperationNode(p, drawflush, [fakeid])


def p_print(p):
    '''cmd_print : PRINT value'''
    print: Token = Token(p.slice[1])
    value: value_t = p[2]
    p[0] = OperationNode(p, print, [value])


def p_printflush(p):
    '''cmd_printflush : PRINTFLUSH fakeid'''
    printflush: Token = Token(p.slice[1])
    fakeid: fakeid_t = p[2]
    p[0] = OperationNode(p, printflush, [fakeid])


def p_getlink(p):
    '''cmd_getlink : GETLINK fakeid var_int'''
    getlink: Token = Token(p.slice[1])
    fakeid: fakeid_t = p[2]
    var_int: var_int_t = p[3]
    p[0] = OperationNode(p, getlink, [fakeid, var_int])


def p_control(p):
    '''cmd_control : CONTROL control_instruction'''
    control: Token = Token(p.slice[1])
    control_instruction: control_instruction_t = p[2]
    p[0] = OperationNode(p, control, control_instruction)


def p_control_instruction(p):
    '''control_instruction : ENABLED fakeid var_bool null null null
                           | SHOOT fakeid var_number var_number var_bool null
                           | SHOOTP fakeid fakeid var_bool null null
                           | CONFIGURE fakeid fakeid null null null
                           | COLOR var_number var_number var_number null null
    '''
    subcommand_s: Token = Token(p.slice[1])
    subcommand: Token = Token(subcommand_s)
    parameters: List[Union[fakeid_t, var_bool_t, null_t, var_number_t]] = p[2:]
    p[0] = [subcommand] + parameters


def p_radar(p):
    '''cmd_radar : RADAR radar_target radar_target radar_target radar_sort fakeid var_int fakeid'''
    radar: Token = Token(p.slice[1])
    parameters: List[Union[radar_target_t, radar_sort_t, fakeid_t, var_int_t]] = p[2:]
    p[0] = OperationNode(p, radar, parameters)


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
    subcommand_s: Token = Token(p.slice[1])
    p[0] = Token(subcommand_s)


def p_radar_sort(p):
    '''radar_sort : DISTANCE
                  | HEALTH
                  | SHIELD
                  | ARMOR
                  | MAXHEALTH
    '''
    subcommand_s: Token = Token(p.slice[1])
    p[0] = Token(subcommand_s)


def p_sensor(p):
    '''cmd_sensor : SENSOR fakeid fakeid fakeid'''
    sensor: Token = Token(p.slice[1])
    parameters: List[fakeid_t] = p[2:]
    p[0] = OperationNode(p, sensor, parameters)


def p_set(p):
    '''cmd_set : SET fakeid value'''
    set: Token = Token(p.slice[1])
    fakeid: fakeid_t = p[2]
    value: value_t = p[3]
    p[0] = OperationNode(p, set, [fakeid, value])


def p_op(p):
    '''cmd_op : OP op_instruction fakeid value value'''
    op: Token = Token(p.slice[1])
    op_instruction: op_instruction_t = p[2]
    fakeid: fakeid_t = p[3]
    value1: value_t = p[4]
    value2: value_t = p[5]
    p[0] = OperationNode(p, op, [op_instruction, fakeid, value1, value2])


def p_op_add(p):
    '''cmd_op_add : fakeid OP_ASSIGN value OP_ADD value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_add_reduced(p):
    '''cmd_op_add : fakeid OP_ADD OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_add_reduced_much(p):
    '''cmd_op_add : fakeid OP_ADD OP_ADD'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    rv = "1"
    params = "add {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=rv)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_sub(p):
    '''cmd_op_sub : fakeid OP_ASSIGN value OP_SUB value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_sub_reduced(p):
    '''cmd_op_sub : fakeid OP_SUB OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_sub_reduced_much(p):
    '''cmd_op_sub : fakeid OP_SUB OP_SUB'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    rv = "1"
    params = "sub {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=rv)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_mul(p):
    '''cmd_op_mul : fakeid OP_ASSIGN value OP_MUL value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "mul {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_mul_reduced(p):
    '''cmd_op_mul : fakeid OP_MUL OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "mul {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_div(p):
    '''cmd_op_div : fakeid OP_ASSIGN value OP_DIV value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "div {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_div_reduced(p):
    '''cmd_op_div : fakeid OP_DIV OP_ASSIGN value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[4]
    params = "div {var} {lv} {rv}".format(var=fakeid, lv=fakeid, rv=value1)
    p[0] = OperationNode(p, op, params.split(" "))



def p_op_eq(p):
    '''cmd_op_eq : fakeid OP_ASSIGN value OP_EQ value'''
    op: str = "op"
    fakeid: fakeid_t = p[1]
    value1: value_t = p[3]
    value2: value_t = p[5]
    params = "equal {var} {lv} {rv}".format(var=fakeid, lv=value1, rv=value2)
    p[0] = OperationNode(p, op, params.split(" "))


def p_op_set(p):
    '''cmd_op_set : fakeid OP_ASSIGN value'''
    op: str = "set"
    fakeid: fakeid_t = p[1]
    value: value_t = p[3]
    p[0] = OperationNode(p, op, [fakeid, value])


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
    subcommand_s: Token = Token(p.slice[1])
    p[0] = Token(subcommand_s)


def p_end(p):
    '''cmd_end : END'''
    op: Token = Token(p.slice[1])
    p[0] = OperationNode(p, op)


def p_jump(p):
    '''cmd_jump : JUMP int jump_comparison value value'''
    op: Token = Token(p.slice[1])
    int_o: int_t = p[2]
    jump_comparison: jump_comparison_t = p[3]
    value1: value_t = p[4]
    value2: value_t = p[5]
    p[0] = OperationNode(p, op, [int_o, jump_comparison, value1, value2])


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
    subcommand: Token = Token(p.slice[1])
    p[0] = Token(subcommand)


def p_ubind(p):
    '''cmd_ubind : UBIND fakeid'''
    ubind: Token = Token(p.slice[1])
    fakeid: fakeid_t = p[2]
    p[0] = OperationNode(p, ubind, [fakeid])


def p_ucontrol(p):
    '''cmd_ucontrol : UCONTROL ucontrol_instruction'''
    ucontrol: Token = Token(p.slice[1])
    ucontrol_instruction: ucontrol_instruction_t = p[2]
    p[0] = OperationNode(p, ucontrol, ucontrol_instruction)


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
    subcommand_s: Token = Token(p.slice[1])
    subcommand: Token = Token(subcommand_s)
    parameters: List[Union[fakeid_t, var_bool_t, null_t, var_int_t, var_number_t]] = p[2:]
    p[0] = [subcommand] + parameters


def p_uradar(p):
    '''cmd_uradar : URADAR radar_target radar_target radar_target radar_sort null var_bool fakeid'''
    uradar: Token = Token(p.slice[1])
    radar_target1: radar_target_t = p[2]
    radar_target2: radar_target_t = p[3]
    radar_target3: radar_target_t = p[4]
    radar_sort: radar_sort_t = p[5]
    null: null_t = p[6]
    var_bool: var_bool_t = p[7]
    fakeid: fakeid_t = p[8]
    p[0] = OperationNode(p, uradar, [radar_target1, radar_target2, radar_target3, radar_sort, null, var_bool, fakeid])


def p_ulocate(p):
    '''cmd_ulocate : ULOCATE ulocate_find ulocate_group var_bool fakeid var_number var_number var_bool fakeid'''
    ulocate: Token = Token(p.slice[1])
    ulocate_find: ulocate_find_t = p[2]
    ulocate_group: ulocate_group_t = p[3]
    var_bool1: var_bool_t = p[4]
    fakeid: fakeid_t = p[5]
    var_number1: var_number_t = p[6]
    var_number2: var_number_t = p[7]
    var_bool2: var_bool_t = p[8]
    fakeid: fakeid_t = p[9]
    p[0] = OperationNode(p, ulocate, [ulocate_find, ulocate_group, var_bool1, fakeid, var_number1, var_number2, var_bool2])


def p_ulocate_find(p):
    '''ulocate_find : ORE
                    | BUILDING
                    | SPAWN
                    | DAMAGED
    '''
    p[0] = Token(p.slice[1])


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
    p[0] = Token(p.slice[1])


def p_noop(p):
    '''cmd_noop : NOOP'''
    noop: Token = Token(p.slice[1])
    p[0] = OperationNode(p, noop)


def p_exec(p):
    '''cmd_exec : EXEC fakeid func_param'''
    fakeid: fakeid_t = p[2]
    func_param: func_param_t = p[3]
    p[0] = ExecNode(p, fakeid, func_param)


def p_lineend1(p):
    '''lineend : NEWLINE'''
    newline: Token = Token(p.slice[1])
    p[0] = NewLineNode(p, newline)


def p_lineend2(p):
    '''lineend : COMMENT NEWLINE'''
    comment: Token = Token(p.slice[1])
    p[0] = CommentNode(p, comment)


def p_line(p):
    '''line : operation lineend'''
    operation: operation_t = p[1]
    lineend: lineend_t = p[2]
    p[0] = OneLineNode(p, operation, lineend)


def p_line1(p):
    '''line : lineend'''
    lineend: lineend_t = p[1]
    p[0] = lineend


def p_line_error(p):
    '''line : error NEWLINE'''
    p[0] = ErrorNode(p)
    p.parser.errok()


def p_operation(p):
    '''operation : cmd_write
                 | cmd_function
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
                 | cmd_op_add
                 | cmd_op_sub
                 | cmd_op_mul
                 | cmd_op_div
                 | cmd_op_eq
                 | cmd_op_set
    '''
    operation: operation_t = p[1]
    p[0] = operation


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

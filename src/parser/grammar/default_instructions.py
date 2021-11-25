from src.parser.types import *
from src.nodes import *


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
    p[0] = subcommand_s


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


def p_op(p):
    '''cmd_op : OP op_instruction fakeid value value'''
    op: Token = Token(p.slice[1])
    op_instruction: op_instruction_t = p[2]
    fakeid: fakeid_t = p[3]
    value1: value_t = p[4]
    value2: value_t = p[5]
    p[0] = OperationNode(p, op, [op_instruction, fakeid, value1, value2])



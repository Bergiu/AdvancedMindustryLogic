from src.nodes import *
from typing import Union, List

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
var_double_t = Union[fakeid_t, double_t]
var_string_t = Union[fakeid_t, string_t]
ids_t = List[value_t]
ids_inplace_t = List[value_t]
func_param_t = ids_inplace_t
exec_param_t = ids_t
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
instruction_t = Union[cmd_exec_t, cmd_function_t, cmd_default_t]
lineend_t = CommentNode
line_t = Union[lineend_t, OneLineNode, ErrorNode]
codeblock_t = CodeBlockNode
statement_t = Union[Token, StatementNode]



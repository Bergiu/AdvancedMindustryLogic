from .preprocessor import CodePosResolver
import ply.lex as lex

from .utils import find_column

instruction_names = [
    'write',
    'read',
    'draw',
    'drawflush',
    'print',
    'printflush',
    'getlink',
    'control',
    'radar',
    'sensor',
    'set',
    'op',
    'end',
    'jump',
    'ubind',
    'ucontrol',
    'uradar',
    'ulocate',
    'noop',
]

sub_instructions_draw = [
    'clear',
    'color',
    'stroke',
    'line',
    'rect',
    'lineRect',
    'poly',
    'linePoly',
    'triangle',
    'image',
]

sub_instructions_control = [
    'enabled',
    'shoot',
    'shootp',
    'configure',
    'color',
]

sub_instructions_radar_target = [
    'any',
    'enemy',
    'ally',
    'player',
    'attacker',
    'flying',
    'boss',
    'ground',
]

sub_instructions_radar_sort = [
    'distance',
    'health',
    'shield',
    'armor',
    'maxHealth',
]

sub_instructions_op = [
    'add',
    'sub',
    'mul',
    'div',
    'idiv',
    'mod',
    'pow',
    'equal',
    'notEqual',
    'land',
    'lessThan',
    'lessThanEq',
    'greaterThan',
    'greaterThanEq',
    'strictEqual',
    'shl',
    'shr',
    'or',
    'and',
    'xor',
    'not',
    'max',
    'min',
    'angle',
    'len',
    'noise',
    'abs',
    'log',
    'log10',
    'sin',
    'cos',
    'tan',
    'floor',
    'ceil',
    'sqrt',
    'rand',
]

# (only the ones that are missing)
sub_instructions_jump = [
    'always',
]

sub_instructions_ucontrol = [
    'idle',
    'stop',
    'move',
    'approach',
    'boost',
    'pathfind',
    'target',
    'targetp',
    'itemDrop',
    'itemTake',
    'payDrop',
    'payTake',
    'mine',
    'flag',
    'build',
    'getBlock',
    'within',
]

sub_instructions_ulocate = [
    'ore',
    'building',
    'spawn',
    'damaged',
    'core',
    'storage',
    'generator',
    'turret',
    'factory',
    'repair',
    'rally',
    'battery',
    'resupply',
    'reactor',
]


reserved_keys = [
    # 'if': 'IF',
    # 'then': 'THEN',
    # 'else': 'ELSE',
    # 'while': 'WHILE',
    # 'define',
    'function',
    'exec',
]

reserved_keys.extend(instruction_names)
reserved_keys.extend(sub_instructions_draw)
reserved_keys.extend(sub_instructions_control)
reserved_keys.extend(sub_instructions_radar_target)
reserved_keys.extend(sub_instructions_radar_sort)
reserved_keys.extend(sub_instructions_op)
reserved_keys.extend(sub_instructions_jump)
reserved_keys.extend(sub_instructions_ucontrol)
reserved_keys.extend(sub_instructions_ulocate)

reserved = {res: res.upper() for res in reserved_keys}

# List of token names.   This is always required
tokens = [
    'INT',
    'DOUBLE',
    'STRING',
    'BOOL',
    'NEWLINE',
    'ID',
    'COMMENT',
    'LCURLY',
    'RCURLY',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'OP_ASSIGN',
    'OP_ADD',
    'OP_SUB',
    'OP_MUL',
    'OP_DIV',
    'OP_EQ',
] + list(reserved.values())


def t_ID(t):
    r'@?[a-zA-Z_][a-zA-Z_0-9/.]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# Regular expression rules for simple tokens
t_STRING = r'".*?"'
t_BOOL = r'"(true|false)"'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_OP_EQ = r'=='
t_OP_ASSIGN = r'='
t_OP_ADD = r'\+'
t_OP_SUB = r'-'
t_OP_MUL = r'\*'
t_OP_DIV = r'/'


def t_COMMENT(t):
    r'\#.*'
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def t_DOUBLE(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_NEWLINE(t):
    r'\n+'
    a = len(t.value)
    t.lexer.lineno += a
    return t


LINT = False
CODE_POS = []


def setup(lint: bool, code_pos: CodePosResolver):
    global LINT, CODE_POS
    LINT = lint
    CODE_POS = code_pos


# Error handling rule
def t_error(t):
    global CODE_POS, LINT
    column = find_column(t.lexer.lexdata, t)
    msg = f"Illegal character: {repr(t.value[0])}"
    form = "{path}:{line}:{column}: ({symbol}) {msg}"
    lineno, filename = CODE_POS[t.lineno]
    formatted = form.format(path=filename, line=lineno, column=column, symbol=t.type, msg=msg)
    if LINT:
        print(formatted)
        t.lexer.skip(1)
    else:
        raise Exception(formatted)


# Build the lexer
lexer = lex.lex()


def do_lexing(data):
    lexer.input(data)
    while True:
        i = lexer.token()
        if i is None:
            break
        print(i)

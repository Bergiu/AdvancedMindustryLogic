from __future__ import annotations

from typing import Any, Optional, List, Generator, Union

from src.preprocessor import CodePosResolver

LINT = False
CODE_POS = []


def setup(lint: bool, code_pos: CodePosResolver):
    global LINT, CODE_POS
    LINT = lint
    CODE_POS = code_pos


class NodeException(BaseException):
    def __init__(self, symbol, message):
        self.symbol = symbol
        self.message = message
        self.filename = "todo"
        self.lineno = "todo"
        self.column = "todo"


class TokenException(BaseException):
    def __init__(self, symbol, message, token, parser):
        global CODE_POS
        self.symbol = symbol
        self.message = message
        line_start = parser.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        self.column = (token.lexpos - line_start) + 1
        lineno, self.filename = CODE_POS[token.lineno - 1]
        self.lineno = lineno + 1


class Node:
    def __init__(self, p):
        self.p = p

    def __iter__(self):
        yield self

    def call_exception(self, exception: Union[NodeException, TokenException]):
        global LINT
        if LINT:
            form = "{path}:{line}:{column}: ({symbol}) {msg}"
            out = form.format(
                path=exception.filename,
                line=exception.lineno,
                column=exception.column,
                symbol=exception.symbol,
                msg=exception.message)
            print(out)
        else:
            raise exception

    def find_function(self, tree: Node, function_name: str) -> Generator[FunctionNode]:
        for x in tree:
            if isinstance(x, FunctionNode) and x.function_name == function_name:
                yield x

    def find_parent(self, tree: Node) -> Node:
        last = None
        for x in tree:
            if x == self:
                return last
            last = x

    def find_self(self, tree: Node) -> Node:
        for x in tree:
            if x == self:
                return x

    def find_type(self, tree: Node, type) -> Generator[Node]:
        for x in tree:
            if isinstance(x, type):
                yield x

    def loc(self):
        raise NotImplementedError()

    def to_code(self, tree: Node):
        raise NotImplementedError()


class OneLineNode(Node):
    """
    One Line Nodes are nodes that have one line (that can result in many lines) and optionally a comment.
    So the loc of this is the amount of lines from the left node.
    """
    def __iter__(self):
        yield self
        yield from self.left
        yield from self.right

    def __init__(self, p, left: Node, right: Node):
        super().__init__(p)
        self.left = left
        self.right = right

    def loc(self):
        return self.left.loc()

    def to_code(self, tree: Node) -> str:
        return f"{self.left.to_code(tree)} {self.right.to_code(tree)}"


class CodeBlockNode(Node):
    def __iter__(self):
        yield self
        if self.prev_node is not None:
            yield from self.prev_node
        yield from self.line

    def __init__(self, p, line: Node, prev_node: CodeBlockNode = None):
        super().__init__(p)
        self.line = line
        self.prev_node = prev_node

    def loc(self):
        loc = 0
        if self.prev_node is not None:
            if isinstance(self.prev_node, Node):
                loc += self.prev_node.loc()
            else:
                loc += 1
        if isinstance(self.line, Node):
            a = self.line.loc()
            loc += a
        else:
            loc += 1
        return loc

    def to_code(self, tree: Node):
        out = ""
        if self.prev_node is not None:
            out += f"{self.prev_node.to_code(tree)}\n"
        out += f"{self.line.to_code(tree)}"
        return out


class OperationNode(Node):
    def __init__(self, p, command: Union[Token, str], parameters: Optional[List[Any]] = None):
        super().__init__(p)
        self.command = command
        self.parameters = parameters

    def loc(self):
        return 1

    def to_code(self, tree: Node):
        out = f"{self.command}"
        if self.parameters is not None:
            out += "".join([f" {param}" for param in self.parameters])
        return out


class OperationStatementNode(Node):
    def __init__(self, p, command: Union[Token, str], statement: Union[Token, str, StatementNode]):
        super().__init__(p)
        self.command = command
        self.statement = statement

    def loc(self):
        out = 1
        if isinstance(self.statement, StatementNode):
            out +=  self.statement.loc()
        return out

    def to_code(self, tree: Node):
        out = ""
        if isinstance(self.statement, StatementNode):
            out += f"{self.statement.to_code(tree)}\n"
            out += f"{self.command} {self.statement.varname}"
        else:
            out += f"{self.command} {self.statement}"
        return out


class FunctionNode(Node):
    def __iter__(self):
        yield self
        yield from self.code_block

    def __init__(self, p, function_name: Token, params: List[Any], code_block: CodeBlockNode, lcurly: Token, rcurly: Token):
        super().__init__(p)
        self.function_name = function_name.token.value
        self.params = params
        self.code_block = code_block
        self.lcurly = lcurly
        self.rcurly = rcurly

    def loc(self):
        return self.code_block.loc() + 4

    def to_code(self, tree: Node):
        out = ""
        lines = self.code_block.loc() + 2
        out += f"op add {self.function_name} @counter 1\n"
        out += f"op add @counter @counter {lines}\n"
        out += f"set _{self.function_name}_retptr retptr\n"
        out += f"{self.code_block.to_code(tree)}\n"
        out += f"set @counter _{self.function_name}_retptr"
        return out


class NewLineNode(Node):
    def __init__(self, p, token):
        super().__init__(p)
        self.token = token

    def to_code(self, tree: Node):
        return ""

    def loc(self):
        return 0


class CommentNode(Node):
    def __init__(self, p, comment: Union[Token, str]):
        super().__init__(p)
        self.comment = comment

    def to_code(self, tree: Node):
        return str(self.comment)

    def loc(self):
        return 0


class ExecNode(Node):
    def __init__(self, p, fnptr: Token, params: List[Any]):
        super().__init__(p)
        #function_name = p.slice[2].value.lexpos
        self.fnptr = fnptr
        self.params = params

    def loc(self):
        return 2 + len(self.params)

    def get_related_function(self, tree: Node) -> Optional[FunctionNode]:
        function_name = self.fnptr.token.value
        functions = list(self.find_function(tree, function_name))
        if len(functions) >= 2:
            self.call_exception(TokenException("error", f"Multiple definitions of function  {function_name}.", self.fnptr.token, self.p))
            self.call_exception(TokenException("error", f"Multiple definitions of function  {function_name}.", self.fnptr.token, self.p))
            return
        if len(functions) < 1:
            self.call_exception(TokenException("error", f"Missing definition of function {function_name}.", self.fnptr.token, self.p))
            return
        function = functions[0]
        x = len(function.params) - len(self.params)
        if x > 0:
            param_names = " and ".join([f"'{param}'" for param in function.params[len(function.params) - x:]])
            if len(function.params) > 1:
                self.call_exception(TokenException("error", f"TypeError: {function_name} missing {x} positional arguments: {param_names}", self.fnptr.token, self.p))
                return
            else:
                self.call_exception(TokenException("error", f"TypeError: {function_name} missing {x} positional argument: {param_names}", self.fnptr.token, self.p))
                return
        if x < 0:
            param = self.params[len(self.params) + x].token
            self.call_exception(TokenException("error", f"TypeError: {function_name} takes {len(function.params)} but {len(self.params)} were given", param, self.p))
            return
        return functions[0]

    def to_code(self, tree: Node):
        out = ""
        function = self.get_related_function(tree)
        if function is None:
            return "ERROR"
        for i, param_value in enumerate(self.params):
            param_name = function.params[i]
            out += f"set {param_name} {param_value}\n"
        out += "op add retptr @counter 1\n"
        out += f"set @counter {self.fnptr.token.value}"
        return out


class ErrorNode(Node):
    def __init__(self, p):
        super().__init__(p)

    def loc(self):
        return 0

    def to_code(self, tree: Node):
        return "ERROR"


class Token:
    def __init__(self, token):
        self.token = token

    def __str__(self):
        if isinstance(self.token, Token):
            return str(self.token)
        return str(self.token.value)


class WhileNode(Node):
    def __init__(self, p, while_o: Token, condition: Token, codeblock: CodeBlockNode):
        super().__init__(p)
        self.while_o = while_o
        self.condition = condition
        self.codeblock = codeblock

    def loc(self):
        out = self.codeblock.loc() + 5
        if isinstance(self.condition, StatementNode):
            out += self.condition.loc()
        return out

    def to_code(self, tree: Node):
        ident = self.__hash__()
        start_ptr = f"while_start_{ident}"
        skip = f"skip_{ident}"
        out = f"set {start_ptr} @counter\n"
        if isinstance(self.condition, StatementNode):
            out += f"{self.condition.to_code(tree)}\n"
            out += f"op notEqual {skip} {self.condition.varname} 1\n"
        else:
            out += f"op notEqual {skip} {self.condition} 1\n"
        out += f"op mul {skip} {skip} {self.codeblock.loc() + 1}\n"
        out += f"op add @counter @counter {skip}\n"
        out += f"{self.codeblock.to_code(tree)}\n"
        out += f"set @counter {start_ptr}\n"
        return out


class IfNode(Node):
    def __init__(self, p, if_o: Token, condition: Union[Token, StatementNode], codeblock: CodeBlockNode):
        super().__init__(p)
        self.if_o = if_o
        self.condition = condition
        self.codeblock = codeblock

    def loc(self):
        out = self.codeblock.loc() + 3
        if isinstance(self.condition, StatementNode):
            out += self.condition.loc()
        return out

    def to_code(self, tree: Node):
        out = ""
        if isinstance(self.condition, StatementNode):
            out += f"{self.condition.to_code(tree)}\n"
            out += f"op notEqual if_skip {self.condition.varname} 1\n"
        else:
            out += f"op notEqual if_skip {self.condition} 1\n"
        out += f"op mul if_skip if_skip {self.codeblock.loc()}\n"
        out += f"op add @counter @counter if_skip\n"
        out += self.codeblock.to_code(tree)
        return out


class IfElseNode(Node):
    def __init__(self, p, if_o: Token, condition: Union[Token, StatementNode], codeblock1: CodeBlockNode, codeblock2: CodeBlockNode):
        super().__init__(p)
        self.if_o = if_o
        self.condition = condition
        self.codeblock1 = codeblock1
        self.codeblock2 = codeblock2

    def loc(self):
        out = self.codeblock1.loc() + self.codeblock2.loc() + 4
        if isinstance(self.condition, StatementNode):
            out += self.condition.loc()
        return out

    def to_code(self, tree: Node):
        out = ""
        if isinstance(self.condition, StatementNode):
            out += f"{self.condition.to_code(tree)}\n"
            out += f"op notEqual if_skip {self.condition.varname} 1\n"
        else:
            out += f"op notEqual if_skip {self.condition} 1\n"
        out += f"op mul if_skip if_skip {self.codeblock1.loc() + 1}\n"
        out += f"op add @counter @counter if_skip\n"
        out += f"{self.codeblock1.to_code(tree)}\n"
        out += f"op add @counter @counter {self.codeblock2.loc()}\n"
        out += self.codeblock2.to_code(tree)
        return out


class StatementNode(Node):
    def __init__(self, p, operation: str, value1: Union[str, Token, StatementNode], value2: Union[str, Token, StatementNode]):
        super().__init__(p)
        self.operation = operation
        self.value1 = value1
        self.value2 = value2
        self.varname = f"var_{self.__hash__()}"

    def loc(self):
        out = 1
        if isinstance(self.value1, StatementNode):
            out += self.value1.loc()
        if isinstance(self.value2, StatementNode):
            out += self.value2.loc()
        return out

    def to_code(self, tree: Node):
        out = ""
        if isinstance(self.value1, StatementNode):
            out += f"{self.value1.to_code(tree)}\n"
            val1 = self.value1.varname
        else:
            val1 = self.value1
        if isinstance(self.value2, StatementNode):
            out += f"{self.value2.to_code(tree)}\n"
            val2 = self.value2.varname
        else:
            val2 = self.value2
        out += f"op {self.operation} {self.varname} {val1} {val2}"
        return out

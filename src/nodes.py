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
            out += f"{self.prev_node.to_code(tree)}"
        out += f"{self.line.to_code(tree)}\n"
        return out


class OperationNode(Node):
    def __init__(self, p, command: str, parameters: Optional[List[Any]] = None):
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


class FunctionNode(Node):
    def __iter__(self):
        yield self
        yield from self.code_block

    def __init__(self, p, function_name: str, params: List[Any], code_block: CodeBlockNode):
        super().__init__(p)
        self.function_name = function_name
        self.params = params
        self.code_block = code_block

    def loc(self):
        return self.code_block.loc() + 4

    def to_code(self, tree: Node):
        out = ""
        lines = self.code_block.loc() + 2
        out += f"op add {self.function_name} @counter 1\n"
        out += f"op add @counter @counter {lines}\n"
        out += f"set _{self.function_name}_retptr retptr\n"
        out += str(self.code_block.to_code(tree))
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
    def __init__(self, p, comment: str):
        super().__init__(p)
        self.comment = comment

    def to_code(self, tree: Node):
        return str(self.comment)

    def loc(self):
        return 0


class ExecNode(Node):
    def __init__(self, p, fnptr: str, params: List[Any]):
        super().__init__(p)
        #function_name = p.slice[2].value.lexpos
        self.fnptr = fnptr
        self.params = params

    def loc(self):
        return 2 + len(self.params)

    def get_related_function(self, tree: Node) -> Optional[FunctionNode]:
        functions = list(self.find_function(tree, self.fnptr))
        if len(functions) > 2:
            self.call_exception(NodeException("error", f"Multiple definitions of function  {self.fnptr}."))
            return
        if len(functions) < 1:
            self.call_exception(NodeException("error", f"Missing definition of function {self.fnptr}."))
            return
        function = functions[0]
        x = len(function.params) - len(self.params)
        if x > 0:
            param_names = " and ".join([f"'{param}'" for param in function.params[len(function.params) - x:]])
            if len(function.params) > 1:
                self.call_exception(NodeException("error", f"TypeError: {self.fnptr} missing {x} positional arguments: {param_names}"))
                return
            else:
                self.call_exception(NodeException("error", f"TypeError: {self.fnptr} missing {x} positional argument: {param_names}"))
                return
        if x < 0:
            self.call_exception(NodeException("error", f"TypeError: {self.fnptr} takes {len(function.params)} but {len(self.params)} were given"))
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
        out += f"set @counter {self.fnptr}"
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
        return str(self.token.value)

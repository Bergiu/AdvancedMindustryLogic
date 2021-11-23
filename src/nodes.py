from __future__ import annotations

from typing import Any, Optional, List, Generator


LINT = True


class NodeException:
    def __init__(self, symbol, message):
        self.symbol = symbol
        self.message = message


class Node:
    def __iter__(self):
        yield self

    def call_exception(self, exception: NodeException):
        global LINT
        if LINT:
            form = "{path}:{line}:{column}: ({symbol}) {msg}"
            out = form.format(path="todo", line="todo", column="todo", symbol=exception.symbol, msg=exception.message)
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
    def __iter__(self):
        yield self
        yield from self.left
        yield from self.right

    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.left = left
        self.right = right

    def loc(self):
        return 1

    def to_code(self, tree: Node) -> str:
        return f"{self.left.to_code(tree)} {self.right.to_code(tree)}"


class CodeBlockNode(Node):
    def __iter__(self):
        yield self
        if self.prev_node is not None:
            yield from self.prev_node
        yield from self.line

    def __init__(self, line: Node, prev_node: CodeBlockNode = None):
        super().__init__()
        self.line = line
        self.prev_node = prev_node

    def loc(self):
        if self.prev_node is not None and isinstance(self.prev_node, Node):
            if isinstance(self.line, Node):
                return self.prev_node.loc() + self.line.loc()
            return self.prev_node.loc() + 1
        return 1

    def to_code(self, tree: Node):
        out = ""
        if self.prev_node is not None:
            out += f"{self.prev_node.to_code(tree)}"
        out += f"{self.line.to_code(tree)}\n"
        return out


class OperationNode(Node):
    def __init__(self, command: str, parameters: Optional[List[Any]] = None):
        super().__init__()
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

    def __init__(self, function_name: str, params: List[Any], code_block: CodeBlockNode):
        super().__init__()
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
        out += f"set _{self.function_name}_retptr @counter\n"
        out += str(self.code_block.to_code(tree))
        out += "set @counter retptr"
        return out


class CommentNode(Node):
    def __init__(self, comment: str):
        super().__init__()
        self.comment = comment

    def to_code(self, tree: Node):
        return str(self.comment)

    def loc(self):
        return 0


class ExecNode(Node):
    def __init__(self, fnptr: str, params: List[Any]):
        super().__init__()
        self.fnptr = fnptr
        self.params = params

    def loc(self):
        return 2 + len(self.params)

    def get_related_function(self, tree: Node) -> FunctionNode:
        functions = list(self.find_function(tree, self.fnptr))
        if len(functions) > 2:
            self.call_exception(NodeException("error", f"Multiple definitions of function  {self.fnptr}."))
        if len(functions) < 1:
            self.call_exception(NodeException("error", f"Missing definition of function {self.fnptr}."))
        function = functions[0]
        x = len(function.params) - len(self.params)
        if x > 0:
            param_names = " and ".join([f"'{param}'" for param in function.params[len(function.params) - x:]])
            if len(function.params) > 1:
                self.call_exception(NodeException("error", f"TypeError: {self.fnptr} missing {x} positional arguments: {param_names}"))
            else:
                self.call_exception(NodeException("error", f"TypeError: {self.fnptr} missing {x} positional argument: {param_names}"))
        if x < 0:
            self.call_exception(NodeException("error", f"TypeError: {self.fnptr} takes {len(function.params)} but {len(self.params)} were given"))
        return functions[0]

    def to_code(self, tree: Node):
        out = ""
        function = self.get_related_function(tree)
        for i, param_value in enumerate(self.params):
            param_name = function.params[i]
            out += f"set {param_name} {param_value}\n"
        out += "op add retptr @counter 1\n"
        out += f"set @counter {self.fnptr}"
        return out


class ErrorNode(Node):
    def loc(self):
        return 0

    def to_code(self, tree: Node):
        out = "ERROR"
        return out
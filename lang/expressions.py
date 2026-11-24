"""Restricted expression evaluator; .roya files cannot execute arbitrary Python."""
import ast
import operator
from .errors import RoyaExpressionError

_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Mod: operator.mod}
_CMPOPS = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge, ast.In: lambda a, b: a in b, ast.NotIn: lambda a, b: a not in b}
_SAFE_FUNCTIONS = {"str": str, "int": int, "float": float, "len": len, "bool": bool}


class _Evaluator(ast.NodeVisitor):
    def __init__(self, scope):
        self.scope = scope

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        return node.value

    def visit_Name(self, node):
        if node.id in _SAFE_FUNCTIONS:
            return _SAFE_FUNCTIONS[node.id]
        if node.id in self.scope:
            return self.scope[node.id]
        raise RoyaExpressionError(f"Unknown name '{node.id}'.")

    def visit_Attribute(self, node):
        if node.attr.startswith("_"):
            raise RoyaExpressionError("Private attributes are not accessible in .roya expressions.")
        value = self.visit(node.value)
        if isinstance(value, dict):
            if node.attr not in value:
                raise RoyaExpressionError(f"Mapping has no key '{node.attr}'.")
            return value[node.attr]
        try:
            return getattr(value, node.attr)
        except AttributeError as exc:
            raise RoyaExpressionError(f"Object has no attribute '{node.attr}'.") from exc

    def visit_Subscript(self, node):
        return self.visit(node.value)[self.visit(node.slice)]

    def visit_List(self, node):
        return [self.visit(item) for item in node.elts]

    def visit_Tuple(self, node):
        return tuple(self.visit(item) for item in node.elts)

    def visit_Dict(self, node):
        return {self.visit(key): self.visit(value) for key, value in zip(node.keys, node.values)}

    def visit_BinOp(self, node):
        operation = _BINOPS.get(type(node.op))
        if operation is None:
            raise RoyaExpressionError("This arithmetic operator is not allowed.")
        return operation(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            return not self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -self.visit(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +self.visit(node.operand)
        raise RoyaExpressionError("This unary operator is not allowed.")

    def visit_BoolOp(self, node):
        if isinstance(node.op, ast.And):
            result = True
            for value in node.values:
                result = self.visit(value)
                if not result:
                    return result
            return result
        if isinstance(node.op, ast.Or):
            for value in node.values:
                result = self.visit(value)
                if result:
                    return result
            return result
        raise RoyaExpressionError("This boolean operator is not allowed.")

    def visit_Compare(self, node):
        left = self.visit(node.left)
        for operation_node, comparator in zip(node.ops, node.comparators):
            operation = _CMPOPS.get(type(operation_node))
            if operation is None:
                raise RoyaExpressionError("This comparison operator is not allowed.")
            right = self.visit(comparator)
            if not operation(left, right):
                return False
            left = right
        return True

    def visit_IfExp(self, node):
        return self.visit(node.body if self.visit(node.test) else node.orelse)

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in _SAFE_FUNCTIONS:
            raise RoyaExpressionError("Only str(), int(), float(), len() and bool() calls are allowed.")
        if node.keywords or len(node.args) != 1:
            raise RoyaExpressionError("Safe conversion functions accept exactly one positional argument.")
        return _SAFE_FUNCTIONS[node.func.id](self.visit(node.args[0]))

    def generic_visit(self, node):
        raise RoyaExpressionError(f"Unsupported expression syntax: {type(node).__name__}.")


def evaluate(expression, scope):
    value = str(expression).strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in ("none", "null"):
        return None
    try:
        tree = ast.parse(value, mode="eval")
        return _Evaluator(scope).visit(tree)
    except RoyaExpressionError:
        raise
    except Exception as exc:
        raise RoyaExpressionError(f"Could not evaluate expression '{value}': {exc}") from exc

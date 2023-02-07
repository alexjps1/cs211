"""
Expression Definitions
by Alex JPS
2023-02-05
CS 211
"""

# Global environment for variable storage
ENV: dict[str, "IntConst"] = dict()

def env_clear():
    """Clear all variables in calculator memory"""
    global ENV
    ENV = dict()

class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")

class IntConst(Expr):

    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"IntConst({str(self.value)})"

    def __eq__(self, other: "IntConst") -> bool:
        return isinstance(other, IntConst) and self.value == other.value

    def eval(self) -> "IntConst":
        return self

class BinOp(Expr):
    """Abstract base class for binary operations"""
    
    def __init__(self, left: Expr, right: Expr, symbol: str = "?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol
    
    def __str__(self) -> str:
        """Algebraic notation, fully parenthesized: (left + right)"""
        return f"({self.left} {self.symbol} {self.right})"

    def __repr__(self) -> str:
        """Returns string like call to constructor,
        e.g. Plus(IntConst(5), IntConst(4)"""
        return f"{self.__class__.__name__}({self.left.__repr__()}, {self.right.__repr__()})"
        
    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define __apply(int, int) -> int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))

class Plus(BinOp):
    """left + right"""
    
    def __init__(self, left: "Expr", right: "Expr"):
        super().__init__(left, right, symbol="+")

    def _apply(self, left: int, right: int) -> int:
        return left + right

class Times(BinOp):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="*")

    def _apply(self, left: int, right: int) -> int:
        return left * right

class Div(BinOp):
    """left / right"""
    
    def __init__(self, left: "Expr", right: "Expr"):
        super().__init__(left, right, symbol="/")

    def _apply(self, left: int, right: int) -> int:
        return left // right

class Minus(BinOp):
    """left - right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="-")

    def _apply(self, left: int, right: int) -> int:
        return left - right

class UnOp(Expr):

    def __init__(self, affected: Expr, symbol: str = "?Operation symbol undefined") -> None:
        self.affected = affected
        self.symbol = symbol

    def __str__(self) -> str:
        """Algebraic notation representation"""
        return f"({self.symbol} {self.affected})"

    def __repr__(self) -> str:
        """Returns string like call to constructor,
        e.g. Neg(IntConst(5))"""
        return f"{self.__class__.__name__}({self.affected.__repr__()})"
        
    def _apply(self, affected_val) -> int:
        """Each concrete UnOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete UnOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define __apply(int, int) -> int"""
        affected_val = self.affected.eval()
        return IntConst(self._apply(affected_val.value))

class Abs(UnOp):

    def __init__(self, affected: Expr) -> None:
        super().__init__(affected, symbol="@")

    def _apply(self, affected: int) -> int:
        return affected if affected > 1 else -1*affected

class Neg(UnOp):

    def __init__(self, affected: Expr) -> None:
        super().__init__(affected, symbol="~")

    def _apply(self, affected: int) -> int:
        return -1*affected

class UndefinedVariable(Exception):
    """Raised if expression tries to use a variable not in ENV"""
    pass

class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")

    def assign(self, value: IntConst):
        ENV[self.name] = value

class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""
    
    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables! 
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self) -> str:
        return f"({self.left} = {self.right})"

    def __repr__(self) -> str:
        return f"Assign({self.left.__repr__()}, {self.right.__repr__()})"

class IfOp(Expr):
    """Class for 'then else condition if' expressions"""
    
    def __init__(self, then_expr: Expr, else_expr: Expr, cond_expr: Expr):
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.cond_expr = cond_expr
    
    def __str__(self) -> str:
        """Algebraic notation, fully parenthesized"""
        return f"(if {self.cond_expr} then {self.then_expr} else {self.else_expr})"

    def __repr__(self) -> str:
        """Returns string like call to constructor"""
        return f"IfOp({self.then_expr.__repr__()}, {self.else_expr.__repr__()}, {self.cond_expr.__repr__()})"
        
    def eval(self) -> "IntConst":
        """Return IntConst object for then_expr if cond_expr is nonzero,
        otherwise return InstConst object for else_expr"""
        cond_val = self.cond_expr.eval()
        if cond_val.value != 0:
            then_val = self.then_expr.eval()
            return then_val
        else:
            else_val = self.else_expr.eval()
            return else_val

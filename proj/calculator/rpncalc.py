"""
Expression Definitions
edited by Alex JPS
2023-02-05
CS 211

This RPN calculator creates an expression tree from
the input.  It prints the expression in algebraic
notation and then prints the result of evaluating it.
"""

import lex
import expr
import io
from expr import ENV

def calc(text: str):
    """Evaluate results from rpn_parse(text) and print them"""
    try:
        stack = rpn_parse(text)
        if len(stack) == 0:
            print("(No expression)")
        else:
            # For a balanced expression there will be one Expr object
            # on the stack, but if there are more we'll just print
            # each of them
            for exp in stack:
                print(f"{exp} => {exp.eval()}")
    except Exception as e: 
        print(e)

def rpn_parse(text: str) -> list[expr.Expr]:
    """Parse RPN text to list of Expr (one list if balanced)
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input
    """
    BINOPS = { lex.TokenCat.PLUS: expr.Plus,
           lex.TokenCat.TIMES: expr.Times,
           lex.TokenCat.DIV: expr.Div,
           lex.TokenCat.MINUS:  expr.Minus
        }
    UNOPS = {lex.TokenCat.NEG: expr.Neg,
             lex.TokenCat.ABS: expr.Abs
             }
    try:
        tokens = lex.TokenStream(io.StringIO(text))
        stack = [ ]
        while tokens.has_more():
            tok = tokens.take()
            if tok.kind == lex.TokenCat.INT:
                # append IntConst() expressions
                stack.append(expr.IntConst(int(tok.value)))
            elif tok.kind in BINOPS:
                # pop 2 elements for BinOp() expressions
                binop_class = BINOPS[tok.kind]
                right = stack.pop()
                left = stack.pop()
                stack.append(binop_class(left, right))
            elif tok.kind in UNOPS:
                # pop 1 elements for UnOp() expressions
                unop_class = UNOPS[tok.kind]
                affected = stack.pop()
                stack.append(unop_class(affected))
            elif tok.kind == lex.TokenCat.ASSIGN:
                right = stack.pop()
                left = stack.pop()
                # Reverse left and right
                stack.append(expr.Assign(right, left))
            elif tok.kind == lex.TokenCat.VAR:
                stack.append(expr.Var(tok.value))
            elif tok.kind == lex.TokenCat.IF:
                cond_expr = stack.pop()
                else_expr = stack.pop()
                then_expr = stack.pop()
                stack.append(expr.IfOp(then_expr, else_expr, cond_expr))
    except lex.LexicalError as e:
        raise ValueError(f"Lexical error {e}")
        return
    except IndexError:
        # Stack underflow means the expression was imbalanced
        raise ValueError(f"Imbalanced RPN expression, missing operand at {tok.value}")
        return
    return stack

def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")



if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()

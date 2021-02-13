'''Python file for the compiler's Interpreter class

The interpreter class is meant to go through and interpret(evaluate) the AST
'''
# Python libs
import math

# Importing token types
from ..tokens import Token
from ..tokens.token_type import PLUS, MINUS, MUL, DIV, MODULUS, INT_DIV, POWER, LPARAM, RPARAM, COMMA, EOF
from ..tokens.token_type import E, PI, SIN, COS, TAN, FLOOR, CEIL, LN, LG, FACTORIAL, SQRT, BIN, HEX, LOG, POW, MOD, PERM, COMB

# Import AST and NodeVisitor
from ..nodes import AST
from ..nodes import Number_Node, String_Node, Unary_Node, BinaryOp_Node, Function_Node
from ..nodes import NodeVisitor

class Interpreter(NodeVisitor):
    def __init__(self, ast: AST):
        self.__ast = ast
    
    # Class helper methods
    def __error(self):
        # Placeholder error method
        # TODO: Make proper one
        raise Exception('Interpreter error')

    # Errors
    # Type error
    # Mixing type op
    
    # Node Type Visitor Implementation
    def visit_BinaryOp_Node(self, node: BinaryOp_Node):
        token_type = node.token.type
        left = self.visit(node.left)
        right = self.visit(node.right)
        # Check if binary op is done on same type of variable
        if type(left) != type(right):
            self.__error()
        
        # For both str or int
        if token_type in set([PLUS]):
            # Supports only number or str
            if not (isinstance(left, int) or isinstance(left, float) or isinstance(left, str)):
                # Type for bin op is not supported
                self.__error()
            if token_type == PLUS:
                return left + right
        
        # For int only
        if token_type in set([MINUS, MODULUS, MUL, DIV, POWER, INT_DIV]):
            # Supports only number
            if not (isinstance(left, int) or isinstance(left, float)):
                # Type for bin op is not supported
                self.__error()
            if token_type == MINUS:
                return left - right
            elif token_type == MODULUS:
                return left % right
            elif token_type == MUL:
                return left * right
            elif token_type == DIV:
                return left / right
            elif token_type == POWER:
                return left ** right
            elif token_type == INT_DIV:
                return left // right
        
        # There is an error?
        self.__error()
    
    def visit_UnaryOp_Node(self, node: Unary_Node):
        token_type = node.token.type
        child = self.visit(node.child)

        # Node only supports number
        if not (isinstance(child, int) or isinstance(child, float)):
            if token_type == PLUS:
                return child
            elif token_type == MINUS:
                return -child
    
    def visit_Function_Node(self, node: Function_Node):
        node_token = node.token
        function_name = node_token.value
        arguments = [self.visit(argument) for argument in node.arguments]
        if function_name in set([E, PI]):
            # Arity 0
            if not node.check_arity(0):
                self.__error()
            # Return based on function call
            if function_name == E:
                return math.e
            elif function_name == PI:
                return math.pi
        elif function_name in set([SIN, COS, TAN, FLOOR, CEIL, LN, LG, FACTORIAL, SQRT, BIN, HEX]):
            # Arity 1
            if not node.check_arity(1):
                self.__error()
            argument = arguments[0]
            # Return based on function call
            if function_name in set([SIN, COS, TAN, FLOOR, CEIL, LN, LG, FACTORIAL, SQRT]):
                # Only takes in number
                if not (isinstance(argument, int) or isinstance(argument, float)):
                    # Type error
                    self.__error()
                # Eval
                if function_name == SIN:
                    return math.sin(argument)
                elif function_name == COS:
                    return math.cos(argument)
                elif function_name == TAN:
                    return math.tan(argument)
                elif function_name == FLOOR:
                    return math.floor(argument)
                elif function_name == CEIL:
                    return math.ceil(argument)
                elif function_name == LN:
                    return math.log(argument)
                elif function_name == LG:
                    return math.log10(argument)
                elif function_name == FACTORIAL:
                    return math.factorial(argument)
                elif function_name == SQRT:
                    return math.sqrt(argument)
            if function_name in set([BIN, HEX]):
                # Only takes in strings
                if not (isinstance(argument, str)):
                    self.__error()
                # Eval
                if function_name == BIN:
                    pass
                elif function_name == HEX:
                    pass
        elif function_name in set([LOG, POW, MOD, PERM, COMB]):
            # Arity 2
            if not node.check_arity(2):
                self.__error()
            # Making sure all are numbers
            for argument in arguments:
                if not (isinstance(argument, int) or isinstance(argument, float)):
                    self.__error()
            
            if function_name == LOG:
                return math.log(arguments[0], arguments[1])
            elif function_name == POW:
                return math.pow(arguments[0], arguments[1])
            elif function_name == MOD:
                return arguments[0]%arguments[1]
            elif function_name == PERM:
                # TODO: Check n >= r
                # Also try catch for no float value stuff
                n = arguments[0]
                r = arguments[1]
                return ((math.factorial(n)) / (math.factorial(n - r)))
            elif function_name == COMB:
                # TODO: Check n >= r
                n = arguments[0]
                r = arguments[1]
                return ((math.factorial(n)) / (math.factorial(r) * math.factorial(n - r)))
    
    def visit_Number_Node(self, node: Number_Node):
        return node.value
    
    def visit_String_Node(self, node: String_Node):
        return node.value
    
    # Public methods
    def get_interpretation(self):
        return self.visit(self.__ast)



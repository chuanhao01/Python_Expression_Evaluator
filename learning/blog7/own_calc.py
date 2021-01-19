# Node implementation
class AST(object):
    pass

class BinOp(AST):
    def __init__(self, op, left, right):
        self.token = self.op = op
        self.left = left
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

# Global token type for now
INTEGER, EOF = 'INTERGER', 'EOF'
ADD, MINUS = 'ADD', 'MINUS'
MUL, DIV = 'MUL', 'DIV'
LPARAM, RPARAM = 'LPARAM', 'RPARAM'

class Token(object):
    def __init__(self, _type: str, value: str):
        '''
        _type : str
            Token type
        value : str
            Str value of the token
        '''
        self.type = _type
        self.value = value
    def __str__(self):
        s = f"Token({self.type}, {self.value})"
        return s

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def __error(self):
        raise Exception('Error parsing input')
    
    def __advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
            return
        else:
            self.current_char = None
    
    def __skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace(): self.__advance()
        return
    
    def __integer(self):
        integer_value = ''
        while self.current_char is not None and self.current_char.isdigit():
            integer_value += self.current_char
            self.__advance()
        return int(integer_value)
    
    def get_next_token(self):
        if self.current_char is not None:
            # Whitespace
            if self.current_char.isspace():
                self.__skip_whitespace()
                return self.get_next_token()
            # Integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.__integer())
            # Expression
            # ADD
            if self.current_char == '+':
                self.__advance()
                return Token(ADD, '+')
            # MINUS
            if self.current_char == '-':
                self.__advance()
                return Token(MINUS, '-')
            # MUL
            if self.current_char == '*':
                self.__advance()
                return Token(MUL, '*')
            # DIV
            if self.current_char == '/':
                self.__advance()
                return Token(DIV, '/')
            # LPARAM
            if self.current_char == '(':
                self.__advance()
                return Token(LPARAM, '(')
            # RPARAM
            if self.current_char == ')':
                self.__advance()
                return Token(RPARAM, ')')

        return Token(EOF, None)

# Parser
class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def __error(self):
        raise Exception('Syntax error')

    def __eat(self, token_type: str):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.__error()
    
    def expr(self):
        '''
        expr: term ((ADD | MINUS) term)*
        '''
        # Set left as term
        node = self.term()

        while self.current_token.type in set([ADD, MINUS]):
            token = self.current_token
            if token.type == ADD:
                self.__eat(ADD)
            elif token.type == MINUS:
                self.__eat(MINUS)
            # Set BinOp node back to left, for chaining
            node = BinOp(token, node, self.term())
        
        return node
    
    def term(self):
        '''
        term: factor ((MUL | DIV) factor)*
        '''
        node = self.factor()

        while self.current_token.type in set([MUL, DIV]):
            token = self.current_token
            if token.type == MUL:
                self.__eat(MUL)
            elif token.type == DIV:
                self.__eat(DIV)
            node = BinOp(token, node, self.factor())
        
        return node
    
    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.__eat(INTEGER)
            return Num(token)
        elif token.type == LPARAM:
            self.__eat(LPARAM)
            node = self.expr()
            self.__eat(RPARAM)
            return node
    
    def parse(self):
        # Helper method to parse the text from lexer
        return self.expr()

# Interpreter
class NodeVisitor(object):
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.__visit_error)
        return visitor(node)
    
    def __visit_error(self, node):
        raise Exception(f"Visit method visit_{type(node).__name__} is not implemented")

class PostFix(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"{left}{right}{node.op.value}"
    
    def visit_Num(self, node):
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
    
    def visit_BinOp(self, node):
        if node.op.type == ADD:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_Num(self, node):
        return node.token.value
    
    def interpret(self):
        # Helper method to interpret the parsed ast
        tree = self.parser.parse()
        print_post_order(tree)
        return self.visit(tree)

# Utils
def print_post_order(node, level=0):
    if not isinstance(node, Num):
        if node.left is not None:
            print_post_order(node.left, level+1)
        if node.right is not None:
            print_post_order(node.right, level+1)
    print(f"{'-'*level} {node.token.value}")

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        # interpreter = PostFix(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()

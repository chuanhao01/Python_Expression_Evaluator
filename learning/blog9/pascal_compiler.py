'''
Grammar we are using for the compiler

program: compund_statement DOT
compund_statement: BEGIN statement_list END
statement_list: statement
    | statement SEMI statement_list
statement: compund_statement
    | assignment_statement
    | empty
assignment_statement: variable ASSIGN expr
variable: ID
empty: 
expr: term ((PLUS | MINUS) term)*
term: factor ((MUL | DIV) factor)*
factor: PLUS factor
    | MINUS factor
    | NUMBER
    | LPARAM expr RPARAM
    | variable
'''

# --- Tokens ---
BEGIN, END = {'BEGIN', 'END'}
DOT = 'DOT'
ID = 'ID'
PLUS, MINUS = {'PLUS', 'MINUS'}
MUL, DIV = {'MUL', 'DIV'}
LPARAM, RPARAM = {'LPARAM', 'RPARAM'}
NUMBER = 'NUMBER'
EOF = 'EOF'

class Token(object):
    def __init__(self, _type:str, value: str):
        self.type = _type
        self.value = value
    
    def __str__(self):
        s = f"Token({self.type}, {self.value})"
        return s

# --- Lexer -- 
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def __error(self):
        raise Exception('Error tokenizing input')
    
    def __advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def __peek(self):
        pos = self.pos + 1
        if pos < len(self.text):
            return self.text[pos]
        else:
            return None
    
    def __check_syntax_errors(self):
        if self.current_char is not None:
            # Making sure there are no syntax errors
            if self.current_char == '.' and self.__peek() == '.':
                self.__error()
        return True

    def __skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.__advance()
        return
    
    def __number(self):
        number_value = ''
        seen_dot = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            # Making sure there is only one dot
            if self.current_char == '.':
                if not seen_dot:
                    seen_dot = True
                else:
                    # Already seen dot, there is another dot. Error
                    self.__error()
            number_value += self.current_char
            self.__advance()
        number_value = float(number_value)
        return number_value
    
    def get_next_token(self):
        if self.current_char is not None and self.__check_syntax_errors():
            # Whitespace
            if self.current_char.isspace():
                self.__skip_whitespace()
                return self.get_next_token()
            # Number
            if self.current_char.isdigit() or (self.current_char == '.' and self.__peek().isdigit()):
                return Token(NUMBER, self.__number())
            # BinaryOps
            if self.current_char == '(':
                self.__advance()
                return Token(LPARAM, '(')
            if self.current_char == ')':
                self.__advance()
                return Token(RPARAM, ')')
            if self.current_char == '+':
                self.__advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.__advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.__advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.__advance()
                return Token(DIV, '/')
        return Token(EOF, None)

#  --- Parser ---

# AST
class AST(object):
    pass

class BinaryOp(AST):
    def __init__(self, token: Token, left: AST, right: AST):
        self.token = token
        self.left = left
        self.right = right

class UnaryOp(AST):
    def __init__(self, token: Token, child):
        self.token = token
        self.child = child

class Num(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = self.token.value

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()
    
    def __error(self):
        raise SyntaxError('Syntax error')

    def __eat(self, token_type):
        '''
        Check if the current_token is the same as the given token type
        If true, 'consume' the current_token
        Else throw an error
        '''
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.__error()
    
    def expr(self):
        '''
        expr: term ((PLUS | MINUS) term)*
        '''
        node = self.term()
        while self.current_token.type in set([PLUS, MINUS]):
            token = self.current_token
            if token.type == PLUS:
                self.__eat(PLUS)
            elif token.type == MINUS:
                self.__eat(MINUS)
            node = BinaryOp(token, node, self.term())
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
            node = BinaryOp(token, node, self.factor())
        return node

    def factor(self):
        '''
        factor: PLUS factor
            | MINUS factor
            | NUMBER
            | LPARAM expr RPARAM
            | variable
        '''
        token = self.current_token
        if token.type == PLUS:
            self.__eat(PLUS)
            return UnaryOp(token, self.factor())
        if token.type == MINUS:
            self.__eat(MINUS)
            return UnaryOp(token, self.factor())
        if token.type == LPARAM:
            self.__eat(LPARAM)
            node = self.expr()
            self.__eat(RPARAM)
            return node
        if token.type == NUMBER:
            self.__eat(NUMBER)
            return Num(token)
    
    def parse(self):
        return self.expr()
        
# --- Interpreter ---
class NodeVisitor(object):
    def __init__(self, parser):
        '''
        Generic init method for the class
        '''
        self.parser = parser

    def visit(self, node: AST):
        '''
        Generic visit method constructor
        When called on a node, will call the node's visit method
        node's visit method -> 'visit_{node_class_name}'

        Example:
        BinaryOp -> visit_BinaryOp(self, node)
        '''
        node_name = type(node).__name__
        method_name = f"visit_{node_name}"
        visit_method = getattr(self, method_name, self.__visit_method_error)
        return visit_method(node)
    
    def __visit_method_error(self, node: AST):
        node_name = type(node).__name__
        error_msg = f"Visit method for {node_name} not implemented"
        error_msg += f"Please implement the method visit_{node_name}"
        raise Exception(error_msg)

class Interpreter(NodeVisitor):
    def visit_BinaryOp(self, node: AST):
        node_token_type = node.token.type
        if node_token_type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node_token_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node_token_type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node_token_type == DIV:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_UnaryOp(self, node: AST):
        node_token_type = node.token.type
        if node_token_type == PLUS:
            return +self.visit(node.child)
        if node_token_type == MINUS:
            return -self.visit(node.child)
    
    def visit_Num(self, node: AST):
        return node.value
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


# --- Main Program Code below ---
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
        # print(interpreter.parser.parse())
        # interpreter = PostFix(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()

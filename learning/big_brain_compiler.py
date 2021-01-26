'''
--- Lexical Grammar ---
NUMBER: DIGIT* ('.' DIGIT+)?
IDENTIFIER: ALPHA+
DIGIT: '0' ... '9'
ALPHA: 'a' ... 'z' | 'A' ... 'Z' | '_'

--- Syntax Grammar ---
expression: term (('+' | '-') term)*
term: factor (('*' | '/' | '//') factor)*
factor: unary (('**') unary)*
unary: ('+' | '-') unary
	| call
call: primary ('(' arguments ')')?
primary: NUMBER
	| IDENTIFIER
	| '(' expression ')'
arguments: expression ((',') expression)*
'''
# Libs needed

###############################################################################
#                                                                             #
#  Tokens Types                                                               #
#                                                                             #
###############################################################################

# Token Class itself
class Token(object):
    def __init__(self, _type: str, value, pos: int):
        self.type = _type
        self.value = value
        self.pos = pos
    
    def __str__(self):
        s = f"Token({self.type}, {self.value})"
        return s

# Reserved token types
# PLUS, MINUS, MUL, DIV = ['+', '-', '*', '/']
# POWER, INT_DIV = ['**', '//']
# LPARAM, RPARAM = ['(', ')']

PLUS, MINUS, MUL, DIV = ['PLUS', 'MINUS', 'MUL', 'DIV']
POWER, INT_DIV = ['POWER', 'INT_DIV']
LPARAM, RPARAM = ['LPARAM', 'RPARAM']
COMMA = 'COMMA'
E, PI = ['E', 'PI']
SIN, COS = ['SIN', 'COS']
EOF = 'EOF'

# Normal token types
NUMBER = 'NUMBER'
IDENTIFIER = 'IDENTIFIER'

# Reserved keywords
RESERVED_KEYWORDS = {
    'E': Token(IDENTIFIER, E, None),
    'PI': Token(IDENTIFIER, PI, None),
    'sin': Token(IDENTIFIER, SIN, None),
    'cos': Token(IDENTIFIER, COS, None)
}


###############################################################################
#                                                                             #
#  Lexer                                                                      #
#                                                                             #
###############################################################################
class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.cur_pos = 0
        self.cur_char = self.text[self.cur_pos]
    
    # Class Helper methods
    def __is_end(self):
        return not (self.cur_pos < len(self.text))
    
    def __syntax_error(self):
        pass
    
    def __error(self):
        # Placeholder error method
        # TODO: Make proper one
        raise Exception('Lexer error')
    
    # Lexer methods
    def __advance(self):
        self.cur_pos += 1
        if not self.__is_end():
            self.cur_char = self.text[self.cur_pos]
        else:
            self.cur_char = None
    
    def __peek(self):
        pos = self.cur_pos + 1
        # Not at end
        if pos < len(self.text):
            return self.text[pos]
        else:
            return None

    # Lexer utility functions
    def __is_whitespace(self, c: str):
        if c is None:
            return False
        return c.isspace()
    
    def __is_digit(self, c: str):
        if c is None:
            return False
        return c.isdigit()
    
    def __is_alpha(self, c: str):
        if c is None:
            return False
        return c.isalpha() or c == '_'
        
    def __get_next_token(self):
        if not self.__is_end():
            # Making sure whitespace is skipped
            if self.__is_whitespace(self.cur_char):
                self.__skip_whitespace()
                return self.__get_next_token()
            # Checking single token types
            if self.cur_char == '+':
                token = Token(PLUS, '+', self.cur_pos)
                self.__advance()
                return token
            elif self.cur_char == '-':
                token = Token(MINUS, '-', self.cur_pos)
                self.__advance()
                return token
            elif self.cur_char == '(':
                token = Token(LPARAM, '(', self.cur_pos)
                self.__advance()
                return token
            elif self.cur_char == ')':
                token = Token(RPARAM, ')', self.cur_pos)
                self.__advance()
                return token
            elif self.cur_char == ',':
                token = Token(COMMA, ',', self.cur_pos)
                self.__advance()
                return token
            
            # Checking double token types
            if self.cur_char == '*':
                # If it is power
                if self.__peek() == '*':
                    token = Token(POWER, '**', self.cur_pos)
                    self.__advance()
                    self.__advance()
                    return token
                # else it is mul
                token = Token(MUL, '*', self.cur_pos)
                self.__advance()
                return token
            elif self.cur_char == '/':
                # If it is power
                if self.__peek() == '/':
                    token = Token(INT_DIV, '//', self.cur_pos)
                    self.__advance()
                    self.__advance()
                    return token
                # else it is mul
                token = Token(DIV, '/', self.cur_pos)
                self.__advance()
                return token
            
            # Check multi strings
            if self.__is_digit(self.cur_char) or self.cur_char == '.':
                # Check NUMBER
                return self.__number()
            elif self.__is_alpha(self.cur_char):
                # Check identifier
                return self.__identifier()
            
            # Unexpected error, char not recognised
            self.__error()
        
        return Token(EOF, None, self.cur_pos)

    def __skip_whitespace(self):
        while self.__is_whitespace(self.cur_char):
            self.__advance()
        return
    
    def __number(self):
        pos = self.cur_pos
        number_value = ''
        # 0 or more DIGITs
        while self.__is_digit(self.cur_char):
            number_value += self.cur_char
            self.__advance()
        # If there is a .
        if self.cur_char == '.':
            number_value == self.cur_char
            self.__advance()
            # Need to check 1 or more DIGITs
            if not self.__is_digit(self.cur_char):
                # Error if there is no DIGIT after
                self.__error()
            while self.__is_digit(self.cur_char):
                number_value += self.cur_char
                self.__advance()
        number_value = float(number_value)
        return Token(NUMBER, number_value, pos)

    def __identifier(self):
        pos = self.cur_pos
        identifier_value = ''
        while self.__is_alpha(self.cur_char):
            identifier_value += self.cur_char
            self.__advance()
        token = RESERVED_KEYWORDS.get(identifier_value, None)
        if token is None:
            self.__error()
        token.pos = pos
        return token

    # Main public class method
    def get_tokens(self):
        '''
        Public method to get all the tokens from the lexer
        Triggers to get all the tokens then return them
        '''
        token = self.__get_next_token()
        while token.type != EOF:
            self.tokens.append(token)
            token = self.__get_next_token()
        self.tokens.append(token)
        return self.tokens

###############################################################################
#                                                                             #
#  Parser                                                                     #
#                                                                             #
###############################################################################

# AST
class AST(object):
    pass

class Function_Node(AST):
    def __init__(self, token, arguments):
        self.token = token
        self.arguments = arguments
        self.arity = len(arguments)

class BinaryOp_Node(AST):
    def __init__(self, token, left: AST, right: AST):
        self.token = token
        self.left = left
        self.right = right

class UnaryOp_Node(AST):
    def __init__(self, token, child: AST):
        self.token = token
        self.child = child

class Number_Node(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_pos = 0
        self.tokens = self.lexer.get_tokens()
        self.cur_token = self.tokens[self.cur_pos]

    def __error(self):
        raise Exception('Parser error')

    def __is_end(self):
        return not (self.cur_pos < len(self.tokens))
    
    def __advance(self):
        if not self.__is_end():
            self.cur_pos += 1
    
    def __peek(self):
        pos = self.cur_pos + 1
        if pos < len(self.tokens):
            return self.tokens[pos]
        else:
            return None

    def __consume(self, token_type: str):
        if self.cur_token.type == token_type:
            self.__advance()
            self.cur_token = self.tokens[self.cur_pos]
        else:
            self.__error()
    
    def __expression(self):
        node = self.__term()
        while self.cur_token.type in set([PLUS, MINUS]):
            token = self.cur_token
            if self.cur_token.type == PLUS:
                self.__consume(PLUS)
            elif self.cur_token.type == MINUS:
                self.__consume(MINUS)
            node = BinaryOp_Node(token, node, self.__term())
        
        return node
    
    def __term(self):
        node = self.__factor()
        while self.cur_token.type in set([MUL, DIV, INT_DIV]):
            token = self.cur_token
            if self.cur_token.type == MUL:
                self.__consume(MUL)
            elif self.cur_token.type == DIV:
                self.__consume(DIV)
            elif self.cur_token.type == INT_DIV:
                self.__consume(INT_DIV)
            node = BinaryOp_Node(token, node, self.__factor())
        return node
    
    def __factor(self):
        node = self.__unary()
        while self.cur_token.type in set([POWER]):
            token = self.cur_token
            if self.cur_token.type == POWER:
                self.__consume(POWER)
            node = BinaryOp_Node(token, node, self.__unary())
        return node
    
    def __unary(self):
        if self.cur_token.type in set([PLUS, MINUS]):
            if self.cur_token.type == PLUS:
                self.__consume(PLUS)
            elif self.cur_token.type == MINUS:
                self.__consume(MINUS)
            return self.__unary()
        else:
            return self.__call()

    def __call(self):
        if self.cur_token.type == IDENTIFIER:
            token = self.cur_token
            self.__consume(IDENTIFIER)
            self.__consume(LPARAM)
            arguments = self.__arguments()
            self.__consume(RPARAM)
            return Function_Node(token, arguments)
        else:
            return self.__primary()
        
    def __arguments(self):
        node = self.__expression()
        if node is None:
            return []
        nodes = [node]
        while self.cur_token.type == COMMA:
            if self.cur_token.type == COMMA:
                self.__consume(COMMA)
            nodes.append(self.__expression)
        return nodes
        
    def __primary(self):
        if self.cur_token.type == NUMBER:
            token = self.cur_token
            self.__consume(NUMBER)
            return Number_Node(token)
        elif self.cur_token.type == LPARAM:
            self.__consume(LPARAM)
            node = self.__expression()
            self.__consume(RPARAM)
            return node
    
    def parse(self):
        return self.__expression()

if __name__ == '__main__':
    t = input('Test input:\n')
    lexer = Lexer(t)
    # tokens = lexer.get_tokens()
    # print([str(token) for token in tokens])
    parser = Parser(lexer)
    print(parser.parse())


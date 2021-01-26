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
E, PI = ['E', 'PI']
SIN, COS = ['SIN', 'COS']
EOF = 'EOF'

# Reserved keywords
RESERVED_KEYWORDS = {
    'E': Token(E, 'E', None),
    'PI': Token(PI, 'PI', None),
    'sin': Token(SIN, 'sin', None),
    'cos': Token(COS, 'cos', None)
}

# Normal token types
NUMBER = 'NUMBER'
IDENTIFIER = 'IDENTIFIER'

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
        return c.isspace()
    
    def __is_digit(self, c: str):
        return c.isdigit()
    
    def __is_alpha(self, c: str):
        return c.isalpha() or c == '_'
        
    def __get_next_token(self):
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
            token = Token(PLUS, '-', self.cur_pos)
            self.__advance()
            return token
        elif self.cur_char == '(':
            token = Token(PLUS, '(', self.cur_pos)
            self.__advance()
            return token
        elif self.cur_char == ')':
            token = Token(PLUS, ')', self.cur_pos)
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
        token.pos = pos
        if token is None:
            self.__error()
        return token

    # Main public class method
    def get_tokens(self):
        '''
        Public method to get all the tokens from the lexer
        Triggers to get all the tokens then return them
        '''
        while not self.__is_end():
            self.tokens.append(self.__get_next_token())
        self.tokens.append(Token(EOF, None, self.cur_pos))
        return self.tokens


if __name__ == '__main__':
    t = input('Test input:\n')
    lexer = Lexer(t)
    tokens = lexer.get_tokens()
    print(tokens)

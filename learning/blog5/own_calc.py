# Global token type for now
INTEGER, EOF = 'INTERGER', 'EOF'
ADD, MINUS = 'ADD', 'MINUS'
MUL, DIV = 'MUL', 'DIV'

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
        while self.current_char is not None and self.current_char.isspace():
            self.__advance()
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

        return Token(EOF, None)
    
class Interpreter(object):
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token() # Get the first token
    
    def __error(self):
        raise Exception('Syntax error')
    
    def __eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.__error()
    
    def expr(self):
        result = self.term()
        while self.current_token.type in set([ADD, MINUS]):
            token = self.current_token
            if token.type == ADD:
                self.__eat(ADD)
                result = result + self.term()
            elif token.type == MINUS:
                self.__eat(MINUS)
                result = result - self.term()
        return result
    
    def term(self):
        result = self.factor()
        while self.current_token.type in set([MUL, DIV]):
            token = self.current_token
            if token.type == MUL:
                self.__eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.__eat(DIV)
                result = result * self.factor()
        return result
    
    def factor(self):
        '''
        factor : INTEGER
        '''
        token = self.current_token
        self.__eat(INTEGER)
        return token.value


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
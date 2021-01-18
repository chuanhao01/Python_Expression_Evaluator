# Global token type for now
INTEGER, EXPR, EOF = 'INTERGER', 'EXPR', 'EOF'

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
    
class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
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
    
    def __get_next_token(self):
        if self.current_char is not None:
            # Whitespace
            if self.current_char.isspace():
                self.__skip_whitespace()
                return self.__get_next_token()
            # Integer
            if self.current_char.isdigit():
                return Token(INTEGER, self.__integer())
            # Expression
            if self.current_char in set(['+', '-', '*', '/']):
                expr_value = self.current_char
                self.__advance()
                return Token(EXPR, expr_value)

        return Token(EOF, None)


    def __eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.__get_next_token()
        else:
            self.__error()
    
    def __term(self):
        token = self.current_token
        self.__eat(INTEGER) # Making sure its an Integer
        return token.value # Return term value
    
    def expr(self):
        '''
        Making it do consec
        '''
        self.current_token = self.__get_next_token()
        result = self.__term()

        while self.current_token.type == EXPR:
            expr = self.current_token
            self.__eat(EXPR)
            if expr.value == '+':
                result = result + self.__term()
            elif expr.value == '-':
                result = result - self.__term()
            elif expr.value == '*':
                result = result * self.__term()
            elif expr.value == '/':
                result = result / self.__term()
        return result

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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
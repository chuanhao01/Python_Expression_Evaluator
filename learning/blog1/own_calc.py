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
    
    def __error(self):
        raise Exception('Error parsing input')
    
    def __get_next_token(self):
        text = self.text
        pos = self.pos

        if pos > len(text)-1:
            return Token(EOF, '')
        
        current_char = text[pos]
        if current_char.isdigit():
            current_token_value = ''
            while current_char.isdigit():
                current_token_value += current_char
                pos += 1
                if pos > len(text) - 1:
                    break
                current_char = text[pos]
            self.pos = pos
            return Token(INTEGER, int(current_token_value))
        
        if current_char in set(['+', '-', '*', '/']):
            self.pos = pos + 1
            return Token(EXPR, current_char)
        
        self.__error()

    def __eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.__get_next_token()
        else:
            self.__error()
    
    def expr(self):
        '''
        For INT EXPR INT
        '''
        self.current_token = self.__get_next_token()

        left = self.current_token
        self.__eat(INTEGER)

        expr = self.current_token
        self.__eat(EXPR)

        right = self.current_token
        self.__eat(INTEGER)

        result = None
        if expr.value == '+':
            result = left.value + right.value
        elif expr.value == '-':
            result = left.value - right.value
        elif expr.value == '*':
            result = left.value * right.value
        elif expr.value == '/':
            result = left.value / right.value
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
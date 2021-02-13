'''Python file for compiler's lexer

This contains the Lexer class which handles turning the input text(raw expression) into a series of tokens
'''

# Importing token types
from ..tokens import Token
from ..tokens.token_type import PLUS, MINUS, MUL, DIV, MODULUS, INT_DIV, POWER, LPARAM, RPARAM, COMMA, EOF
from ..tokens.token_type import NUMBER, IDENTIFIER, STRING
from ..tokens.token_type import RESERVED_KEYWORDS 

# Building the Lexer class
class Lexer(object):
    def __init__(self, text):
        self.__text = text
        self.__tokens = []
        self.__cur_pos = 0
    
    # Class helper methods
    def __check_end(self, pos: int):
        '''
        Helper private method to check if the position given has already reached the end of the text
        '''
        return pos >= len(self.__text)
        
    def __get_char(self, pos: int):
        '''
        Helper private method to get the char at a given pos
        If the pos has reached the end, return None
        '''
        if not self.__check_end(pos):
            return self.__text[pos]
        return None
    
    # TODO: Chuan Hao, implement the syntax error
    def __syntax_error(self):
        pass

    def __error(self):
        # Placeholder error method
        # TODO: Make proper one
        raise Exception('Lexer error')

    # Class auxiliary methods
    @property
    def __cur_char(self):
        '''
        Auxiliary private method to return the current char of the lexer
        '''
        return self.__get_char(self.__cur_pos)

    @property
    def __peek(self):
        '''
        Auxiliary private method to peek at the next char without moving the lexer
        '''
        return self.__get_char(self.__cur_pos + 1)
    
    @property
    def __is_end(self):
        '''
        Auxiliary private method to check if the lexer has reached the end
        '''
        return self.__check_end(self.__cur_pos)
    
    def __advance(self):
        '''
        Auxiliary private method to advance the lexer to the next character
        '''
        self.__cur_pos += 1
    
    # Lexer, utility methods
    def __is_whitespace(self, c: str):
        if c is None:
            return False
        return c.isspace()
    
    def __is_quote(self, c: str):
        if c is None:
            return False
        return c == "\'"
    
    def __is_digit(self, c: str):
        if c is None:
            return False
        return c.isdigit()
    
    def __is_alpha(self, c: str):
        if c is None:
            return False
        return c.isalpha()
    
    # Lexer logic methods
    def __skip_whitespace(self):
        '''
        Private method used to skip whitespace as it is ignored
        '''
        while self.__is_whitespace(self.__cur_char):
            self.__advance()
        return
    
    def __number(self):
        '''
        Private method used to tokenize number tokens
        '''
        pos = self.__cur_pos
        number_value = ''
        # For any digits before, DIGIT*
        while self.__is_digit(self.__cur_char):
            number_value += self.__cur_char
            self.__advance()
        # If there is a '.'
        if self.__cur_char == '.':
            number_value += '.'
            self.__advance()
            # Rest of DIGIT+
            while self.__is_digit(self.__cur_char):
                number_value += self.__cur_char
                self.__advance()
        # Error checking if it was only a .
        if number_value == '.':
            self.__error()
        
        number_value = float(number_value)
        return Token(NUMBER, number_value, pos)
    
    def __identifier(self):
        '''
        Private method used to tokenize identifiers

        Differentiated with no quotes and only alphas
        '''
        pos = self.__cur_pos
        identifier_value = ''
        while self.__is_alpha(self.__cur_char):
            identifier_value += self.__cur_char
            self.__advance()

        # Invalid identifier
        # Only accepts reserved keywords
        if identifier_value not in RESERVED_KEYWORDS:
            self.__error()
        return Token(identifier_value, identifier_value, pos)
    
    def __string(self):
        '''
        Private method used to tokenize strings
        '''
        pos = self.__cur_pos
        string_value = ''
        # Need first quote
        if self.__is_quote(self.__cur_char):
            self.__advance()
        else:
            self.__error()

        # Consume all chars in the middle
        while not self.__is_quote(self.__cur_char) and self.__cur_char is not None:
            string_value += self.__cur_char
            self.__advance()

        # Need ending quote
        if self.__is_quote(self.__cur_char):
            self.__advance()
        else:
            self.__error()
        
        return Token(STRING, string_value, pos)
    
    # Main lexer methods
    def __get_next_token(self):
        '''
        Private method to get the next token from the given text
        '''
        if not self.__is_end:
            # Skipping all the ignored chars
            if self.__is_whitespace(self.__cur_char):
                self.__skip_whitespace()
                return self.__get_next_token()
            
            # Checking single char tokens
            if self.__cur_char == '+':
                token = Token(PLUS, '+', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == '-':
                token = Token(MINUS, '-', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == '%':
                token = Token(MODULUS, '%', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == '(':
                token = Token(LPARAM, '(', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == ')':
                token = Token(RPARAM, ')', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == ',':
                token = Token(COMMA, ',', self.__cur_pos)
                self.__advance()
                return token
            
            # Checking double char tokens
            if self.__cur_char == '*':
                # If POWER
                if self.__peek == '*':
                    token = Token(POWER, '**', self.__cur_pos)
                    self.__advance()
                    self.__advance()
                    return token
                # else MUL
                token = Token(MUL, '*', self.__cur_pos)
                self.__advance()
                return token
            elif self.__cur_char == '/':
                # If INT_DIV
                if self.__peek == '/':
                    token = Token(INT_DIV, '//', self.__cur_pos)
                    self.__advance()
                    self.__advance()
                    return token
                # else DIV
                token = Token(DIV, '/', self.__cur_pos)
                self.__advance()
                return token
            
            # Check multi-strings
            # Check NUMBER, then IDENTIFIER, then STRING
            if self.__is_digit(self.__cur_char) or self.__cur_char == '.':
                return self.__number()
            elif self.__is_alpha(self.__cur_char):
                return self.__identifier()
            elif self.__is_quote(self.__cur_char):
                return self.__string()
            
            # If not able to tokenize, error
            self.__error()

        # If we have reached the end, EOF
        return Token(EOF, None, self.__cur_pos)

    # Public methods
    def get_tokens(self):
        '''
        Public method to get the tokens tokenized by the lexer
        '''
        # If lexer has already tokenized the text
        if len(self.__tokens) > 0:
            return self.__tokens
        
        tokens = []
        while True:
            cur_token = self.__get_next_token()
            tokens.append(cur_token)

            if cur_token.type == EOF:
                break
        self.__tokens = tokens
        return self.__tokens

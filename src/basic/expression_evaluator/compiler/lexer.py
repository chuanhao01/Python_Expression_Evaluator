
'''
## This is the Python File containing the main 'Lexer' class

#* The main purpose is to tokenize all the characters in the input expression provided by the user
#! Take note that there will be no checking of the syntax of the input expression in this class
''' 

from ..tokens import Token
from ..tokens import INIT, EOF, WHITESPACE, OPERATOR, NUMBER, PLUS, MINUS, MUL, DIV, POWER, LPARAN, RPARAN, DOT 

class Lexer(object):
    def __init__(self, text):
        self.__text = text.strip()

        # Indexing input text
        self.__pos = 0
        self.__current_char = self.__text[self.__pos]

        # Tokenizing
        self.__current_token_type = INIT
        self.__current_token_value = None

    #* Getters ( No need for Setters because these attributes should only be altered within the class )
    def get_text(self):
        return self.__text

    def get_pos(self):
        return self.__pos

    def get_current_char(self):
        return self.__current_char

    def get_current_token_type(self):
        return self.__current_token_type

    def get_current_token_value(self):
        return self.__current_token_value

    
    def __error(self, error_type, character = None):
        if error_type == "unrecognised_token_type":
            raise Exception(f"Lexical Error: Invalid character(s) detected\n")

        elif error_type == "unrecognised_operator":
            raise Exception(f"Lexical Error: Support for the {character} operator has not yet been implemented\n")

        elif error_type == "invalid_float":
            raise Exception(f"Lexical Error: Invalid float / integer value(s)\n")

        else:
            raise SystemError("An unexpected error has occurred in the Lexer.. Please try again\n")


    def __check_token_type(self, char):
        #* Checks and returns the token_type of the character passed in

        if char == None:
            return EOF

        if char.isspace():
            return WHITESPACE
        
        if char.isdigit():
            return NUMBER

        if char == "(":
            return LPARAN

        if char == ")":
            return RPARAN

        if char in ["+", "-", "*", "/"]:
            return OPERATOR

        if char == ".":
            return DOT

        #! The character passed in does not match any token type, raise an __error
        error_type = "unrecognised_token_type"
        self.__error(error_type)

    def __peek(self):
        #* "Peek" into the next character of the input expression and,
        #* return this character if it is not the end of the input expression

        pos = self.__pos + 1

        if pos >= len(self.__text):
            return None
        return self.__text[pos]

    def __advance(self):
        #* Advance to the next character of the input expression and,
        #* Update self.__current_char if not reached the end of the input expression

        self.__pos += 1

        if self.__pos >= len(self.__text):
            self.__current_char = None
        else:
            self.__current_char = self.__text[self.__pos]

    def __differentiate_between_operators(self):
        #* Check and differentiate between the different types of accepted operators:
        #* PLUS, MINUS, MUL, DIV, POWER
        #* Then, update the current_token_type to represent the actual operator

        if self.__current_token_value == "*":
            if self.__peek() == "*":
                self.__advance()
                self.__current_token_value += self.__current_char
                self.__current_token_type = POWER
            else:
                self.__current_token_type = MUL

        elif self.__current_token_value == "+":
            self.__current_token_type = PLUS

        elif self.__current_token_value == "-":
            self.__current_token_type = MINUS
    
        elif self.__current_token_value == "/":
            self.__current_token_type = DIV

        #! Theorectically, this should never occur as a check is made previously to 
        #! determine if self.current_token is an OPERATOR token type.
        #! However, we are still checking just in case
        else:
            error_type = "unrecognised_operator"
            self.__error(error_type, self.__current_token_value)
    
    def __get_number(self):
        #* Get the entirety of the NUMBER value, whether it is a Float or an Integer

        number_value = self.__current_char

        # Normal Integer
        while self.__check_token_type(self.__peek()) == NUMBER:
            self.__advance()
            number_value += self.__current_char

        # Float Number
        if self.__check_token_type(self.__peek()) == DOT:
            number_value += "."
            self.__advance()

            #! If the next character after "." is not a number,
            #! Raise an __error
            if self.__check_token_type(self.__peek()) != NUMBER:
                error_type = "invalid_float"
                self.__error(error_type)

            while self.__check_token_type(self.__peek()) == NUMBER:
                self.__advance()
                number_value += self.__current_char

                if self.__check_token_type(self.__peek()) == DOT:
                    error_type = "invalid_float"
                    self.__error(error_type)

        self.__current_token_value = float(number_value)
        self.__advance()

    def __get_next_token(self):
        #* Gets and returns the next token of the input string
        #* If the next token is a WHITESPACE, continue advancing to the next non-WHITESPACE token
        
        # EOF
        if self.__current_char == None:
            return Token(EOF, None)

        self.__current_token_value = ""
        self.__current_token_value += self.__current_char
        self.__current_token_type = self.__check_token_type(self.__current_char)

        # WHITESPACE
        if self.__current_token_type == WHITESPACE:
            while self.__check_token_type(self.__peek()) == WHITESPACE:
                self.__advance()

            self.__advance()
            return self.__get_next_token()
        
        # OPERATORS
        if self.__current_token_type == OPERATOR:
            self.__differentiate_between_operators()
            self.__advance()
            return Token(self.__current_token_type, self.__current_token_value)

        # PARANTHESIS
        elif self.__current_token_type == LPARAN or self.__current_token_type == RPARAN:
            self.__advance()
            return Token(self.__current_token_type, self.__current_token_value)
        
        # NUMBER
        elif self.__current_token_type == DOT or self.__current_token_type == NUMBER:
            self.__get_number()
            return Token(NUMBER, self.__current_token_value)

        #! If this point is reached,
        #! The next char does not have a recognised token type
        error_type = "unrecognised_token_type"
        self.__error(error_type)

    def get_all_tokens(self):
        #* Continuously calls get_next_token() until the entire input expression has been transformed into tokens

        # The starting token is always an INIT
        init_token = Token(INIT, None)
        tokens = [init_token]

        while True:
            current_token = self.__get_next_token()
            tokens.append(current_token)

            # The last token is always an EOF
            if current_token.token_type == EOF:
                break

        return tokens
'''
This Python File contains the main 'Parser' class

#* Its main purpose is to parse the sequence of tokens from the lexer and check the grammer
#! At this stage, it is assumed that all characters in the input __expression is a valid token
'''

from ..tokens import Token
from ..tokens import INIT, EOF, WHITESPACE, OPERATOR, NUMBER, PLUS, MINUS, MUL, DIV, POWER, LPARAN, RPARAN, DOT 
from ..nodes import Number_Node, BinaryOp_Node
from .lexer import Lexer


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.all_tokens = lexer.get_all_tokens()

        self.token_index = 0
        self.current_token = self.all_tokens[self.token_index]

    #* Utilities

    def __error(self, error_type):
        if error_type == "non-matching_token_types" or error_type == "internal_error":
            raise SystemError("An internal __error has occurred in the parser.. Please try again\n")

        elif error_type == "multiple_consecutive_operators":
            raise SyntaxError("There are multiple consecutive operators in your expression..\n")

        elif error_type == "multiple_consecutive_numbers":
            raise SyntaxError("There are multiple consecutive numbers in your expression with no operators between..\n")

        elif error_type == "term_error":
            raise SyntaxError("Multiple expressions detected.. Please try again\n")

        elif error_type == "factor_error":
            raise SystemError("An unexpected error has occurred in the Parser.. Please check your NUMBER inputs\n")

        elif error_type == "incorrect_paranthesis" or error_type == "!EOF":
            raise SyntaxError("The expression provided is not a legal fully paranthesised expression\n")

        else:
            raise SystemError("An unexpected error has occurred in the Parser.. Please try again\n")


    def __advance(self):
        #* Advance to the next character of the input __expression and,
        #* Update self.current_token if not reached the end of the stream of tokens

        if self.token_index < len(self.all_tokens):
            self.token_index += 1
            self.current_token = self.all_tokens[self.token_index]

    def __peek(self):
        #* "Peek" into the next token of the stream of tokens and,
        #* return this token if it is not the end of the stream of tokens

        pos = self.token_index + 1

        if pos < len(self.all_tokens):
            return self.all_tokens[pos]
        
        return None

    def __eat(self, token_type):
        #* Compare the current token type with the passed token type
        #* If they match, "__eat" the current token and __advance to next token
        #* Else, raise an Exception __error
        if self.current_token.token_type == token_type:
            self.__advance()

        else:
            error_type = "non-matching_token_types"
            self.__error(error_type)


    #* Grammer

    def __expr(self):
        ''' LPARAN TERM ( (OPERATOR) TERM )* RPARAN '''

        # Performing a check for INIT token
        # If INIT Token is found, raise an __error
        # This should only occur if this is called separately from self.parse()
        if self.current_token.token_type == INIT:
            error_type = "internal_error"
            self.__error(error_type)

        node = None
        left___term = self.__term()

        if self.current_token.token_type in [PLUS, MINUS, MUL, DIV, POWER]:
            # Peek and make sure that the next token is not an OPERATOR 
            # (with the exception of MINUS due to MINUS FACTOR)
            # If it is an operator, raise and __error
            if self.__peek().token_type in [PLUS, MUL, DIV, POWER]:
                error_type = "multiple_consecutive_operators"
                self.__error(error_type)

            node = self.current_token
            
            if self.current_token.token_type == PLUS:
                self.__eat(PLUS)
            elif self.current_token.token_type == MINUS:
                self.__eat(MINUS)
            elif self.current_token.token_type == MUL:
                self.__eat(MUL)
            elif self.current_token.token_type == DIV:
                self.__eat(DIV)
            elif self.current_token.token_type == POWER:
                self.__eat(POWER)

            right___term = self.__term()
            node = BinaryOp_Node(left___term, node, right___term)
            
            if self.current_token.token_type != RPARAN:
                error_type = "incorrect_paranthesis"
                self.__error(error_type)

        elif self.current_token.token_type != RPARAN:
            error_type = "incorrect_paranthesis"
            self.__error(error_type)

        if node == None:
            return left___term

        return node

    def __term(self):
        ''' FACTOR | EXPR '''

        # EXPR
        if self.current_token.token_type == LPARAN:
            self.__eat(LPARAN)

            node = self.__expr()
            return node

        # FACTOR
        elif self.current_token.token_type == NUMBER or (self.__peek().token_type == NUMBER and self.current_token.token_type == MINUS):
            node = self.__factor()
            return node

        else:
            error_type = "term_error"
            self.__error(error_type)

    def __factor(self):
        ''' MINUS FACTOR | NUMBER '''
        node = self.current_token

        # NUMBER
        if node.token_type == NUMBER:
            #* Peek and make sure that the next token is not a NUMBER
            #* If it is, raise an __error
            if self.__peek().token_type == NUMBER:
                error_type = "multiple_consecutive_numbers"
                self.__error(error_type)

            self.__eat(NUMBER)
            return Number_Node(node)
        
        # MINUS FACTOR
        if node.token_type == MINUS:
            self.__eat(MINUS)

            self.current_token.token_value *= -1
            node = self.current_token

            self.__eat(NUMBER)
            return Number_Node(node)

        error_type = "factor_error"
        self.__error(error_type)


    #* Main

    def parse(self):
        #* Parse the stream of tokens, checking the grammer

        # Perform a check of the Paranthesis count before starting any parsing
        left_paran_count = right_paran_count = 0
        for token in self.all_tokens:
            if token.token_type == LPARAN:
                left_paran_count += 1
            if token.token_type == RPARAN:
                right_paran_count += 1

        # Basics of fully-paranthesised __expressions -> same count of left and right paranthesis && even number of paranthesis overall
        if left_paran_count != right_paran_count or (left_paran_count + right_paran_count) % 2 != 0 or left_paran_count < 1 or right_paran_count < 1:
            error_type = "incorrect_paranthesis"
            self.__error(error_type)


        # If this point is reached, the paranthesis check has passed
        # As such, "eat" the INIT token and start parsing
        self.__eat(INIT)
        ast = self.__expr()

        return ast
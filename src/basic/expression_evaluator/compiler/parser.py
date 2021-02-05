'''
This Python File contains the main 'Parser' class that will:
parse the sequence of tokens from the lexer and check the grammer
'''

from ..tokens import Token
from ..tokens import INIT, EOF, WHITESPACE, OPERATOR, NUMBER, PLUS, MINUS, MUL, DIV, POWER, LPARAN, RPARAN, DOT 
from ..nodes import Number_Node, BinaryOp_Node
from .lexer import Lexer

accepted_operators = [PLUS, MINUS, MUL, DIV, POWER]

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.all_tokens = lexer.get_all_tokens()

        self.token_index = 0
        self.current_token = self.all_tokens[self.token_index]

    #* Utilities

    def error(self):
        #TODO: Change this to an actual error function
        raise Exception("Error during Parsing")

    def advance(self):
        #* Advance to the next character of the input expression and,
        #* Update self.current_token if not reached the end of the stream of tokens

        if self.token_index < len(self.all_tokens):
            self.token_index += 1
            self.current_token = self.all_tokens[self.token_index]

    def peek(self):
        #* "Peek" into the next token of the stream of tokens and,
        #* return this token if it is not the end of the stream of tokens

        pos = self.token_index + 1

        if pos < len(self.all_tokens):
            return self.all_tokens[pos]
        
        return None

    def eat(self, token_type):
        #* Compare the current token type with the passed token type
        #* If they match, "eat" the current token and advance to next token
        #* Else, raise an Exception error
        if self.current_token.token_type == token_type:
            self.advance()

        else:
            self.error()


    #* Grammer

    def expr(self):
        ''' LPARAN TERM ( (OPERATOR) TERM )* RPARAN '''

        # Performing a check for INIT token
        # If INIT Token is found, raise an error
        # This should only occur if this is called separately from self.parse()
        if self.current_token.token_type == INIT:
            self.error()

        node = None
        left_term = self.term()

        while self.current_token.token_type in accepted_operators:
            # Peek and make sure that the next token is not an OPERATOR
            # If it is an operator, raise and error
            if self.peek().token_type in accepted_operators:
                self.error()

            node = self.current_token
            
            if self.current_token.token_type == PLUS:
                self.eat(PLUS)
            if self.current_token.token_type == MINUS:
                self.eat(MINUS)
            if self.current_token.token_type == MUL:
                self.eat(MUL)
            if self.current_token.token_type == DIV:
                self.eat(DIV)
            if self.current_token.token_type == POWER:
                self.eat(POWER)

            node = BinaryOp_Node(left_term, node, self.term())

        if node == None:
            return left_term

        return node

    def term(self):
        ''' FACTOR | EXPR '''

        # EXPR
        if self.current_token.token_type == LPARAN:
            self.eat(LPARAN)

            node = self.expr()
            return node

        # FACTOR
        elif self.current_token.token_type == NUMBER or (self.peek().token_type == NUMBER and self.current_token.token_type == MINUS):
            node = self.factor()
            return node

        else:
            self.error()

    def factor(self):
        ''' MINUS FACTOR | NUMBER '''
        node = self.current_token

        # NUMBER
        if node.token_type == NUMBER:
            #* Peek and make sure that the next token is not a NUMBER
            #* If it is, raise an error
            if self.peek().token_type == NUMBER:
                self.error()

            self.eat(NUMBER)
            return Number_Node(node)
        
        # MINUS FACTOR
        if node.token_type == MINUS:
            self.eat(MINUS)

            self.current_token.token_value *= -1
            node = self.current_token

            self.eat(NUMBER)
            return Number_Node(node)

        self.error()


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

        if left_paran_count != right_paran_count or (left_paran_count + right_paran_count) % 2 != 0 or left_paran_count < 1 or right_paran_count < 1:
            self.error()

        # If this point is reached, the paranthesis check has passed
        # As such, "eat" the INIT token and start parsing
        self.eat(INIT)
        return self.expr()
'''Python file for compiler's parser

This contains the parser, which creates the AST from a series of tokens
'''
# Importing token types
from ..tokens import Token
from ..tokens.token_type import PLUS, MINUS, MUL, DIV, MODULUS, INT_DIV, POWER, LPARAM, RPARAM, COMMA, EOF
from ..tokens.token_type import NUMBER, IDENTIFIER, STRING

# Importing nodes
from ..nodes import Number_Node, String_Node, Unary_Node, BinaryOp_Node, Function_Node

class Parser(object):
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__cur_pos = 0
        # When the ast is fully built
        self.__ast = None

    # Class helper methods
    def __check_end(self, pos: int):
        '''
        Helper private method to check if the position given has already reached the end of the given tokens
        '''
        return self.__cur_pos >= len(self.__tokens)
    
    def __get_token(self, pos: int):
        '''
        Helper private method to get the token at a given pos
        If the token has reached the end, return None
        '''
        if not self.__check_end(pos):
            return self.__tokens[pos]
        return None
    
    def __check_match_token_type(self, token: Token, token_types: list):
        '''
        Helper private method to see if given token matches any of the given types
        '''
        if token is None:
            return False
        return token.type in set(token_types)

    def __error(self):
        # Placeholder error method
        # TODO: Make proper one
        raise Exception('Parser error')
    
    # Class auxiliary methods
    @property
    def __is_end(self):
        '''
        Auxiliary private method to check if the parser has reached the end of the tokens given
        '''
        return self.__check_end(self.__cur_pos)

    @property
    def __cur_token(self) -> Token:
        '''
        Auxiliary private method used to get the current token the parser is on
        '''
        return self.__get_token(self.__cur_pos)
    
    @property
    def __peek(self):
        '''
        Auxiliary private method peek at the next token
        '''
        return self.__get_token(self.__cur_pos + 1)
    
    def __advance(self):
        '''
        Auxiliary private method to advance the parser
        '''
        self.__cur_pos += 1
    
    def __match_token(self, token_types: list):
        '''
        Auxiliary private method to check if current token match given token_types
        '''
        return self.__check_match_token_type(self.__cur_token, token_types)
    
    def __consume(self, token_types: list):
        '''
        Auxiliary private method to check if the current token's type matches the given token_types
        Consumes the token if it is
        '''
        if self.__match_token(token_types):
            self.__advance()
        else:
            # TODO: Err shld be specific to token types given
            self.__error()
        
    # Parser Grammar implementation
    def __expression(self):
        node = self.__term()
        token_types = [PLUS, MINUS, MODULUS]
        while self.__match_token(token_types):
            token = self.__cur_token
            self.__consume(token_types)
            node = BinaryOp_Node(token, node, self.__term())
        return node
    
    def __term(self):
        node = self.__factor()
        token_types= [MUL, DIV, INT_DIV]
        while self.__match_token(token_types):
            token = self.__cur_token
            self.__consume(token_types)
            node = BinaryOp_Node(token, node, self.__factor())
        return node
    
    def __factor(self):
        node = self.__unary()
        token_types = [POWER]
        while self.__match_token(token_types):
            token = self.__cur_token
            self.__consume(token_types)
            node = BinaryOp_Node(token, node, self.__unary())
        return node
    
    # TODO: Chuan Hao
    # Think of a better way to check and continue to store token types to check
    def __unary(self):
        if self.__match_token([PLUS, MINUS]):
            token = self.__cur_token
            self.__consume([PLUS, MINUS])
            return Unary_Node(token, self.__unary())
        else:
            return self.__call()

    def __call(self):
        if self.__match_token([IDENTIFIER]):
            token = self.__cur_token
            self.__consume([IDENTIFIER])
            self.__consume([LPARAM])
            # Else we have arguments to parse
            arguments = self.__arguments()
            self.__consume([RPARAM])
            return Function_Node(token, arguments)

        else:
            return self.__primary()
    
    def __arguments(self) -> list:
        nodes = []
        # To tell if there are more expression, check for ending of function
        if not self.__match_token([RPARAM]):
            nodes.append(self.__expression())
            while self.__match_token([COMMA]):
                self.__consume([COMMA])
                nodes.append(self.__expression())
        return nodes

    def __primary(self):
        if self.__match_token([NUMBER]):
            token = self.__cur_token
            self.__consume([NUMBER])
            return Number_Node(token)
        elif self.__match_token([STRING]):
            token = self.__cur_token
            self.__consume([STRING])
            return String_Node(token)
        elif self.__match_token([LPARAM]):
            self.__consume([LPARAM])
            expression = self.__expression()
            self.__consume([RPARAM])
            return expression
        else:
            # If when parsing, primary grammar fails, there is an error
            self.__error()
    
    # Main Parser logic
    def __parse(self):
        '''
        Private method for the parser to parse the given tokens into the ast
        '''
        # TODO: Chuan Hao
        # What if there is nothing
        ast = self.__expression()
        if not self.__match_token([EOF]):
            # TODO: Chuan Hao
            # Should have parsed all tokens and left EOF
            self.__error()
        return ast

    # Public methods
    def get_ast(self):
        '''
        Public method to get the ast of the parser
        '''
        # Check if ast has already been parsed
        if self.__ast is not None:
            return self.__ast
        self.__ast = self.__parse()        
        return self.__ast




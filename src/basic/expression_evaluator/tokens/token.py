
'''
This Python file contains the 'Token' class

Each individual token should have a token_type and a token_value
'''

class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self):
        return f"TOKEN({self.token_type}, {self.token_value})"
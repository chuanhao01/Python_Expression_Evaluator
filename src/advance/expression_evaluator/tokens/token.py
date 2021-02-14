'''Python file contain the Token Class

The Token Class is used to create tokens by the lexer
These token are later parsed by the parser
'''

class Token(object):
    def __init__(self, _type: str, value, pos: int):
        self.type = _type
        self.value = value
        self.pos = pos
    
    def __str__(self):
        s = f"Token({self.type}, {self.value})"
        return s
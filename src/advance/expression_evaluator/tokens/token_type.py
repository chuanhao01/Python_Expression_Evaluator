'''Python file for all the token types

This contains all the static token types used in the evaluator
'''
# Special Tokens
# +, -, *, /, %
PLUS, MINUS, MUL, DIV, MODULUS = ['PLUS', 'MINUS', 'MUL', 'DIV', 'MODULUS']
# **, //
INT_DIV, POWER = ['INT_DIV', 'POWER']
# (, )
LPARAM, RPARAM = ['LPARAM', 'RPARAM']
# ,
COMMA = 'COMMA'
EOF = 'EOF'

# Normal Token Types
NUMBER = 'NUMBER'
IDENTIFIER = 'IDENTIFIER'
STRING = 'STRING'

# Reserved Keywords
RESERVED_KEYWORDS = set([
    # Arity 0
    'E', 'PI',
    # Arity 1
    'sin', 'cos', 'tan', 'floor', 'ceil', 'ln', 'lg', 'factorial', 'sqrt', 'bin', 'hex',
    # Arity 2
    'log', 'pow', 'mod', 'perm', 'combo'
])

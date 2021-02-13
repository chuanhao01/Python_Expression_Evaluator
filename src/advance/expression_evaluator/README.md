# Grammar
```python
'''
--- Special Tokens ---
PLUS: '+'
MINUS: '-'
MODULUS: '%'
MUL: '*'
DIV: '/'
INT_DIV: '//'
POWER: '**'
LPARAM: '('
RPARAM: ')'
COMMA: ','

EOF: 'EOF'

--- Normal Tokens ---
NUMBER, IDENTIFIER, STRING

--- Lexical Grammar ---
NUMBER: DIGIT* ('.' DIGIT+)?
IDENTIFIER: ALPHA+
STRING: '\'' <any char except '\''>* '\''
DIGIT: '0' ... '9'
ALPHA: 'a' ... 'z' | 'A' ... 'Z'

--- Syntax Grammar ---
expression: term (('+' | '-' | '%') term)*
term: factor (('*' | '/' | '//') factor)*
factor: unary (('**') unary)*
unary: ('+' | '-') unary
	| call
call: primary ('(' arguments ')')?
primary: NUMBER
	| IDENTIFIER
	| '(' expression ')'
arguments: expression ((',') expression)*

--- Reserved Keywords ---
Arity 0: E, PI
Arity 1: sin, cos, tan, floor, ceil, ln, lg, factorial, sqrt, bin, hex
Arity 2: log, pow, mod, perm, comb
'''
```
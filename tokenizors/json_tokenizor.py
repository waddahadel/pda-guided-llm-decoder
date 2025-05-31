import re

class JsonTokenizer:
    def __init__(self):
        self.token_specification = [
            ('STRING',      r'"[^"\\]*(?:\\.[^"\\]*)*"'),  # Quoted string
            ('NUMBER',      r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'),  # Integer/float
            ('TRUE',        r'true'),
            ('FALSE',       r'false'),
            ('NULL',        r'null'),
            ('LBRACE',      r'\{'),
            ('RBRACE',      r'\}'),
            ('LBRACKET',    r'\['),
            ('RBRACKET',    r'\]'),
            ('COLON',       r':'),
            ('COMMA',       r','),
            ('WHITESPACE',  r'[ \t\n\r]+'),  # Skip whitespace
            ('MISMATCH',    r'.'),           # Any other character
        ]
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification))

    def tokenize(self, json_str):
        tokens = []
        for match in self.regex.finditer(json_str):
            kind = match.lastgroup
            value = match.group()

            if kind == 'WHITESPACE':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Unexpected character: {value}")
            else:
                tokens.append(value)
        return tokens

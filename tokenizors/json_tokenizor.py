import re

class JsonTokenizer:
    def __init__(self):
        self.token_specification = [
            ('STRING',         r'"[^"\\]*(?:\\.[^"\\]*)*"'),  
            ('PARTIAL_STRING', r'"[^"\\]*(?:\\.[^"\\]*)*'),   
            ('NUMBER',         r'-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'),  
            ('PARTIAL_NUMBER', r'-?\d+(?:\.\d*|[eE][+-]?)?$'),        
            ('TRUE',           r'true'),
            ('FALSE',          r'false'),
            ('NULL',           r'null'),
            ('LBRACE',         r'\{'),
            ('RBRACE',         r'\}'),
            ('LBRACKET',       r'\['),
            ('RBRACKET',       r'\]'),
            ('COLON',          r':'),
            ('COMMA',          r','),
            ('WHITESPACE',     r'[ \t\n\r]+'),  
            ('MISMATCH',       r'.'),           
        ]
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification))

    def tokenize(self, json_str, allow_partial=False):
        tokens = []
        pos = 0
        while pos < len(json_str):
            match = self.regex.match(json_str, pos)
            if not match:
                raise SyntaxError(f"Unexpected character at position {pos}: {json_str[pos]!r}")

            kind = match.lastgroup
            value = match.group().strip()  
            
            if kind == 'WHITESPACE':
                pos = match.end()
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"Unexpected character: {value}")
            elif kind in ('PARTIAL_STRING', 'PARTIAL_NUMBER'):
                if allow_partial:
                    tokens.append(value)
                else:
                    raise SyntaxError(f"Incomplete token: {value}")
            else:
                tokens.append(value)
            pos = match.end()
        return tokens

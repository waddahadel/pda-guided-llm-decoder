import copy

class JsonPDA:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.state = 'START'
        self.stack = []
        self.buffer = ""  # For building strings/numbers
        self.escape = False  # For tracking escape sequences
        self.last_states = []  # For nested state tracking
    
    def clone(self):
        return copy.deepcopy(self)
    
    def consume_char(self, char, partial=False):
        # Handle string escape sequences first
        if self.state == 'IN_STRING':
            if self.escape:
                self.buffer += char
                self.escape = False
                return True
            elif char == '\\':
                self.escape = True
                return True
            elif char == '"':
                self.state = self.stack.pop()  # Return to previous state
                return True
            else:
                self.buffer += char
                return True
        
        # Skip whitespace except in strings
        if char.isspace() and self.state != 'IN_STRING':
            return True
            
        # Main state machine
        if self.state == 'START':
            if char == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif char == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END'
                return True
            return False
        
        elif self.state == 'EXPECT_KEY_OR_END':
            if char == '}':
                if not self.stack or self.stack.pop() != '}':
                    return False
                self.state = self._get_next_state()
                return True
            elif char == '"':
                self.stack.append('EXPECT_COLON')
                self.state = 'IN_STRING'
                self.buffer = ""
                return True
            return False
        
        elif self.state == 'EXPECT_COLON':
            if char == ':':
                self.state = 'EXPECT_VALUE'
                return True
            return False
        
        elif self.state == 'EXPECT_VALUE':
            if char == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif char == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END'
                return True
            elif char == '"':
                self.stack.append('EXPECT_COMMA_OR_END')
                self.state = 'IN_STRING'
                self.buffer = ""
                return True
            elif self._is_primitive_start(char):
                self.stack.append('EXPECT_COMMA_OR_END')
                self.state = 'IN_PRIMITIVE'
                self.buffer = char
                return True
            return False
        
        elif self.state == 'IN_PRIMITIVE':
            if self._is_primitive_char(char):
                self.buffer += char
                return True
            else:
                # End of primitive
                if not self._validate_primitive():
                    return False
                self.state = self.stack.pop()
                return self.consume_char(char, partial)  # Reprocess the char
        
        elif self.state == 'EXPECT_VALUE_OR_END':
            if char == ']':
                if not self.stack or self.stack.pop() != ']':
                    return False
                self.state = self._get_next_state()
                return True
            elif char in '{["' or self._is_primitive_start(char):
                self.stack.append('EXPECT_COMMA_OR_END')
                return self.consume_char(char, partial)
            return False
        
        elif self.state == 'EXPECT_COMMA_OR_END':
            if char == ',':
                top = self.stack[-1] if self.stack else None
                if top == '}':
                    self.state = 'EXPECT_KEY_OR_END'
                else:
                    self.state = 'EXPECT_VALUE_OR_END'
                return True
            elif char in ']}':
                if not self.stack or self.stack[-1] != char:
                    return False
                self.stack.pop()
                self.state = self._get_next_state()
                return True
            return False
        
        elif self.state == 'END':
            return False
        
        return False
    
    def _get_next_state(self):
        if not self.stack:
            return 'END'
        top = self.stack[-1]
        return 'EXPECT_COMMA_OR_END' if top in '}]' else 'END'
    
    def _is_primitive_start(self, char):
        return char.isdigit() or char == '-' or char.lower() in ('t', 'f', 'n')
    
    def _is_primitive_char(self, char):
        if not self.buffer:
            return False
        first_char = self.buffer[0].lower()
        
        # Number
        if first_char.isdigit() or first_char == '-':
            return (char.isdigit() or char in '.eE+-' or 
                   (char in 'eE' and 'e' not in self.buffer.lower() and 
                    'E' not in self.buffer.lower()))
        # Boolean/null
        elif first_char == 't':
            return len(self.buffer) < 4 and char in 'true'[len(self.buffer):]
        elif first_char == 'f':
            return len(self.buffer) < 5 and char in 'false'[len(self.buffer):]
        elif first_char == 'n':
            return len(self.buffer) < 4 and char in 'null'[len(self.buffer):]
        return False
    
    def _validate_primitive(self):
        if not self.buffer:
            return False
        s = self.buffer.lower()
        if s in ('true', 'false', 'null'):
            return True
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def accepts(self, chars, partial=False):
        self.reset()
        for i, char in enumerate(chars):
            if not self.consume_char(char, partial):
                if partial and i == len(chars)-1 and self._is_partial_acceptable():
                    return True
                return False
        return True if partial else (self.state == 'END' and not self.stack)
    
    def _is_partial_acceptable(self):
        return (self.state in ('IN_STRING', 'IN_PRIMITIVE') or 
               (self.state == 'EXPECT_VALUE' and self.buffer) or
               (self.state == 'EXPECT_VALUE_OR_END' and self.buffer))
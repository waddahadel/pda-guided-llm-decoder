import copy

class JsonPDA:
    """
    Push-down automaton that validates JSON *incrementally*.
    This version includes full support for the JSON number format, including
    scientific notation and leading decimal points.
    """

   
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "START"
        self.stack = []          
        self.buffer = ""         
        self.escape = False     

    def clone(self):
        """Deep-copy so each beam can branch independently."""
        return copy.deepcopy(self)

   
    def consume_char(self, char, *, partial=False):
        """
        Feed one character. Return **True** if the prefix can still form
        valid JSON; **False** if it is already impossible.
        """
        
        if self.state == "IN_STRING":
            if self.escape:
                self.buffer += char
                self.escape = False
                return True
            if char == "\\":
                self.escape = True
                return True
            if char == '"':
                self.state = self.stack.pop()
                return True
            self.buffer += char
            return True

        if char.isspace():
            return True

        if self.state == "START":
            if char == "{":
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            if char == "[":
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            if char == '"':
                self.stack.append("END")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            if self._is_primitive_start(char):
                self.stack.append("END") 
                self.state = "IN_PRIMITIVE"
                self.buffer = char
                return True
            return False

        
        if self.state == "EXPECT_KEY_OR_END":
            if char == "}":
                if not self.stack or self.stack.pop() != "}": return False
                self.state = self._get_next_state()
                return True
            if char == '"':
                self.stack.append("EXPECT_COLON")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            return False

        if self.state == "EXPECT_COLON":
            if char == ":":
                self.state = "EXPECT_VALUE"
                return True
            return False

        if self.state == "EXPECT_VALUE":
            if char == "{":
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            if char == "[":
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            if char == '"':
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            if self._is_primitive_start(char):
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_PRIMITIVE"
                self.buffer = char
                return True
            return False

       
        if self.state == "IN_PRIMITIVE":
            if self._is_primitive_char(char):
                self.buffer += char
                return True
            if not self._validate_primitive():
                return False
            self.state = self.stack.pop()
            return self.consume_char(char, partial=partial)

        if self.state == "EXPECT_VALUE_OR_END":
            if char == "]":
                if not self.stack or self.stack.pop() != "]": return False
                self.state = self._get_next_state()
                return True
            if char == "{":
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            if char == "[":
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            if char == '"':
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            if self._is_primitive_start(char):
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_PRIMITIVE"
                self.buffer = char
                return True
            return False

        if self.state == "EXPECT_COMMA_OR_END":
            if char == ",":
                top = self.stack[-1] if self.stack else None
                self.state = "EXPECT_KEY_OR_END" if top == "}" else "EXPECT_VALUE_OR_END"
                return True
            if char in "]}":
                if not self.stack or self.stack[-1] != char:
                    return False
                self.stack.pop()
                self.state = self._get_next_state()
                return True
            return False

        if self.state == "END":
            return False

        return False

   
    def _get_next_state(self):
        if not self.stack:
            return "END"
        top = self.stack[-1]
        if top == "END": 
             return "END"
        return "EXPECT_COMMA_OR_END"

    def _is_primitive_start(self, char):
        return char.isdigit() or char in "-." or char.lower() in ("t", "f", "n")

    def _is_primitive_char(self, char):
        if not self.buffer:
            return False
        first = self.buffer[0].lower()

        if first in "tfn":
            if first == "t": return len(self.buffer) < 4 and char in "true"[len(self.buffer):]
            if first == "f": return len(self.buffer) < 5 and char in "false"[len(self.buffer):]
            if first == "n": return len(self.buffer) < 4 and char in "null"[len(self.buffer):]
            return False

        if char.isdigit():
            return True

        if char == '.':
           
            return '.' not in self.buffer and 'e' not in self.buffer.lower()

        if char.lower() == 'e':
     
            return 'e' not in self.buffer.lower()

        if char in "+-":
           
            if len(self.buffer) == 1 and self.buffer[0] == '-':
                 return False
            last_char = self.buffer[-1].lower()
            return last_char == 'e'

        return False

    def _validate_primitive(self):
        if not self.buffer:
            return False
        s = self.buffer.lower()
        if s in ("true", "false", "null"):
            return True
        try:
            float(s)
            return True
        except ValueError:
            return False

    def accepts(self, text, *, partial=False):
        self.reset()
        for idx, ch in enumerate(text):
            if not self.consume_char(ch, partial=True): 
                return False
        
        if self.buffer and not self._validate_primitive():
            return False
        
        final_state = self.state
        if self.buffer:
            final_state = self.stack[-1] if self.stack else "END"

        return partial or (final_state == "END" and not self.stack)

    def _is_partial_acceptable(self):
        return True 

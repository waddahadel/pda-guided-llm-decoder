# json_pda.py

class JsonPDA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'START'
        self.stack = []

    def is_valid_token(self, token):
        if self.state == 'START':
            if token == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif token == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END_ARRAY'
                return True
            elif self.is_value(token):
                self.state = 'END'
                return True
            return False

        elif self.state == 'EXPECT_KEY_OR_END':
            if token == '}':
                if not self.stack or self.stack.pop() != '}':
                    return False
                self.state = self.next_after_value()
                return True
            elif self.is_string(token):
                self.state = 'EXPECT_COLON'
                return True
            return False

        elif self.state == 'EXPECT_COLON':
            if token == ':':
                self.state = 'EXPECT_VALUE'
                return True
            return False

        elif self.state == 'EXPECT_VALUE':
            if token == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif token == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END_ARRAY'
                return True
            elif self.is_value(token):
                self.state = 'EXPECT_COMMA_OR_END_OBJ'
                return True
            return False

        elif self.state == 'EXPECT_COMMA_OR_END_OBJ':
            if token == ',':
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif token == '}':
                if not self.stack or self.stack.pop() != '}':
                    return False
                self.state = self.next_after_value()
                return True
            return False

        elif self.state == 'EXPECT_VALUE_OR_END_ARRAY':
            if token == ']':
                if not self.stack or self.stack.pop() != ']':
                    return False
                self.state = self.next_after_value()
                return True
            elif token == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif token == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END_ARRAY'
                return True
            elif self.is_value(token):
                self.state = 'EXPECT_COMMA_OR_END_ARRAY'
                return True
            return False

        elif self.state == 'EXPECT_COMMA_OR_END_ARRAY':
            if token == ',':
                self.state = 'EXPECT_VALUE_OR_END_ARRAY'
                return True
            elif token == ']':
                if not self.stack or self.stack.pop() != ']':
                    return False
                self.state = self.next_after_value()
                return True
            return False

        elif self.state == 'END':
            return False

        return False

    def next_after_value(self):
        if not self.stack:
            return 'END'
        top = self.stack[-1]
        return {
            '}': 'EXPECT_COMMA_OR_END_OBJ',
            ']': 'EXPECT_COMMA_OR_END_ARRAY',
        }.get(top, 'END')

    def is_value(self, token):
        return (
            self.is_string(token)
            or self.is_number(token)
            or token in ('true', 'false', 'null')
        )

    def is_string(self, token):
        return len(token) >= 2 and token[0] == '"' and token[-1] == '"'

    def is_number(self, token):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def accepts(self, tokens):
        self.reset()
        for token in tokens:
            print(f"Processing token: {token}")
            if not self.is_valid_token(token):
                print(f"Rejected at token: {token}")
                return False
        return self.state == 'END' and len(self.stack) == 0

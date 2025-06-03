import copy

class JsonPDA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'START'
        self.stack = []

    def clone(self):
        return copy.deepcopy(self)

    def log_state(self):
        print(f"[PDA] State: {self.state}, Stack: {self.stack}")

    def __str__(self):
        return f"JsonPDA(state={self.state}, stack={self.stack})"

    def is_valid_token(self, token, partial=False):
        token = token.strip()
        if self.state == 'START':
            if token == '{':
                self.stack.append('}')
                self.state = 'EXPECT_KEY_OR_END'
                return True
            elif token == '[':
                self.stack.append(']')
                self.state = 'EXPECT_VALUE_OR_END_ARRAY'
                return True
            elif self.is_value(token, partial=partial):
                self.state = 'END'
                return True
            return False

        elif self.state == 'EXPECT_KEY_OR_END':
            if token == '}':
                if not self.stack or self.stack.pop() != '}':
                    return False
                self.state = self.next_after_value()
                return True
            elif self.is_string(token, partial=partial):
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
            elif self.is_value(token, partial=partial):
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
            elif self.is_value(token, partial=partial):
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

    def is_value(self, token, partial=False):
        return (
            self.is_string(token, partial=partial)
            or self.is_number(token, partial=partial)
            or token in ('true', 'false', 'null')
        )

    def is_string(self, token, partial=False):
        # Strip whitespace first
        clean_token = token.strip()
        if not clean_token.startswith('"'):
            return False
        if not partial:
            return len(clean_token) >= 2 and clean_token.endswith('"') and not clean_token.endswith('\\"')
        # In partial mode, allow strings that start with " but are not yet closed
        return True

    def is_number(self, token, partial=False):
        try:
            float(token)
            return True
        except ValueError:
            if partial:
                # Accept partial numeric patterns like '2.', '3e', '4e-'
                import re
                return re.fullmatch(r'-?\d+(\.\d*)?([eE][+-]?)?', token) is not None
            return False

    def partial_token_ok(self, token):
        return self.is_string(token, partial=True) or self.is_number(token, partial=True)

    def accepts(self, tokens, partial=True):
        self.reset()
        for i, token in enumerate(tokens):
            print(f"Processing token: {token}")
            is_last = i == len(tokens) - 1
            if not self.is_valid_token(token, partial=partial):
                if partial and is_last and self.partial_token_ok(token):
                    print(f"Accepting partial token: {token}")
                    return True
                print(f"Rejected at token: {token}")
                return False
        if partial:
            return True
        return self.state == 'END' and len(self.stack) == 0

import copy

class JsonPDA:
    """
    Push‑down automaton that validates JSON *incrementally*.
    The `consume_char` method tells you whether adding one more character keeps
    the prefix syntactically valid.
    """

    # ------------------------------------------------------------------ #
    #  Construction / cloning helpers
    # ------------------------------------------------------------------ #
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "START"
        self.stack = []            # delimiter / obligation stack
        self.buffer = ""           # for numbers / literals
        self.escape = False        # inside-string escape flag
        self.last_states = []      # (reserved for future use)

    def clone(self):
        """Deep‑copy so each beam can branch independently."""
        return copy.deepcopy(self)

    # ------------------------------------------------------------------ #
    #  Main transition function
    # ------------------------------------------------------------------ #
    def consume_char(self, char, *, partial=False):
        """
        Feed one character. Return **True** if the prefix can still form
        valid JSON; **False** if it is already impossible.

        `partial=True` allows the last character to leave the PDA in an
        unfinished but acceptable state (e.g. inside an open string).
        """

        # ---------- 1. Inside-string escape handling ----------
        if self.state == "IN_STRING":
            if self.escape:
                self.buffer += char
                self.escape = False
                return True
            if char == "\\":
                self.escape = True
                return True
            if char == '"':
                self.state = self.stack.pop()      # back to caller state
                return True
            self.buffer += char
            return True

        # ---------- 2. Skip whitespace outside strings ----------
        if char.isspace():
            return True

        # ---------- 3. Finite‑state controller ----------
        # START ----------------------------------------------------------
        if self.state == "START":
            if char == "{":
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            if char == "[":
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            return False

        # OBJECT STATES --------------------------------------------------
        if self.state == "EXPECT_KEY_OR_END":
            if char == "}":                            # empty object
                if not self.stack or self.stack.pop() != "}":
                    return False
                self.state = self._get_next_state()
                return True
            if char == '"':                            # start key
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
            # open object
            if char == "{":
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            # open array
            if char == "[":
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            # string value
            if char == '"':
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            # number / true / false / null
            if self._is_primitive_start(char):
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_PRIMITIVE"
                self.buffer = char
                return True
            return False

        # PRIMITIVE ------------------------------------------------------
        if self.state == "IN_PRIMITIVE":
            if self._is_primitive_char(char):
                self.buffer += char
                return True
            # primitive closed → validate and reprocess char
            if not self._validate_primitive():
                return False
            self.state = self.stack.pop()
            return self.consume_char(char, partial=partial)

        # ARRAY STATES ---------------------------------------------------
        if self.state == "EXPECT_VALUE_OR_END":
            if char == "]":                             # empty array / close
                if not self.stack or self.stack.pop() != "]":
                    return False
                self.state = self._get_next_state()
                return True

            # value starts here -----------------------------------------
            if char == "{":                             # object value
                self.stack.append("EXPECT_COMMA_OR_END")
                self.stack.append("}")
                self.state = "EXPECT_KEY_OR_END"
                return True
            if char == "[":                             # nested array
                self.stack.append("EXPECT_COMMA_OR_END")
                self.stack.append("]")
                self.state = "EXPECT_VALUE_OR_END"
                return True
            if char == '"':                             # string value
                self.stack.append("EXPECT_COMMA_OR_END")
                self.state = "IN_STRING"
                self.buffer = ""
                return True
            if self._is_primitive_start(char):          # primitive value
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

        # Already finished → any extra char is invalid
        if self.state == "END":
            return False

        return False  # safety fallback

    # ------------------------------------------------------------------ #
    #  Helper utilities
    # ------------------------------------------------------------------ #
    def _get_next_state(self):
        """After closing a container, decide the next controller state."""
        if not self.stack:
            return "END"
        top = self.stack[-1]
        return "EXPECT_COMMA_OR_END" if top in "}]" else "END"

    def _is_primitive_start(self, char):
        return char.isdigit() or char == "-" or char.lower() in ("t", "f", "n")

    def _is_primitive_char(self, char):
        if not self.buffer:
            return False
        first = self.buffer[0].lower()

        # numeric literal
        if first.isdigit() or first == "-":
            return (
                char.isdigit()
                or char in ".eE+-"
                or (char in "eE" and "e" not in self.buffer.lower() and "E" not in self.buffer.lower())
            )

        # true / false / null
        if first == "t":
            return len(self.buffer) < 4 and char in "true"[len(self.buffer):]
        if first == "f":
            return len(self.buffer) < 5 and char in "false"[len(self.buffer):]
        if first == "n":
            return len(self.buffer) < 4 and char in "null"[len(self.buffer):]
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

    # ------------------------------------------------------------------ #
    #  Public convenience
    # ------------------------------------------------------------------ #
    def accepts(self, text, *, partial=False):
        """Validate an entire string (or prefix if `partial=True`)."""
        self.reset()
        for idx, ch in enumerate(text):
            if not self.consume_char(ch, partial=partial):
                if partial and idx == len(text) - 1 and self._is_partial_acceptable():
                    return True
                return False
        return True if partial else (self.state == "END" and not self.stack)

    def _is_partial_acceptable(self):
        return (
            self.state in ("IN_STRING", "IN_PRIMITIVE")
            or (self.state == "EXPECT_VALUE" and self.buffer)
            or (self.state == "EXPECT_VALUE_OR_END" and self.buffer)
        )

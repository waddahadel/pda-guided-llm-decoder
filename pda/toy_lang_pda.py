# grammars/toy_lang_pda.py

class ToyLangPDA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'START'
        self.stack = []

    def is_valid_token(self, token: str) -> bool:
        """
        Very simplified PDA validator for a toy programming language.
        Focuses on parsing: let x = 5 + 3; print(x);
        """
        if self.state == 'START':
            if token == 'let':
                self.state = 'VAR_DECL'
                return True
            elif token == 'print':
                self.state = 'PRINT'
                return True
            return False

        elif self.state == 'VAR_DECL':
            if token.isidentifier():
                self.state = 'ASSIGN_EQ'
                return True
            return False

        elif self.state == 'ASSIGN_EQ':
            if token == '=':
                self.state = 'EXPR'
                return True
            return False

        elif self.state == 'EXPR':
            if token.isdigit() or token.isidentifier():
                self.state = 'EXPR_CONT'
                return True
            return False

        elif self.state == 'EXPR_CONT':
            if token in ['+', '-']:
                self.state = 'EXPR_OPR'
                return True
            elif token == ';':
                self.state = 'START'  # End of statement
                return True
            return False

        elif self.state == 'EXPR_OPR':
            if token.isdigit() or token.isidentifier():
                self.state = 'EXPR_CONT'
                return True
            return False

        elif self.state == 'PRINT':
            if token == '(':
                self.state = 'PRINT_ARG'
                return True
            return False

        elif self.state == 'PRINT_ARG':
            if token.isidentifier():
                self.state = 'PRINT_END'
                return True
            return False

        elif self.state == 'PRINT_END':
            if token == ')':
                self.state = 'PRINT_SEMI'
                return True
            return False

        elif self.state == 'PRINT_SEMI':
            if token == ';':
                self.state = 'START'
                return True
            return False

        return False

    def get_state(self):
        return self.state

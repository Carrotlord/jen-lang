class Tokenizer(object):
    def get_tokens(self, program):
        self.pos = 0
        self.length = len(program)
        self.program = program
        tokens = []
        while self.in_bounds():
            char = self.program[self.pos]
            if char.isdigit():
                tokens.append(self.read_number(char))
            elif char == '\n':
                tokens.append(Token('Newline'))
                self.pos += 1
            elif is_operator(char):
                tokens.append(Token('Operator', char))
                self.pos += 1
            elif char.isspace():
                # Ignore whitespace that isn't a newline
                self.pos += 1
            else:
                raise TokenizationError("Invalid character '{0}'".format(char))
        return tokens

    def in_bounds(self, next_pos=None):
        if next_pos is not None:
            return next_pos < self.length
        return self.pos < self.length

    def read_number(self, first_digit):
        buffer = first_digit
        self.pos += 1
        has_exponent = False
        has_dot = False
        exp_markers = 'eE'
        last = None
        while self.in_bounds():
            char = self.program[self.pos]
            if char in exp_markers:
                if has_exponent:
                    raise TokenizationError('Number already has exponent field: ' + buffer + char)
                if last == '.':
                    raise TokenizationError('Exponent marker cannot be preceded by decimal point: ' + buffer + char)
                has_exponent = True
                # Exponent notation
                if self.in_bounds(self.pos + 1):
                    next = self.program[self.pos + 1]
                    if next in '+-':
                        buffer += char + next
                        self.pos += 2
                    else:
                        buffer += char
                        self.pos += 1
                else:
                    trailing_exp_error(buffer + char)
            elif char.isdigit():
                # Ordinary digit
                buffer += char
                self.pos += 1
            elif char == '.':
                # Decimal point
                if has_dot:
                    # Assume that this might be the property access operator,
                    # e.g. 3.method() is valid syntax
                    break
                if last is not None and last in exp_markers:
                    raise TokenizationError('Decimal point cannot be preceded by exponent marker: ' + buffer + char)
                has_dot = True
                buffer += char
                self.pos += 1
            else:
                # End of number
                break
            last = char
        if buffer.endswith('.'):
            raise TokenizationError('Number cannot end with decimal point: ' + buffer)
        for exp in exp_markers:
            if buffer.endswith(exp):
                trailing_exp_error(buffer)
        try:
            num = float(buffer)
        except ValueError:
            raise TokenizationError('{0} cannot be recognized as a number'.format(buffer))
        return Token('Number', (buffer, num))

    def print_tokens(self, tokens):
        for token in tokens:
            if token.kind == 'Newline':
                print(token)
            else:
                print(token, end='')
        print()

def is_operator(char):
    return char in '+-*/%^'

def trailing_exp_error(buffer):
    raise TokenizationError('Number cannot end with exponent marker: ' + buffer)

class TokenizationError(Exception):
    def __init__(self, message):
        self.message = message

class Token(object):
    def __init__(self, kind, val=None):
        self.kind = kind
        self.value = val

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.value is None:
            return '[{0}]'.format(self.kind)
        return '[{0} {1}]'.format(self.kind, self.value)

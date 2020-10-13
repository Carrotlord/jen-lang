import tokenize

class ExprTree(object):
    def __init__(self, operator, left=None, right=None):
        self.operator = operator
        self.left = left
        self.right = right

    def format(self, indentation=0):
        leading = ' ' * indentation
        simple_left = type(self.left) is tokenize.Token
        simple_right = type(self.right) is tokenize.Token
        if simple_left and simple_right:
            return '{0}({1} {2} {3})'.format(
                leading,
                self.operator,
                format_number_token(self.left),
                format_number_token(self.right)
            )
        if simple_left:
            left_repr = leading + '  ' + format_number_token(self.left)
        else:
            left_repr = self.left.format(indentation + 2)
        if simple_right:
            right_repr = leading + '  ' + format_number_token(self.right)
        else:
            right_repr = self.right.format(indentation + 2)
        return '{0}({1}\n{2}\n{3}\n{4})'.format(leading, self.operator, left_repr, right_repr, leading)

    def is_singleton(self):
        return self.left is None and self.right is None

    def __str__(self):
        return self.format()

    def __repr__(self):
        return str(self)

class ExpressionError(Exception):
    def __init__(self, message):
        self.message = message

def is_int(n):
    return int(n) == n

def format_number(n):
    if is_int(n):
        return str(int(n))
    return str(n)

def format_number_token(token, indentation=0):
    if token.kind == 'Number':
        return (' ' * indentation) + format_number(token.value[1])
    else:
        raise ExpressionError('Token {0} is not numeric'.format(token))

precedences = {
    '^': 0,
    '*': 1, '/': 1, '%': 1,
    '+': 2, '-': 2
}
MAX_PRECEDENCE = 2

def build_tree(tokens):
    if len(tokens) == 1:
        return tokens[0]
    operator_indices = []
    for i, token in enumerate(tokens):
        if type(token) is tokenize.Token and token.kind == 'Operator':
            operator_indices.append(i)
    for i in range(MAX_PRECEDENCE + 1):
        for j in operator_indices:
            operator = tokens[j].value
            if precedences[operator] == i:
                prev = j - 1
                next = j + 1
                subtree = ExprTree(operator, tokens[prev], tokens[next])
                return build_tree(tokens[:prev] + [subtree] + tokens[next+1:])

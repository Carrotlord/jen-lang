import tokenize

class ExprTree(object):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def format(self, indentation=0):
        simple_left = self.left.is_leaf()
        simple_right = self.right.is_leaf()
        leading = ' ' * indentation
        if simple_left and simple_right:
            return '{0}({1} {2} {3})'.format(
                leading,
                self.operator,
                self.left.format(),
                self.right.format()
            )
        left_repr = self.left.format(indentation + 2)
        right_repr = self.right.format(indentation + 2)
        return '{0}({1}\n{2}\n{3}\n{4})'.format(leading, self.operator, left_repr, right_repr, leading)

    def is_leaf(self):
        return False

    def __str__(self):
        return self.format()

    def __repr__(self):
        return str(self)

class ExpressionError(Exception):
    def __init__(self, message):
        self.message = message

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

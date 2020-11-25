import error
import parser2
import tokenize2

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

    def is_register(self):
        return False

    def __str__(self):
        return self.format()

    def __repr__(self):
        return str(self)

class ExpressionError(error.JenError):
    def __init__(self, message):
        self.message = message

precedences = {
    '^': 0,
    '*': 1, '/': 1, '%': 1,
    '+': 2, '-': 2
}
MAX_PRECEDENCE = 2

def replace_trees(tokens, pairs):
    new_tokens = []
    start = 0
    for i, end in pairs:
        sub_expr = tokens[i+1 : end]
        sub_tree = build_tree(sub_expr)
        new_tokens += tokens[start : i]
        new_tokens.append(sub_tree)
        start = end + 1
    new_tokens += tokens[start:]
    return new_tokens

def build_tree(tokens):
    length = len(tokens)
    if length == 1:
        return tokens[0]
    parser2.mark_parens(tokens)
    operator_indices = []
    pairs = []
    i = 0
    while i < length:
        token = tokens[i]
        if type(token) is tokenize2.Token and token.kind == 'Brace' and type(token.value) is tuple:
            brace, end = token.value
            if brace == '(':
                pairs.append((i, end))
            i = end + 1
        else:
            i += 1
    if len(pairs) > 0:
        tokens = replace_trees(tokens, pairs)
    for i, token in enumerate(tokens):
        if type(token) is tokenize2.Token and token.kind == 'Operator':
            operator_indices.append(i)
    for i in range(MAX_PRECEDENCE + 1):
        for j in operator_indices:
            operator = tokens[j].value
            if precedences[operator] == i:
                prev = j - 1
                next = j + 1
                subtree = ExprTree(operator, tokens[prev], tokens[next])
                return build_tree(tokens[:prev] + [subtree] + tokens[next+1:])

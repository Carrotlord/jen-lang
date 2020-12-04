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

class FunctionCall(object):
    def __init__(self, func_name, args):
        if type(func_name) is tokenize2.Token and func_name.kind == 'Name':
            func_name = func_name.value
        self.name = func_name
        self.args = args

    def format(self, indentation=0):
        # TODO : use indentation when formatting function calls
        content = '({0} '.format(self.name)
        for arg in self.args:
            content += arg.format() + ' '
        content = content[:-1]
        return content + ')'

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

def has_function_call(tokens, i):
    prev = i - 1
    if prev >= 0 and prev < len(tokens):
        function_name = tokens[prev]
        typ = type(function_name)
        if typ is tokenize2.Token:
            return function_name.kind == 'Name'
        elif typ is FunctionCall:
            return True
    return False

def parse_args(args):
    parser2.mark_parens(args)
    i = 0
    start = 0
    parsed = []
    while i < len(args):
        arg = args[i]
        if is_valid_open_brace(arg):
            _, end = arg.value
            i = end + 1
        elif is_comma(arg):
            parsed.append(args[start : i])
            i += 1
            start = i
        else:
            i += 1
    parsed.append(args[start:])
    return parsed

def build_function_call(tokens, i, args):
    parsed = parse_args(args)
    function_name = tokens[i - 1]
    return FunctionCall(function_name, [build_tree(arg) for arg in parsed])

def replace_trees(tokens, pairs):
    new_tokens = []
    start = 0
    for i, end in pairs:
        sub_expr = tokens[i+1 : end]
        if has_function_call(tokens, i):
            sub_tree = build_function_call(tokens, i, sub_expr)
            new_tokens += tokens[start : i-1]
        else:
            sub_tree = build_tree(sub_expr)
            new_tokens += tokens[start : i]
        new_tokens.append(sub_tree)
        start = end + 1
    new_tokens += tokens[start:]
    return new_tokens

def is_valid_open_brace(token):
    return type(token) is tokenize2.Token and token.kind == 'Brace' and \
           type(token.value) is tuple and token.value[0] == '('

def is_comma(token):
    return type(token) is tokenize2.Token and token.kind == 'Delimiter' and \
           token.value == ','

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
        if is_valid_open_brace(token):
            _, end = token.value
            pairs.append((i, end))
            i = end + 1
        else:
            i += 1
    if len(pairs) > 0:
        tokens = replace_trees(tokens, pairs)
    if len(tokens) == 1:
        return tokens[0]
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
    raise ExpressionError('Could not construct tree')

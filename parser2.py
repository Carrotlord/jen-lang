import expr_tree
import tokenize2

def is_paren(token, brace):
    if type(token.value) is tuple:
        paren, _ = token.value
        return paren == brace
    return token.value == brace

def mark_sublist_parens(tokens, start, stop):
    """
    Mark all opening parentheses with the list index of the
    corresponding closing parenthesis.
    """
    i = start
    while i <= stop:
        token = tokens[i]
        if type(token) is tokenize2.Token and token.kind == 'Brace':
            if is_paren(token, ')'):
                return i
            elif is_paren(token, '('):
                end = mark_sublist_parens(tokens, i + 1, stop)
                if end is None:
                    raise expr_tree.ExpressionError('Found opening parenthesis without closing parenthesis')
                token.mark(end)
                i = end + 1
            else:
                i += 1
        else:
            i += 1
    return None

def mark_parens(tokens):
    final = mark_sublist_parens(tokens, 0, len(tokens) - 1)
    if final is not None:
        raise expr_tree.ExpressionError('Found closing parenthesis without opening parenthesis')

import tokenize
import expr_tree

def test_tokenizer():
    tokenizer = tokenize.Tokenizer()
    expressions = '2+3\n18 * 24\n5^3 + 21.24e+5\n8 + 16e-4\n123e99 * 135e1000'
    print(expressions)
    tokens = tokenizer.get_tokens(expressions)
    tokenizer.print_tokens(tokens)

def test_numeric_token_errors():
    tokenizer = tokenize.Tokenizer()
    expressions = ['2.+3.', '.75+.25', '2eee10 * 3...5', '3...5', '2EEe-3',
                   '5.6e', '7E', '1e+2e', '1e*2e', '2e.0', '10.E+5']
    print(expressions)
    for expr in expressions:
        try:
            tokens = tokenizer.get_tokens(expr)
            tokenizer.print_tokens(tokens)
        except tokenize.TokenizationError as e:
            print("For '{0}', caught tokenization error: {1}".format(expr, e.message))

def test_expr_tree():
    tokenizer = tokenize.Tokenizer()
    expressions = ['2.0+3.0', '0.75+0.25*2', '2e10 + 3.5 * 8 - 2', '4/1*3^5-10', '2e-3/5.6*0.01',
                   '18+5*3^2-100+2e4']
    print(expressions)
    for expr in expressions:
        print('--------')
        print(expr)
        tokens = tokenizer.get_tokens(expr)
        tokenizer.print_tokens(tokens)
        print(expr_tree.build_tree(tokens))

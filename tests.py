import tokenize

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

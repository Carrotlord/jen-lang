import tokenize

def test_tokenizer():
    tokenizer = tokenize.Tokenizer()
    expressions = '2+3\n18 * 24\n5^3 + 21.24e+5\n8 + 16e-4\n123e99 * 135e1000'
    print(expressions)
    tokens = tokenizer.get_tokens(expressions)
    tokenizer.print_tokens(tokens)

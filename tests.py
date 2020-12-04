import expr_tree
import parser2
import tokenize2
import virtual_machine

def test_tokenizer():
    tokenizer = tokenize2.Tokenizer()
    expressions = '2+3\n18 * 24\n5^3 + 21.24e+5\n8 + 16e-4\n123e99 * 135e1000'
    print(expressions)
    tokens = tokenizer.get_tokens(expressions)
    tokenizer.print_tokens(tokens)

def test_numeric_token_errors():
    tokenizer = tokenize2.Tokenizer()
    expressions = ['2.+3.', '.75+.25', '2eee10 * 3...5', '3...5', '2EEe-3',
                   '5.6e', '7E', '1e+2e', '1e*2e', '2e.0', '10.E+5']
    print(expressions)
    for expr in expressions:
        try:
            tokens = tokenizer.get_tokens(expr)
            tokenizer.print_tokens(tokens)
        except tokenize2.TokenizationError as e:
            print("For '{0}', caught tokenization error: {1}".format(expr, e.message))

def test_expressions(expressions):
    tokenizer = tokenize2.Tokenizer()
    compiler = virtual_machine.TreeCompiler()
    vm = virtual_machine.VirtualMachine()
    print(expressions)
    for expr in expressions:
        print('--------')
        print(expr)
        tokens = tokenizer.get_tokens(expr)
        tokenizer.print_tokens(tokens)
        tree = expr_tree.build_tree(tokens)
        print(tree)
        instructions, final_reg = compiler.compile(tree)
        for inst in instructions:
            print(inst)
        print(final_reg)
        vm.execute(instructions)
        value = vm.get_reg(final_reg.reg_num)
        print('{0} evaluates to {1}'.format(expr, tokenize2.format_number(value)))

def test_expr_tree():
    test_expressions([
        '2.0+3.0', '0.75+0.25*2', '2e10 + 3.5 * 8 - 2',
        '4/1*3^5-10', '2e-3/5.6*0.01', '18+5*3^2-100+2e4'
    ])

def test_parentheses():
    test_expressions([
        '(2.0+3.0)*100', '(0.75+5.25)*(2+1)', '(2e10 + 3.5) * (8 - (1+1))',
        '(4/(2*3)^5)-(10)', '2e-3/(5.6*0.01)', '(18+(5*3))^(4-(100-98))'
    ])

def test_function_calls():
    test_expressions([
        'add(2.0, 3.0)*100', 'mul(add(0.5+0.25, 5.25), add(2,1))', 'add(2e10, 3.5) * minus(8, add(1,1))',
        'minus(divide(4, pow(mul(2, 3), 5)),(10))', 'divide(2e-3, mul(5.6, 0.01))', '(18+(5*3))^minus(4, minus(100, 98))'
    ])

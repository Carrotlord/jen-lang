# Use Python 3, not Python 2
# @author Jiangcheng Oliver Chu

import sys

version_major = sys.version_info[0]
if version_major < 3:
    print('Error: please use Python 3, not Python 2')
    exit()

import expr_tree
import tests
import tokenize
import virtual_machine

def repl():
    tokenizer = tokenize.Tokenizer()
    compiler = virtual_machine.TreeCompiler()
    vm = virtual_machine.VirtualMachine()
    while True:
        line = input('Jen> ')
        if line.strip() == 'exit()':
            break
        else:
            try:
                tokens = tokenizer.get_tokens(line)
                if len(tokens) == 1:
                    value = tokens[0].extract_number()
                else:
                    tree = expr_tree.build_tree(tokens)
                    instructions, final_reg = compiler.compile(tree)
                    vm.execute(instructions)
                    value = vm.get_reg(final_reg.reg_num)
                print(tokenize.format_number(value))
            except tokenize.TokenizationError as e:
                print('Error: ' + e.message)

def main():
    args = sys.argv[1:]
    if len(args) > 0:
        first = args[0]
        if first == '--test':
            print('==== Running tests... ====')
            test_list = [
                tests.test_tokenizer,
                tests.test_numeric_token_errors,
                tests.test_expr_tree
            ]
            for i, test in enumerate(test_list):
                print('== Test #{0} =='.format(i))
                test()
    else:
        repl()

if __name__ == "__main__":
    main()

# Use Python 3, not Python 2
# @author Jiangcheng Oliver Chu

import sys

version_major = sys.version_info[0]
if version_major < 3:
    print('Error: please use Python 3, not Python 2')
    exit()

import tokenize
import tests

def repl():
    tokenizer = tokenize.Tokenizer()
    while True:
        line = input('Jen> ')
        if line.strip() == 'exit()':
            break
        else:
            try:
                tokens = tokenizer.get_tokens(line)
                tokenizer.print_tokens(tokens)
            except tokenize.TokenizationError as e:
                print('Error: ' + e.message)

def main():
    args = sys.argv[1:]
    if len(args) > 0:
        first = args[0]
        if first == '--test':
            print('==== Running tests... ====')
            tests.test_tokenizer()
    else:
        repl()

if __name__ == "__main__":
    main()

import expr_tree

class Instruction(object):
    def __init__(self, opcode, param_code, operands):
        self.opcode = opcode
        self.param_code = param_code
        self.operands = operands

    def __repr__(self):
        return str(self)

    def __str__(self):
        params = None
        for key, val in param_table.items():
            if self.param_code == val:
                params = key
                break
        return str([self.opcode, params] + self.operands)

class RegisterRef(object):
    def __init__(self, reg_num):
        self.reg_num = reg_num

    def is_leaf(self):
        return False

    def is_register(self):
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Reg[{0}]'.format(self.reg_num)

class TreeCompiler(object):
    def compile(self, tree):
        self.current_register = 0
        self.instructions = []
        final_register = self.compile_tree(tree)
        return (self.instructions, final_register)

    def allocate_register(self):
        next_register = self.current_register
        self.current_register += 1
        return RegisterRef(next_register)

    def compile_branch(self, branch):
        if branch.is_leaf():
            return (branch.extract_number(), 'I')
        elif branch.is_register():
            return (branch.reg_num, 'R')
        else:
            return (self.compile_tree(branch).reg_num, 'R')

    def compile_tree(self, tree):
        left_operand, left_param = self.compile_branch(tree.left)
        right_operand, right_param = self.compile_branch(tree.right)
        param_code = param_table[left_param + right_param]
        dest = self.allocate_register()
        self.instructions.append(
            Instruction(
                tree.operator,
                param_code,
                [dest.reg_num, left_operand, right_operand]
            )
        )
        return dest

class VirtualMachine(object):
    pass

RII = 0
RRI = 1
RIR = 2
RRR = 3

param_table = {
    'II': RII,
    'RI': RRI,
    'IR': RIR,
    'RR': RRR
}

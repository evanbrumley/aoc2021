import re
import sympy


class alu_eq(sympy.Function):
    pass


class ALU:
    VALID_INPUTS = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input = []

    def __str__(self):
        return f"w={self.w} ## x={self.x} ## y={self.y} ## z={self.z}"

    def compile(self, lines):
        commands = []
        for line in lines:
            unary_command_match = re.match(r"(?P<cmd>inp) (?P<op1>[wxyz])", line)
            binary_command_match = re.match(r"(?P<cmd>(mul|add|mod|div|eql)) (?P<op1>[wxyz]) (?P<op2>[wxyz]|(-?\d+))", line)

            if unary_command_match:
                commands.append(
                    (
                        unary_command_match.group("cmd"),
                        (unary_command_match.group("op1"),)
                    )
                )
            elif binary_command_match:
                op2 = binary_command_match.group("op2")

                if op2 not in "wxyz":
                    op2 = int(op2)

                commands.append(
                    (
                        binary_command_match.group("cmd"),
                        (
                            binary_command_match.group("op1"),
                            op2,
                        )
                    )
                )
            else:
                raise Exception("Invalid Input: %s" % line)

        return commands

    def reset(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.input = None

    def run(self, program, input):
        self.input = input
        input_idx = 0
        for idx, (command, args) in enumerate(program):
            if command == "inp":
                self.inp(args, input[input_idx])
                input_idx += 1
            elif command == "mul":
                self.mul(args)
            elif command == "add":
                self.add(args)
            elif command == "mod":
                self.mod(args)
            elif command == "div":
                self.div(args)
            elif command == "eql":
                self.eql(args)


        result = self.w, self.x, self.y, self.z
        return result

    def get(self, var):
        if var not in "wxyz":
            raise Exception("Invalid get: %s" % var)

        return getattr(self, var)

    def store(self, var, val):
        if var not in "wxyz":
            raise Exception("Invalid store: %s -> %s" % (val, var))

        setattr(self, var, val)

    def get_vals(self, args):
        val1 = self.get(args[0])

        if isinstance(args[1], str) and args[1] in "wxyz":
            val2 = self.get(args[1])
        else:
            val2 = args[1]

        return self.process_val(val1), self.process_val(val2)

    def process_val(self, val):
        if isinstance(val, sympy.core.numbers.Integer):
            return int(val)

        if isinstance(val, sympy.core.numbers.Zero):
            return 0

        return val

    def inp(self, args, val):
        self.store(args[0], val)

    def mul(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 * val2)

    def mod(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 % val2)
        return

    def add(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 + val2)

    def div(self, args):
        val1, val2 = self.get_vals(args)

        if val2 == 1:
            self.store(args[0], val1)
            return

        self.store(args[0], sympy.floor(val1 / val2))

    def eql(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], alu_eq(val1, val2))
        return


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    alu = ALU()
    program = alu.compile(lines)

    program_blocks = []
    current_block = None

    for command, args in program:
        if command == "inp":
            if current_block:
                program_blocks.append(current_block)

            current_block = []

        current_block.append((command, args))

    program_blocks.append(current_block)

    input = (
        sympy.symbols("m1"),
        sympy.symbols("m2"),
        sympy.symbols("m3"),
        sympy.symbols("m4"),
        sympy.symbols("m5"),
        sympy.symbols("m6"),
        sympy.symbols("m7"),
        sympy.symbols("m8"),
        sympy.symbols("m9"),
        sympy.symbols("m10"),
        sympy.symbols("m11"),
        sympy.symbols("m12"),
        sympy.symbols("m13"),
        sympy.symbols("m14"),
    )

    for idx, block in enumerate(program_blocks):
        alu.run(block, input[idx:])
        print(f"{idx+1}: {alu.z}")
        alu.reset()
        alu.w = sympy.symbols("w" + str(idx + 1))
        alu.x = sympy.symbols("x" + str(idx + 1))
        alu.y = sympy.symbols("y" + str(idx + 1))
        alu.z = sympy.symbols("z" + str(idx + 1))


if __name__ == "__main__":
    main()

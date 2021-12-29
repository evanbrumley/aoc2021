import math
import re


class ALU:
    VALID_INPUTS = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

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

        return self.w, self.x, self.y, self.z

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

        return val1, val2

    def inp(self, args, val):
        self.store(args[0], val)

    def mul(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 * val2)

    def mod(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 % val2)

    def add(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], val1 + val2)

    def div(self, args):
        val1, val2 = self.get_vals(args)
        self.store(args[0], math.floor(val1 / val2))

    def eql(self, args):
        val1, val2 = self.get_vals(args)

        if val1 == val2:
            self.store(args[0], 1)
        else:
            self.store(args[0], 0)


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    alu = ALU()
    program = alu.compile(lines)

    # Worked out on pen and paper using output of solution_sympy.py
    largest_input = [9, 9, 8, 9, 3, 9, 9, 9, 2, 9, 1, 9, 6, 7]
    smallest_input = [3, 4, 1, 7, 1, 9, 1, 1, 1, 8, 1, 2, 1, 1]

    alu.run(program, largest_input)
    print(alu.z)

    alu.reset()

    alu.run(program, smallest_input)
    print(alu.z)


if __name__ == "__main__":
    main()

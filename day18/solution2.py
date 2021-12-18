import json
from copy import deepcopy
import math
from termcolor import colored


class SnailfishNumber:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.parent = None
        self.set_parents()

    def __str__(self):
        return f"[{self.a},{self.b}]"

    @property
    def colored_str(self):
        return self._colored_str()

    def _colored_str(self, depth=0):
        color_mapping = {
            0: 'blue',
            1: 'cyan',
            2: 'green',
            3: 'yellow',
            4: 'red',
        }

        color = color_mapping[depth]

        response = ""
        response += colored("[", color)

        if isinstance(self.a, int):
            response += colored(str(self.a), color)
        else:
            response += self.a._colored_str(depth=depth+1)

        response += colored(",", color)

        if isinstance(self.b, int):
            response += colored(str(self.b), color)
        else:
            response += self.b._colored_str(depth=depth+1)

        response += colored("]", color)

        return response

    @classmethod
    def from_str(cls, s):
        return cls.from_list(json.loads(s))

    @classmethod
    def from_list(cls, l):
        a = l[0]
        b = l[1]

        if isinstance(a, list):
            a = cls.from_list(a)

        if isinstance(b, list):
            b = cls.from_list(b)

        return cls(a, b)

    def set_parents(self):
        if isinstance(self.a, SnailfishNumber):
            self.a.parent = self
            self.a.set_parents()

        if isinstance(self.b, SnailfishNumber):
            self.b.parent = self
            self.b.set_parents()

    def __add__(self, other):
        joined = SnailfishNumber(deepcopy(self), deepcopy(other))
        joined.reduce()
        return joined

    def reduce(self):
        changes_found = True

        while changes_found:
            changes_found = False

            while exploder := self.find_exploder():
                changes_found = True
                exploder.explode()

            if splitter := self.find_splitter():
                changes_found = True
                splitter.split()

    def find_exploder(self):
        return self._find_exploder(self.a) or self._find_exploder(self.b)

    def _find_exploder(self, n, depth=0):
        if isinstance(n, int):
            return

        if depth == 3:
            return n

        return self._find_exploder(n.a, depth=depth+1) or self._find_exploder(n.b, depth=depth+1)

    def explode(self):
        self.parent.distribute_left(self.a, self)
        self.parent.distribute_right(self.b, self)

        if self.parent.a == self:
            self.parent.a = 0

        if self.parent.b == self:
            self.parent.b = 0

    def distribute_left(self, val, origin):
        if isinstance(self.a, int):
            self.a += val
            return

        if self.a != origin:
            if origin == self.parent:
                self.a.distribute_left(val, self)
            else:
                self.a.distribute_right(val, self)
            return

        if self.parent:
            self.parent.distribute_left(val, self)

    def distribute_right(self, val, origin):
        if isinstance(self.b, int):
            self.b += val
            return

        if self.b != origin:
            if origin == self.parent:
                self.b.distribute_right(val, self)
            else:
                self.b.distribute_left(val, self)
            return

        if self.parent:
            self.parent.distribute_right(val, self)

    def find_splitter(self):
        return self._find_splitter(self)

    def _find_splitter(self, n):
        if isinstance(n, int):
            return None

        if splitter := self._find_splitter(n.a):
            return splitter

        if n.is_splitter:
            return n

        if splitter := self._find_splitter(n.b):
            return splitter

        return None

    @property
    def is_splitter(self):
        return (isinstance(self.a, int) and self.a >= 10) or (isinstance(self.b, int) and self.b >= 10)

    def split(self):
        if isinstance(self.a, int) and self.a >= 10:
            self.split_a()
            return

        if isinstance(self.b, int) and self.b >= 10:
            self.split_b()
            return

    def split_a(self):
        self.a = SnailfishNumber(
            math.floor(self.a / 2),
            math.ceil(self.a / 2)
        )
        self.set_parents()

    def split_b(self):
        self.b = SnailfishNumber(
            math.floor(self.b / 2),
            math.ceil(self.b / 2)
        )
        self.set_parents()

    @property
    def magnitude(self):
        if isinstance(self.a, int):
            magnitude = self.a * 3
        else:
            magnitude = self.a.magnitude * 3

        if isinstance(self.b, int):
            magnitude += self.b * 2
        else:
            magnitude += self.b.magnitude * 2

        return magnitude


class Assignment:
    def __init__(self, numbers):
        self.numbers = numbers

    def __str__(self):
        output = ""

        for number in self.numbers:
            output += f"{number}\n"

        return output

    @classmethod
    def from_input(cls, lines):
        numbers = []

        for line in lines:
            numbers.append(SnailfishNumber.from_str(line))

        return cls(numbers)

    def solve(self):
        max_magnitude = 0

        for i in range(len(self.numbers)):
            for j in range(len(self.numbers)):
                if i == j:
                    continue

                magnitude = (self.numbers[i] + self.numbers[j]).magnitude

                if magnitude > max_magnitude:
                    max_magnitude = magnitude

        return max_magnitude


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    a = Assignment.from_input(lines)
    print(a.solve())


if __name__ == "__main__":
    main()

import re


class Grid:
    def __init__(self, dots, folds):
        self.dots = dots
        self.folds = folds
        self.width = max([d[0] for d in dots])
        self.height = max([d[1] for d in dots])

    def __str__(self):
        output = ""
        for y in range(0, self.height+1):
            for x in range(0, self.width+1):
                if (x, y) in self.dots:
                    output += "# "
                else:
                    output += ". "
            output += "\n"

        return output

    @classmethod
    def from_input(cls, lines):
        dots = []
        folds = []
        for line in lines:
            match = re.match(r"(?P<x>\d+),(?P<y>\d+)", line)
            if not match:
                continue

            x = int(match.group("x"))
            y = int(match.group("y"))

            dots.append((x, y))

        for line in lines:
            match = re.match(r"fold along (?P<axis>[xy])=(?P<val>\d+)", line)

            if not match:
                continue

            axis = match.group("axis")
            val = int(match.group("val"))

            folds.append((axis, val))

        return cls(dots, folds)

    def fold(self):
        if not self.folds:
            raise Exception("No folds available")

        fold_axis = self.folds[0][0]
        fold_line = self.folds[0][1]

        if fold_axis == "x":
            return self.fold_x(fold_line)
        else:
            return self.fold_y(fold_line)

    def fold_x(self, fold_line):
        new_dots = []

        for dot in self.dots:
            if dot[0] < fold_line:
                if dot not in new_dots:
                    new_dots.append(dot)
            elif dot[0] > fold_line:
                new_x = 2 * fold_line - dot[0]

                if new_x < 0:
                    raise Exception("Invalid Fold")

                new_dot = (
                    new_x,
                    dot[1],
                )

                if new_dot not in new_dots:
                    new_dots.append(new_dot)

        return Grid(new_dots, self.folds[1:])

    def fold_y(self, fold_line):
        new_dots = []

        for dot in self.dots:
            if dot[1] < fold_line:
                if dot not in new_dots:
                    new_dots.append(dot)
            elif dot[1] > fold_line:
                new_y = 2 * fold_line - dot[1]

                if new_y < 0:
                    raise Exception("Invalid Fold")

                new_dot = (
                    dot[0],
                    new_y,
                )

                if new_dot not in new_dots:
                    new_dots.append(new_dot)

        return Grid(new_dots, self.folds[1:])


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    grid = Grid.from_input(lines)

    while grid.folds:
        grid = grid.fold()

    print(grid)


if __name__ == "__main__":
    main()

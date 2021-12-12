import re


class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

        if (x0 - x1):
            self.a = (y0 - y1) / (x0 - x1)
            self.b = y0 - self.a * x0
        else:
            self.a = None
            self.b = 0

    @classmethod
    def from_str(cls, line_str):
        match = re.match(r"(?P<x0>\d+),(?P<y0>\d+) -> (?P<x1>\d+),(?P<y1>\d+)", line_str)
        if not match:
            raise Exception("Invalid Input")

        return cls(
            int(match.group("x0")),
            int(match.group("y0")),
            int(match.group("x1")),
            int(match.group("y1")),
        )

    def intersects(self, x, y):
        return y == self.a * x + self.b

    def grid_intersections(self):
        possible_x_points = range(
            int(min(self.x0, self.x1)),
            int(max(self.x0, self.x1)) + 1,
        )

        if self.a is None:
            y_points = range(
                int(min(self.y0, self.y1)),
                int(max(self.y0, self.y1)) + 1,
            )
            points = [(possible_x_points[0], y) for y in y_points]
        else:
            points = [(x, self.a * x + self.b) for x in possible_x_points]
            points = [(int(x), int(y)) for (x, y) in points if not y % 1]

        return points


def main():
    with open("input", "r") as f:
        lines_raw = f.read().splitlines()

    lines = [Line.from_str(line_raw) for line_raw in lines_raw]

    points = {}

    for line in lines:
        for x, y in line.grid_intersections():
            if (x, y) not in points:
                points[(x, y)] = 0

            points[(x, y)] += 1

    intersections = 0

    for count in points.values():
        if count > 1:
            intersections += 1

    print(intersections)


if __name__ == "__main__":
    main()

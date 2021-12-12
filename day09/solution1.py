import statistics


class TubeMap:
    def __init__(self, rows):
        self.rows = rows
        self.cols = list(map(list, zip(*self.rows)))
        self.width = len(self.rows[0])
        self.height = len(self.cols[0])

    @classmethod
    def from_raw_lines(cls, lines):
        rows = []

        for line in lines:
            if line.strip():
                rows.append([int(c) for c in line])

        return cls(rows)

    @property
    def minima(self):
        minima = []

        for y in range(self.height):
            for x in range(self.width):
                val = self.rows[y][x]

                if x == 0:
                    is_x_minima = val < self.rows[y][x+1]
                elif x == self.width - 1:
                    is_x_minima = val < self.rows[y][x-1]
                else:
                    is_x_minima = self.rows[y][x-1] > val < self.rows[y][x+1]

                if y == 0:
                    is_y_minima = val < self.rows[y+1][x]
                elif y == self.height - 1:
                    is_y_minima = val < self.rows[y-1][x]
                else:
                    is_y_minima = self.rows[y+1][x] > val < self.rows[y-1][x]

                if is_x_minima and is_y_minima:
                    minima.append((x, y, val))

        return minima

    @property
    def total_risk_factor(self):
        total = 0

        for x, y, val in self.minima:
            total += (1 + val)

        return total


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    tube_map = TubeMap.from_raw_lines(lines)

    print(tube_map.width, tube_map.height)
    print(tube_map.minima)
    print(tube_map.total_risk_factor)



if __name__ == "__main__":
    main()

class Image:
    def __init__(self, algorithm, rows):
        self.algorithm = algorithm
        self.set_rows(rows)
        self.universe_cell = "0"

    def __str__(self):
        output = ""

        for row in self.rows:
            output += "".join([c for c in row])
            output += "\n"

        return output

    def set_rows(self, rows):
        self.rows = rows
        self.cols = list(map(list, zip(*self.rows)))
        self.width = len(self.rows[0])
        self.height = len(self.cols[0])

    @classmethod
    def from_input(cls, lines):
        algorithm = lines[0].strip()
        rows = []

        for line in lines[2:]:
            rows.append(list(line.strip()))

        return cls(algorithm, rows)

    def refine(self):
        output_rows = []

        for y in range(-1, self.height + 1):
            output_row = []
            for x in range(-1, self.width + 1):
                output_row.append(self.refine_cell((x, y)))

            output_rows.append(output_row)

        self.universe_cell = self.refine_cell((self.width + 10, self.height + 10))
        self.set_rows(output_rows)

    def refine_cell(self, cell):
        binstring = ""
        for y in range(cell[1] - 1, cell[1] + 2):
            for x in range(cell[0] - 1, cell[0] + 2):
                binstring += self.get_cell_binval(x, y)

        val = int(binstring, 2)
        return self.algorithm[val]

    def get_cell_binval(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            val = self.universe_cell
        else:
            val = self.rows[y][x]

        if val == "#":
            return "1"
        else:
            return "0"

    @property
    def num_lit_pixels(self):
        count = 0

        for row in self.rows:
            for c in row:
                if c == "#":
                    count += 1

        return count


def main():
    with open("input", "r") as f:
        lines = f.read().strip().splitlines()

    img = Image.from_input(lines)

    for idx in range(50):
        print(idx)
        img.refine()

    print(img.num_lit_pixels)


if __name__ == "__main__":
    main()

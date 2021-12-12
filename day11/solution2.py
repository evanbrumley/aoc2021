class OctoGrid:
    FLASH = "F"

    def __init__(self, rows):
        self.rows = rows
        self.cols = list(map(list, zip(*self.rows)))
        self.width = len(self.rows[0])
        self.height = len(self.cols[0])
        self.flashes = []
        self.total_flashes = 0
        self.ticks = 0

    def __str__(self):
        output = ""
        for row in self.rows:
            output = output + "".join([str(i) for i in row]) + "\n"

        return output

    @classmethod
    def from_raw_lines(cls, lines):
        rows = []

        for line in lines:
            if line.strip():
                rows.append([int(c) for c in line])

        return cls(rows)

    def tick(self):
        self.ticks += 1
        tick_flashes = 0

        for x in range(self.width):
            for y in range(self.height):
                self.powerup(x, y)

        while self.flashes:
            tick_flashes += 1
            self.apply_flash(self.flashes.pop(0))

        for x in range(self.width):
            for y in range(self.height):
                if self.rows[y][x] == self.FLASH:
                    self.rows[y][x] = 0

        return tick_flashes

    def fast_forward(self, num_ticks):
        for _ in range(num_ticks):
            self.tick()

    def fast_forward_until_sync(self):
        found_sync = 0
        while not found_sync:
            num_flashes = self.tick()
            found_sync = num_flashes == self.width * self.height

    def powerup(self, x, y):
        if self.rows[y][x] == self.FLASH:
            return

        if self.rows[y][x] == 9:
            self.rows[y][x] = self.FLASH
            self.flashes.append((x, y))
            return

        self.rows[y][x] += 1

    def apply_flash(self, flash):
        self.total_flashes += 1

        min_x = max(flash[0] - 1, 0)
        max_x = min(flash[0] + 2, self.width)
        min_y = max(flash[1] - 1, 0)
        max_y = min(flash[1] + 2, self.height)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                self.powerup(x, y)


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    grid = OctoGrid.from_raw_lines(lines)

    grid.fast_forward_until_sync()
    print(grid.ticks)



if __name__ == "__main__":
    main()

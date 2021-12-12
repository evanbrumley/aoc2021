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
    def basins(self):
        basins = []
        points_seen = {}
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in points_seen or self.rows[y][x] == 9:
                    continue

                basin = self.fill_basin(x, y)
                basins.append(basin)

                for point in basin:
                    points_seen[point] = True

        return basins

    def fill_basin(self, x, y):
        result = []
        seen = {}
        q = []
        q.append((x, y))

        while q:
            n = q.pop(0)

            if n in seen:
                continue

            seen[n] = True

            val = self.rows[n[1]][n[0]]

            if n[0] >= 0 and n[1] >= 0 and val not in (None, 9):
                result.append(n)

                adjacent_nodes = (
                    (n[0] - 1, n[1]),
                    (n[0] + 1, n[1]),
                    (n[0], n[1] - 1),
                    (n[0], n[1] + 1),
                )

                for a in adjacent_nodes:
                    if a not in seen and a[0] >= 0 and a[1] >= 0 and a[0] < self.width and a[1] < self.height:
                        q.append(a)

        return result


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    tube_map = TubeMap.from_raw_lines(lines)

    sorted_basins = sorted(tube_map.basins, key=lambda b: -len(b))
    print(len(sorted_basins[0]) * len(sorted_basins[1]) * len(sorted_basins[2]))



if __name__ == "__main__":
    main()

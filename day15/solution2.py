class Cave:
    def __init__(self, rows):
        self.rows = []
        for i in range(5):
            for row in rows:
                new_row = []
                for j in range(5):
                    for val in row:
                        new_val = ((val -1 + j + i) % 9) + 1
                        new_row.append(new_val)
                self.rows.append(new_row)

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

    def search(self):
        q = {}
        dist = {}
        prev = {}

        for y, row in enumerate(self.rows):
            for x, cost in enumerate(row):
                q[(x, y)] = True
                dist[(x, y)] = 999999999999999999999
                prev[(x, y)] = None

        dist[(0, 0)] = 0

        while q:
            print(len(q))

            u = None
            min_dist = None

            for k in q.keys():
                if min_dist is None or dist[k] < min_dist:
                    min_dist = dist[k]
                    u = k

            del q[u]

            neighbours = (
                (u[0] - 1, u[1]),
                (u[0] + 1, u[1]),
                (u[0], u[1] - 1),
                (u[0], u[1] + 1),
            )

            valid_neighbours = []

            for n in neighbours:
                if n not in q:
                    continue

                if not (0 <= n[0] < self.width):
                    continue

                if not (0 <= n[1] < self.height):
                    continue

                valid_neighbours.append(n)

            for v in valid_neighbours:
                alt = dist[u] + self.rows[v[1]][v[0]]
                if alt <= dist[v]:
                    dist[v] = alt
                    prev[v] = u

        return dist, prev


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    cave = Cave.from_raw_lines(lines)

    dist, prev = cave.search()
    print(dist[(499, 499)])


if __name__ == "__main__":
    main()

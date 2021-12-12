class CrabNavy:
    def __init__(self, positions):
        self.positions = positions

    @classmethod
    def from_str(cls, positions_str):
        positions = [int(c) for c in positions_str.split(",")]

        return cls(positions)

    def calculate_consumption(self, alignment):
        total = 0

        for position in self.positions:
            total += abs(alignment - position)

        return total

    @property
    def ideal_alignment(self):
        min_consumption = None
        min_idx = None

        for idx in range(min(self.positions), max(self.positions)):
            consumption = self.calculate_consumption(idx)

            if min_consumption is None or consumption < min_consumption:
                min_consumption = consumption
                min_idx = idx

        return min_idx

    @property
    def ideal_alignment_consumption(self):
        return self.calculate_consumption(self.ideal_alignment)


def main():
    with open("input", "r") as f:
        lines_raw = f.read().splitlines()

    sample_navy = CrabNavy([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
    navy = CrabNavy.from_str(lines_raw[0])
    print(sample_navy.ideal_alignment)
    print(sample_navy.ideal_alignment_consumption)
    print(navy.ideal_alignment_consumption)


if __name__ == "__main__":
    main()

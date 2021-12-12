class FishPopulation:
    breeding_cycle_days = 7
    childhood_length = 2

    def __init__(self, counts):
        self.counts = counts

    @classmethod
    def from_str(cls, fishies_str):
        fishies = [int(c) for c in fishies_str.split(",")]
        counts = [0] * (cls.breeding_cycle_days + cls.childhood_length)

        for fish in fishies:
            counts[fish] += 1

        return cls(counts)

    def tick(self):
        new_counts = [0] * (self.breeding_cycle_days + self.childhood_length)

        for idx in range(self.breeding_cycle_days + self.childhood_length - 1):
            new_counts[idx] = self.counts[idx+1]

        new_counts[self.breeding_cycle_days - 1] += self.counts[0]
        new_counts[self.breeding_cycle_days + self.childhood_length - 1] += self.counts[0]

        self.counts = new_counts

    def fast_forward(self, num_ticks):
        for _ in range(num_ticks):
            self.tick()

    @property
    def total(self):
        return sum(self.counts)


def main():
    with open("input", "r") as f:
        fishies = f.readline()

    fishpop = FishPopulation.from_str(fishies)
    fishpop.fast_forward(256)
    print(fishpop.total)


if __name__ == "__main__":
    main()

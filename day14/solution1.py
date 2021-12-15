from collections import defaultdict
import re


class Polymerizer:
    def __init__(self, template, rules):
        self.template = template
        self.rules = rules
        self.polymer = template

    def __str__(self):
        return self.polymer

    @classmethod
    def from_input(cls, lines):
        rules = []

        template = lines[0].strip()
        for line in lines[2:]:
            match = re.match(r"(?P<x>..) -> (?P<y>.)", line)
            if not match:
                raise Exception("Invalid Input: %s" % line)

            x = match.group("x")
            y = match.group("y")

            rules.append((x, y))

        return cls(template, rules)

    def tick(self):
        result = []
        for idx, c1 in enumerate(self.polymer):
            result.append(c1)

            try:
                c2 = self.polymer[idx+1]
            except IndexError:
                continue

            for pattern, insert in self.rules:
                if c1 + c2 == pattern:
                    result.append(insert)
                    break

        self.polymer = "".join(result)

    def fast_forward(self, num_ticks):
        for _ in range(num_ticks):
            self.tick()

    @property
    def counts(self):
        counts = defaultdict(int)

        for c in self.polymer:
            counts[c] += 1

        return counts

    @property
    def num_most_common(self):
        result = 0
        for _, count in self.counts.items():
            if count > result:
                result = count

        return result

    @property
    def num_least_common(self):
        result = None
        for _, count in self.counts.items():
            if result is None or count < result:
                result = count

        return result


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    polymerizer = Polymerizer.from_input(lines)
    polymerizer.fast_forward(10)
    print(polymerizer.num_most_common)
    print(polymerizer.num_least_common)
    print(polymerizer.num_most_common - polymerizer.num_least_common)


if __name__ == "__main__":
    main()

import re


class Polymerizer:
    def __init__(self, template, rules):
        self.template = template
        self.rules = rules

        self.pairs = self.generate_pairs()
        self.chars = self.generate_chars()

    def __str__(self):
        return self.template

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

    def generate_pairs(self):
        pairs = {}

        for idx, c1 in enumerate(self.template[:-1]):
            c2 = self.template[idx + 1]
            pair = c1 + c2
            print(pair)

            if pair not in pairs:
                pairs[pair] = 1
            else:
                pairs[pair] += 1

        return pairs

    def generate_chars(self):
        chars = {}

        for c in self.template:
            if c not in chars:
                chars[c] = 1
            else:
                chars[c] += 1

        return chars

    def tick(self):
        new_pairs = {}

        for pattern, insert in self.rules:
            new_pair_1 = pattern[0] + insert
            new_pair_2 = insert + pattern[1]
            num_matches = self.pairs.get(pattern, 0)

            if new_pair_1 not in new_pairs:
                new_pairs[new_pair_1] = num_matches
            else:
                new_pairs[new_pair_1] += num_matches

            if new_pair_2 not in new_pairs:
                new_pairs[new_pair_2] = num_matches
            else:
                new_pairs[new_pair_2] += num_matches

            if insert not in self.chars:
                self.chars[insert] = num_matches
            else:
                self.chars[insert] += num_matches

        self.pairs = new_pairs

    def fast_forward(self, num_ticks):
        for _ in range(num_ticks):
            self.tick()

    @property
    def num_most_common(self):
        result = 0
        for _, count in self.chars.items():
            if count > result:
                result = count

        return result

    @property
    def num_least_common(self):
        result = None
        for _, count in self.chars.items():
            if result is None or count < result:
                result = count

        return result


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    polymerizer = Polymerizer.from_input(lines)

    polymerizer.fast_forward(40)
    print("--------")
    print(polymerizer.num_most_common)
    print(polymerizer.num_least_common)
    print(polymerizer.num_most_common - polymerizer.num_least_common)


if __name__ == "__main__":
    main()

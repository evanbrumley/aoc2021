from collections import defaultdict
import re


def sort_string(string):
    return "".join(sorted(string))


class Display:
    def __init__(self, combinations, message_encrypted):
        self.combinations = [sort_string(c) for c in combinations]
        self.message_encrypted = [sort_string(c) for c in message_encrypted]
        self.message = self.decode(self.message_encrypted)

    @classmethod
    def from_str(cls, input_str):
        match = re.match(r"(?P<combinations>[abcdefg ]+) \| (?P<outputs>[abcdefg ]+)", input_str)
        if not match:
            raise Exception("Invalid Input")

        return cls(
            match.group("combinations").split(),
            match.group("outputs").split()
        )

    def find_zero(self, six, nine):
        for combo in self.combinations:
            if len(combo) == 6 and combo != six and combo != nine:
                return combo

        raise Exception("Incomplete Combinations (couldn't find zero)")

    def find_one(self):
        for combo in self.combinations:
            if len(combo) == 2:
                return combo

        raise Exception("Incomplete Combinations (couldn't find one)")

    def find_two(self, three, five):
        for combo in self.combinations:
            if len(combo) == 5 and combo != three and combo != five:
                return combo

        raise Exception("Incomplete Combinations (couldn't find two)")

    def find_three(self, one):
        for combo in self.combinations:
            if len(combo) == 5 and len(set(one + combo)) == 5:
                return combo

        raise Exception("Incomplete Combinations (couldn't find nine)")

    def find_four(self):
        for combo in self.combinations:
            if len(combo) == 4:
                return combo

        raise Exception("Incomplete Combinations (couldn't find four)")

    def find_five(self, six):
        for combo in self.combinations:
            if len(combo) == 5 and len(set(six + combo)) != 7:
                return combo

        raise Exception("Incomplete Combinations (couldn't find five)")

    def find_six(self, one):
        for combo in self.combinations:
            if len(combo) == 6 and (one[0] not in combo or one[1] not in combo):
                return combo

        raise Exception("Incomplete Combinations (couldn't find six)")

    def find_seven(self):
        for combo in self.combinations:
            if len(combo) == 3:
                return combo

        raise Exception("Incomplete Combinations (couldn't find seven)")

    def find_eight(self):
        for combo in self.combinations:
            if len(combo) == 7:
                return combo

        raise Exception("Incomplete Combinations (couldn't find eight)")

    def find_nine(self, four):
        for combo in self.combinations:
            if len(combo) == 6 and len(set(four + combo)) == 6:
                return combo

        raise Exception("Incomplete Combinations (couldn't find nine)")

    def decode(self, message):
        one = self.find_one()
        three = self.find_three(one)
        four = self.find_four()
        six = self.find_six(one)
        five = self.find_five(six)
        seven = self.find_seven()
        eight = self.find_eight()
        nine = self.find_nine(four)
        zero = self.find_zero(six, nine)
        two = self.find_two(three, five)

        decoder = {
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
            six: 6,
            seven: 7,
            eight: 8,
            nine: 9,
            zero: 0,
        }

        return [decoder[x] for x in message]


def main():
    with open("input", "r") as f:
        lines_raw = f.read().splitlines()

    displays = [Display.from_str(line_raw) for line_raw in lines_raw]

    counts = defaultdict(int)

    for display in displays:
        for num in display.message:
            counts[num] += 1

    print(counts[1] + counts[4] + counts[7] + counts[8])

if __name__ == "__main__":
    main()

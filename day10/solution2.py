import statistics

class Line:
    CHUNK_MARKERS = (
        ("(", ")", 3, 1),
        ("[", "]", 57, 2),
        ("{", "}", 1197, 3),
        ("<", ">", 25137, 4),
    )

    def __init__(self, line_str):
        self.line_str = line_str

        self.is_corrupted = False
        self.is_incomplete = False
        self.first_corrupted_char = None
        self.completion_str = ""
        self.parse()

    def __str__(self):
        if self.is_corrupted:
            return f"{self.line_str} - CORRUPT - {self.first_corrupted_char}"

        if self.is_incomplete:
            return f"{self.line_str} - INCOMPLETE"

        return f"{self.line_str} - OK"

    def parse(self):
        starting_markers = [m[0] for m in self.CHUNK_MARKERS]
        start_to_end = {m[0]: m[1] for m in self.CHUNK_MARKERS}

        stack = []

        for c in self.line_str:
            if c in starting_markers:
                stack.append(c)
                continue

            if not stack:
                self.is_corrupted = True
                self.first_corrupted_char = c
                return

            expected_start = stack.pop()

            if c != start_to_end[expected_start]:
                self.is_corrupted = True
                self.first_corrupted_char = c
                return

        if stack:
            self.is_incomplete = True
            self.completion_str = ""

            while stack:
                self.completion_str += start_to_end[stack.pop()]

    @property
    def corruption_score(self):
        scores = {m[1]: m[2] for m in self.CHUNK_MARKERS}
        return scores.get(self.first_corrupted_char, 0)

    @property
    def completion_score(self):
        character_scores = {m[1]: m[3] for m in self.CHUNK_MARKERS}
        score = 0

        for c in self.completion_str:
            character_score = character_scores[c]
            score = score * 5
            score = score + character_score

        return score


def main():
    with open("input", "r") as f:
        lines = [Line(line_str) for line_str in f.read().splitlines() if line_str]

    scores = [l.completion_score for l in lines if l.is_incomplete]
    print(len(scores))
    print(statistics.median(scores))



if __name__ == "__main__":
    main()

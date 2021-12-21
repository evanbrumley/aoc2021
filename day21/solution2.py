from collections import defaultdict


SCORE_LIMIT = 21
NUM_SQUARES = 10
UNIVERSES_PER_ROLL = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]


class Game:
    def __init__(self, p1_start, p2_start):
        self.p1_start = p1_start
        self.p2_start = p2_start

        self.state = self.generate_empty_state()
        self.state[0][0][p1_start-1][p2_start-1] = 1

    def __str__(self):
        return str(self.state)

    def generate_empty_state(self):
        return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

    def iter_state(self):
        for p1_score in range(SCORE_LIMIT):
            for p2_score in range(SCORE_LIMIT):
                for p1_square in range(NUM_SQUARES):
                    for p2_square in range(NUM_SQUARES):
                        yield (p1_score, p2_score, p1_square, p2_square)

    def p1_turn(self):
        new_state = self.generate_empty_state()
        wins = 0

        for roll, universe_multiplier in enumerate(UNIVERSES_PER_ROLL):
            for p1_score, p2_score, p1_square, p2_square in self.iter_state():
                new_square = (p1_square + roll) % 10
                new_score = (p1_score + new_square + 1)
                incoming_universes = self.state[p1_score][p2_score][p1_square][p2_square]
                new_universes = incoming_universes * universe_multiplier

                if new_score >= SCORE_LIMIT:
                    wins += new_universes
                else:
                    new_state[new_score][p2_score][new_square][p2_square] += new_universes

        self.state = new_state
        return wins

    def p2_turn(self):
        new_state = self.generate_empty_state()
        wins = 0

        for roll, universe_multiplier in enumerate(UNIVERSES_PER_ROLL):
            for p1_score, p2_score, p1_square, p2_square in self.iter_state():
                new_square = (p2_square + roll) % 10
                new_score = (p2_score + new_square + 1)
                incoming_universes = self.state[p1_score][p2_score][p1_square][p2_square]
                new_universes = incoming_universes * universe_multiplier

                if new_score >= SCORE_LIMIT:
                    wins += new_universes
                else:
                    new_state[p1_score][new_score][p1_square][new_square] += new_universes

        self.state = new_state
        return wins

    @classmethod
    def from_input(cls, lines):
        p1_start = int(lines[0][-1])
        p2_start = int(lines[1][-1])

        return cls(p1_start, p2_start)

    def play(self):
        p1_total_wins = 0
        p2_total_wins = 0
        current_turn = 0

        while self.still_playing:
            current_turn += 1
            p1_wins = self.p1_turn()
            p2_wins = self.p2_turn()

            p1_total_wins += p1_wins
            p2_total_wins += p2_wins

            print(f"After Turn #{current_turn}: P1={p1_total_wins} P2={p2_total_wins}")

    @property
    def still_playing(self):
        count = 0
        for v1 in self.state.values():
            for v2 in v1.values():
                for v3 in v2.values():
                    for universes in v3.values():
                        count += 1
                        if universes:
                            return True

        return False


def main():
    with open("example", "r") as f:
        lines = f.read().splitlines()

    game = Game.from_input(lines)
    game.play()


if __name__ == "__main__":
    main()

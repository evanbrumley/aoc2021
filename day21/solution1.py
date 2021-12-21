class Die:
    def roll(self):
        raise NotImplementedError


class DeterministicDie(Die):
    def __init__(self):
        self.next_roll = 1
        self.times_rolled = 0

    def roll(self):
        roll = self.next_roll
        self.next_roll = self.next_roll + 1

        if self.next_roll > 100:
            self.next_roll = 1

        self.times_rolled += 1
        return roll


class Player:
    def __init__(self, player_id, starting_position):
        self.player_id = player_id
        self.current_position = starting_position
        self.score = 0

    def __str__(self):
        return f"Player #{self.player_id} - POS:{self.current_position} - SCORE:{self.score}"

    def take_turn(self, die):
        result = 0

        for _ in range(3):
            result += die.roll()

        self.current_position = (self.current_position + result - 1) % 10 + 1
        self.score += self.current_position

    @property
    def is_winner(self):
        return self.score >= 1000


class Game:
    def __init__(self, p1_start, p2_start):
        self.die = DeterministicDie()
        self.players = (
            Player(1, p1_start),
            Player(2, p2_start),
        )
        self.winner = None
        self.losers = None
        self.turns_played = 0

    def __str__(self):
        output = ""
        for player in self.players:
            output += f"{player}\n"

        return output

    @classmethod
    def from_input(cls, lines):
        p1_start = int(lines[0][-1])
        p2_start = int(lines[1][-1])

        return cls(p1_start, p2_start)

    def play(self):
        current_player_idx = 0

        while True:
            self.turns_played += 1
            player = self.players[current_player_idx]
            player.take_turn(self.die)

            if player.is_winner:
                self.winner = player
                self.losers = [p for p in self.players if p != player]
                return

            current_player_idx = (current_player_idx + 1) % len(self.players)


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    game = Game.from_input(lines)

    game.play()
    print(game)

    print(game.losers[0].score)
    print(game.die.times_rolled)
    print(game.losers[0].score * game.die.times_rolled)


if __name__ == "__main__":
    main()

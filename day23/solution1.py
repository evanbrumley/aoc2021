from copy import copy
import heapq


class Burrow:
    COSTS = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }
    NETWORK = (
        ("a", "b", 1),
        ("b", "c", 2),
        ("c", "d", 2),
        ("d", "e", 2),
        ("e", "f", 2),
        ("f", "g", 1),
        ("b", "h", 2),
        ("h", "c", 2),
        ("c", "i", 2),
        ("i", "d", 2),
        ("d", "j", 2),
        ("j", "e", 2),
        ("e", "k", 2),
        ("k", "f", 2),
        ("f", "g", 1),
        ("h", "l", 1),
        ("i", "m", 1),
        ("j", "n", 1),
        ("k", "o", 1),
    )

    BASE_MOVES = (
        ("abh", 3),
        ("abhl", 4),
        ("abci", 5),
        ("abcim", 6),
        ("abcdj", 7),
        ("abcdjn", 8),
        ("abcdek", 9),
        ("abcdeko", 10),
        ("bh", 2),
        ("bhl", 3),
        ("bci", 4),
        ("bcim", 5),
        ("bcdj", 6),
        ("bcdjn", 7),
        ("bcdek", 8),
        ("bcdeko", 9),
        ("ch", 2),
        ("chl", 3),
        ("ci", 2),
        ("cim", 3),
        ("cdj", 4),
        ("cdjn", 5),
        ("cdek", 6),
        ("cdeko", 7),
        ("dch", 4),
        ("dchl", 5),
        ("di", 2),
        ("dim", 3),
        ("dj", 2),
        ("djn", 3),
        ("dek", 4),
        ("deko", 5),
        ("edch", 6),
        ("edchl", 7),
        ("edi", 4),
        ("edim", 5),
        ("ej", 2),
        ("ejn", 3),
        ("ek", 2),
        ("eko", 3),
        ("fedch", 8),
        ("fedchl", 9),
        ("fedi", 6),
        ("fedim", 7),
        ("fej", 4),
        ("fejn", 5),
        ("fk", 2),
        ("fko", 3),
        ("gfedch", 9),
        ("gfedchl", 10),
        ("gfedi", 7),
        ("gfedim", 8),
        ("gfej", 5),
        ("gfejn", 6),
        ("gfk", 3),
        ("gfko", 4),
    )

    MOVES = BASE_MOVES + tuple([(m[::-1], cost) for (m, cost) in BASE_MOVES])

    HALLWAY_LOCATIONS = "abcdefg"
    BURROWS = {
        "A": "hl",
        "B": "im",
        "C": "jn",
        "D": "ko",
    }

    BURROW_ENDS = {
        "A": "l",
        "B": "m",
        "C": "n",
        "D": "o",
    }

    def __init__(self, positions):
        self.initial_state = self.setup_state(positions)

    def setup_state(self, positions):
        state = {
            "a": positions.get("a"),
            "b": positions.get("b"),
            "c": positions.get("c"),
            "d": positions.get("d"),
            "e": positions.get("e"),
            "f": positions.get("f"),
            "g": positions.get("g"),
            "h": positions.get("h"),
            "i": positions.get("i"),
            "j": positions.get("j"),
            "k": positions.get("k"),
            "l": positions.get("l"),
            "m": positions.get("m"),
            "n": positions.get("n"),
            "o": positions.get("o"),
        }

        return state

    def is_complete(self, state):
        return all((
            state["h"] == "A",
            state["l"] == "A",
            state["i"] == "B",
            state["m"] == "B",
            state["j"] == "C",
            state["n"] == "C",
            state["k"] == "D",
            state["o"] == "D",
        ))

    def repr_state(self, state):
        s = ""
        for key in state:
            val = state.get(key) or "."
            s = s + (f"{key}{val}")

        return s

    def find_best_solution(self):
        self._state_cache = {}
        self._current_min = None
        return self._find_best_solution(self.initial_state)

    def _find_best_solution(self, state):
        h = []
        state_counter = 0
        heapq.heappush(h, (0, state_counter, self.initial_state))

        while h:
            score, _, state = heapq.heappop(h)
            print(score, len(self._state_cache), state_counter)
            possible_moves = self.find_possible_moves(state)

            state_repr = self.repr_state(state)

            if state_repr in self._state_cache and self._state_cache[state_repr] < score:
                continue

            for move, cost_multiplier in possible_moves:
                move_cost = self.COSTS[state[move[0]]] * cost_multiplier
                new_state = self.apply_move(move, state)
                new_score = score + move_cost

                if self.is_complete(new_state):
                    return new_score

                state_repr = self.repr_state(new_state)

                if state_repr not in self._state_cache or self._state_cache[state_repr] > new_score:
                    state_counter += 1
                    self._state_cache[state_repr] = new_score
                    heapq.heappush(h, (new_score, state_counter, new_state))

    def find_possible_moves(self, state):
        moves = []
        for (move, cost_multiplier) in self.MOVES:
            if self.is_valid_move(move, state):
                moves.append((move, cost_multiplier))

        return moves

    def is_valid_move(self, move, state):
        start = move[0]
        end = move[-1]

        if len(move) > 2:
            interstitials = move[1:-1]
        else:
            interstitials = ""

        # No amphipods at this location
        if not state[start]:
            return False

        # Target location is occupied
        if state[end]:
            return False

        # Interstitial is occupied
        for interstitial in interstitials:
            if state[interstitial]:
                return False

        mover_type = state[start]
        mover_burrow = self.BURROWS[mover_type]
        mover_burrow_end = self.BURROW_ENDS[mover_type]

        # If in hallway, can only move to own burrow
        if start in self.HALLWAY_LOCATIONS and end not in mover_burrow:
            return False

        # Cannot move to own burrow if other type is present
        if end in mover_burrow:
            for burrow_node in mover_burrow:
                if state.get(burrow_node) is not None and state[burrow_node] != mover_type:
                    return False

        # Never move from the back of our own burrow
        if start == mover_burrow_end:
            return False

        # Never move out of a full burrow
        if start in mover_burrow and state[mover_burrow_end] == mover_type:
            return False

        return True

    def apply_move(self, move, state):
        state = copy(state)
        state[move[-1]] = state[move[0]]
        state[move[0]] = None
        return state


def main():
    test = {
        "b": "A",
        "l": "A",
        "i": "B",
        "m": "B",
        "j": "C",
        "n": "C",
        "k": "D",
        "o": "D",
    }

    example = {
        "h": "B",
        "l": "A",
        "i": "C",
        "m": "D",
        "j": "B",
        "n": "C",
        "k": "D",
        "o": "A",
    }

    input = {
        "h": "B",
        "l": "D",
        "i": "A",
        "m": "C",
        "j": "A",
        "n": "B",
        "k": "D",
        "o": "C",
    }

    burrow = Burrow(input)

    print(burrow.find_best_solution())


if __name__ == "__main__":
    main()

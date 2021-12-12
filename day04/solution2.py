class BingoBoard:
    def __init__(self, values):
        self.rows = []
        self.height = len(values)
        self.width = len(values[0])
        self.history = []

        for y, row in enumerate(values):
            self.rows.append([BingoCell(v) for v in row])

    @property
    def columns(self):
        return list(map(list, zip(*self.rows)))

    def register_value(self, value):
        for row in self.rows:
            for cell in row:
                cell.register_value(value)

        self.history.append(value)

    @property
    def is_complete(self):
        for row in self.rows:
            if all([cell.filled for cell in row]):
                return True

        for column in self.columns:
            if all([cell.filled for cell in column]):
                return True

        return False

    @property
    def score(self):
        unmarked_total = 0

        for row in self.rows:
            for cell in row:
                if not cell.filled:
                    unmarked_total = unmarked_total + cell.value

        return unmarked_total * self.history[-1]


class BingoCell:
    def __init__(self, value):
        self.value = value
        self.filled = False

    def register_value(self, value):
        if value == self.value:
            self.filled = True


def run_game(boards, numbers):
    completed_boards = []

    for number in numbers:
        for board in boards:
            if board in completed_boards:
                continue

            board.register_value(number)
            if board.is_complete:
                completed_boards.append(board)

    return completed_boards


def main():
    with open("input", "r") as f:
        numbers_raw = f.readline()
        boards_raw = f.read()

    numbers = [int(n) for n in numbers_raw.split(",")]

    boards_raw_lines = boards_raw.splitlines()
    boards_raw_lines.pop()
    boards = []

    while boards_raw_lines:
        rows = []
        while line := boards_raw_lines.pop():
            row = [int(n) for n in line.split(" ") if n.strip()]
            rows.append(row)

        boards.append(BingoBoard(rows))

    completed_boards = run_game(boards, numbers)
    print(completed_boards[-1].score)



if __name__ == "__main__":
    main()

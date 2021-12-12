import statistics


class DiagnosticReport:
    def __init__(self, report_content):
        self.report_content = report_content
        self.rows = self.parse_report_content()
        self.cols = list(map(list, zip(*self.rows)))
        self.width = len(self.rows[0])
        self.height = len(self.cols[0])

    def parse_report_content(self):
        rows = []
        lines = [l.strip() for l in self.report_content.splitlines()]

        for line in lines:
            rows.append([int(c) for c in line])

        return rows

    def rows_to_columns(self, rows):
        return list(map(list, zip(*rows)))

    def most_common(self, column, tiebreaker=1):
        ones = 0
        zeroes = 0

        for val in column:
            if val == 0:
                zeroes += 1
            else:
                ones += 1

        if zeroes == ones:
            return tiebreaker

        if zeroes > ones:
            return 0

        return 1

    def filter_rows_by_most_common(self, rows, filter_pos, invert=False):
        cols = self.rows_to_columns(rows)

        filter_val = self.most_common(cols[filter_pos])

        if invert:
            mapping = {0: 1, 1: 0}
            filter_val = mapping[filter_val]

        return [row for row in rows if row[filter_pos] == filter_val]

    @property
    def oxygen_consumption(self):
        rows = self.rows

        for idx in range(self.width):
            rows = self.filter_rows_by_most_common(rows, idx)

        return int(''.join(map(str, rows[0])), 2)

    @property
    def co2_scrubber_rating(self):
        rows = self.rows

        for idx in range(self.width):
            rows = self.filter_rows_by_most_common(rows, idx, invert=True)
            if len(rows) == 1:
                break

        return int(''.join(map(str, rows[0])), 2)

    @property
    def life_support_rating(self):
        return self.oxygen_consumption * self.co2_scrubber_rating


def main():
    with open("input", "r") as f:
        report_content = f.read()

    report = DiagnosticReport(report_content)

    print(report.oxygen_consumption)
    print(report.co2_scrubber_rating)
    print(report.life_support_rating)



if __name__ == "__main__":
    main()

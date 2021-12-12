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

    @property
    def column_modes(self):
        return [statistics.mode(col) for col in self.cols]

    @property
    def gamma_rate(self):
        return int(''.join(map(str, self.column_modes)), 2)

    @property
    def epsilon_rate(self):
        return self.bit_not(self.gamma_rate)

    def bit_not(self, n):
        return (1 << self.width) - 1 - n

    @property
    def power_consumption(self):
        return self.gamma_rate * self.epsilon_rate


def main():
    with open("input", "r") as f:
        report_content = f.read()

    report = DiagnosticReport(report_content)

    print(report.gamma_rate)
    print(report.epsilon_rate)
    print(report.power_consumption)



if __name__ == "__main__":
    main()

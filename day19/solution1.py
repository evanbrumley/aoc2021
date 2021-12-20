import re
import numpy as np
from scipy.spatial.transform import Rotation as R


def rotation_matrix(axes, degrees):
    m = R.from_euler(axes, degrees, degrees=True).as_matrix()
    return m.astype(int)


ALL_ROTATIONS = (
    rotation_matrix("xz", (0, 0)),
    rotation_matrix("xz", (0, 90)),
    rotation_matrix("xz", (0, 180)),
    rotation_matrix("xz", (0, 270)),
    rotation_matrix("xy", (0, 90)),
    rotation_matrix("xy", (0, 270)),
    rotation_matrix("xz", (90, 0)),
    rotation_matrix("xz", (90, 90)),
    rotation_matrix("xz", (90, 180)),
    rotation_matrix("xz", (90, 270)),
    rotation_matrix("xy", (90, 90)),
    rotation_matrix("xy", (90, 270)),
    rotation_matrix("xz", (180, 0)),
    rotation_matrix("xz", (180, 90)),
    rotation_matrix("xz", (180, 180)),
    rotation_matrix("xz", (180, 270)),
    rotation_matrix("xy", (180, 90)),
    rotation_matrix("xy", (180, 270)),
    rotation_matrix("xz", (270, 0)),
    rotation_matrix("xz", (270, 90)),
    rotation_matrix("xz", (270, 180)),
    rotation_matrix("xz", (270, 270)),
    rotation_matrix("xy", (270, 90)),
    rotation_matrix("xy", (270, 270)),
)


class Scanner:
    def __init__(self, scanner_id, beacons):
        self.scanner_id = scanner_id
        self.beacons = np.array(beacons)
        self.location = None

    def __str__(self):
        output = ""
        output += f"Scanner #{self.scanner_id}\n"

        for beacon in self.beacons:
            output += f"{beacon}\n"

        return output

    @classmethod
    def from_input(cls, lines):
        match = re.match(r"--- scanner (?P<scanner_id>\d+) ---", lines[0])

        if not match:
            raise Exception("Invalid Input %s" % lines[0])

        scanner_id = int(match.group("scanner_id"))
        beacons = []

        for line in lines[1:]:
            match = re.match(r"(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)", line)

            if not match:
                raise Exception("Invalid Input %s" % line)

            beacons.append((
                int(match.group("x")),
                int(match.group("y")),
                int(match.group("z")),
            ))

        return cls(scanner_id, beacons)


class Problem:
    def __init__(self, scanners):
        self.scanners = scanners

    def __str__(self):
        output = ""

        for scanner in self.scanners:
            output += f"{scanner}\n"

        return output

    @classmethod
    def from_input(cls, lines):
        scanners = []
        current_scanner_lines = []

        for line in lines:
            if not line.strip():
                scanners.append(Scanner.from_input(current_scanner_lines))
                current_scanner_lines = []
                continue

            current_scanner_lines.append(line)

        scanners.append(Scanner.from_input(current_scanner_lines))

        return cls(scanners)

    def solve(self):
        current = self.scanners[0].beacons

        scanners_to_place = [s for s in self.scanners]

        while scanners_to_place:
            scanner = scanners_to_place.pop(0)
            print("Looking for match on scanner #%s (%s remaining)" % (scanner.scanner_id, len(scanners_to_place) + 1))
            scanner_location, match = self.find_match(current, scanner.beacons)

            if match is not None:
                print("MATCH FOUND")
                current = self.union(current, match)
                scanner.location = scanner_location
            else:
                print("NO MATCH")
                scanners_to_place = scanners_to_place + [scanner]

        return current

    def find_match(self, current_beacons, new_beacons):
        for rotation in ALL_ROTATIONS:
            rotated_beacons = np.matmul(new_beacons, rotation)
            for existing_beacon in current_beacons:
                for new_beacon in rotated_beacons:
                    transposition = existing_beacon - new_beacon
                    transposed = rotated_beacons + transposition
                    intersect = self.intersect(transposed, current_beacons)
                    if len(intersect) >= 12:
                        scanner_location = np.array([0, 0, 0]) + transposition
                        return scanner_location, transposed

        return None, None

    def intersect(self, arr1, arr2):
        arr1_view = arr1.view([('', arr1.dtype)] * arr1.shape[1])
        arr2_view = arr2.view([('', arr2.dtype)] * arr2.shape[1])
        intersected = np.intersect1d(arr1_view, arr2_view)
        return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])

    def union(self, arr1, arr2):
        arr1_view = arr1.view([('', arr1.dtype)] * arr1.shape[1])
        arr2_view = arr2.view([('', arr2.dtype)] * arr2.shape[1])
        union = np.union1d(arr1_view, arr2_view)
        return union.view(arr1.dtype).reshape(-1, arr1.shape[1])

    def cast_all_to_int(self, l):
        return [int(x) for x in l]


def main():
    with open("input", "r") as f:
        lines = f.read().strip().splitlines()

    problem = Problem.from_input(lines)
    beacons = problem.solve()
    print(len(beacons))


if __name__ == "__main__":
    main()

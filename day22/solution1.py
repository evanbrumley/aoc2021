import re
from shapely.geometry import Polygon


class Instruction:
    def __init__(self, command, x_start, x_end, y_start, y_end, z_start, z_end):
        self.command = command
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.z_start = z_start
        self.z_end = z_end

        self._polygon = Polygon((
            (self.x_start - 0.5, self.y_start - 0.5),
            (self.x_end + 0.5, self.y_start - 0.5),
            (self.x_end + 0.5, self.y_end + 0.5),
            (self.x_start - 0.5, self.y_end + 0.5),
            (self.x_start - 0.5, self.y_start - 0.5),
        ))

    def __str__(self):
        return f"{self.command} " \
               f"x={self.x_start}..{self.x_end}" \
               f",y={self.y_start}..{self.y_end}" \
               f",z={self.z_start}..{self.z_end}"

    def get_polygon(self, z):
        if self.z_start <= z <= self.z_end:
            return self._polygon

        return None


class Reactor:
    def __init__(self, instructions):
        self.instructions = instructions
        self.slices = None

    def __str__(self):
        output = ""
        for instruction in self.instructions:
            output += str(instruction)
            output += "\n"

        return output

    @classmethod
    def from_input(cls, lines):
        instructions = []

        for line in lines:
            match = re.match(r"(?P<command>(on|off)) x=(?P<x_start>-?\d+)..(?P<x_end>-?\d+),y=(?P<y_start>-?\d+)..(?P<y_end>-?\d+),z=(?P<z_start>-?\d+)..(?P<z_end>-?\d+)", line)
            if not match:
                raise Exception("Invalid input: %s" % line)

            command = match.group("command")
            x_start = int(match.group("x_start"))
            x_end = int(match.group("x_end"))
            y_start = int(match.group("y_start"))
            y_end = int(match.group("y_end"))
            z_start = int(match.group("z_start"))
            z_end = int(match.group("z_end"))

            instruction = Instruction(command, x_start, x_end, y_start, y_end, z_start, z_end)

            instructions.append(instruction)

        return cls(instructions)

    @property
    def z_bounds(self):
        min_z = None
        max_z = None

        for instruction in self.instructions:
            if min_z is None or instruction.z_start < min_z:
                min_z = instruction.z_start

            if max_z is None or instruction.z_end > max_z:
                max_z = instruction.z_end

        return min_z, max_z

    def construct_slices(self):
        slices = []

        z_start, z_end = self.z_bounds

        for z in range(z_start, z_end+1):
            slices.append(self.construct_slice(z))

        return slices

    def construct_slice(self, z):
        print("Constructing slice z=%s" % z)
        slice = None

        for instruction in self.instructions:
            polygon = instruction.get_polygon(z)

            if polygon is None:
                continue

            if slice is None and instruction.command == "off":
                continue
            elif slice is None:
                slice = polygon
            else:
                if instruction.command == "on":
                    slice = slice.union(polygon)
                else:
                    slice = slice.difference(polygon)

        return slice


def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()[:20]

    reactor = Reactor.from_input(lines)
    slices = reactor.construct_slices()

    total_area = 0

    for slice in slices:
        if slice:
            total_area += slice.area

    print(total_area)

if __name__ == "__main__":
    main()

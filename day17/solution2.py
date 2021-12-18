import math
import re


class Problem:
    def __init__(self, target_x0, target_x1, target_y0, target_y1):
        self.target_x0 = target_x0
        self.target_x1 = target_x1
        self.target_y0 = target_y0
        self.target_y1 = target_y1

    def __str__(self):
        return f"x={self.target_x0}..{self.target_x1} y={self.target_y0}..{self.target_y1},"

    @classmethod
    def from_input(cls, input_str):
        match = re.match(r"target area: x=(?P<x0>-?\d+)..(?P<x1>-?\d+), y=(?P<y0>-?\d+)..(?P<y1>-?\d+)", input_str)

        if not match:
            raise Exception("Invalid Input: %s" % input_str)

        x0 = int(match.group("x0"))
        x1 = int(match.group("x1"))
        y0 = int(match.group("y0"))
        y1 = int(match.group("y1"))

        return cls(x0, x1, y0, y1)

    @property
    def vx_max(self):
        """
        The horizontal launch velocity at which we'll pass the target
        area in one second. Not worth checking any lower velocities.
        """
        return self.target_x1

    @property
    def vx_min(self):
        """
        The horizontal launch velocity at which the projectile
        will have slowed to zero before reaching the target area.
        """
        return -0.5 + math.sqrt(0.25 + 2 * self.target_x0)

    def find_vy_min(self, vx):
        """
        The vertical launch velocity that means the projectile will be below
        the target area before we reach it when launched with horizontal
        velocity vx.
        """
        # Time at which we pass target_x0 if we start at velocity vx
        t = -0.5 * math.sqrt(4 * (vx**2) + 4*vx - 8*self.target_x0 + 1) + vx + 0.5
        result = (self.target_y0 / t) + (0.5 * t) - 0.5
        return result

    def find_vy_max(self, vx):
        """
        The y velocity that means the projectile will still be above
        the target area at the time we pass it in the x direction
        when launched with x velocity vx
        """
        # X movement stops in the middle of the target area range, so there's
        # no theoretical limit to initial vy? Not sure about this. Just pick
        # a suitably big number for now
        if (4 * (vx ** 2) + 4 * vx - 8 * self.target_x1 + 1) < 0:
            print("PUKE")
            return 400

        # Time at which we pass target_x1 if we start at velocity vx
        t = -0.5 * math.sqrt(4 * (vx**2) + 4*vx - 8*self.target_x1 + 1) + vx + 0.5
        result = (self.target_y1 / t) + (0.5 * t) - 0.5
        return result

    @property
    def vx_range(self):
        return range(math.ceil(self.vx_min), self.vx_max + 1)

    def find_vy_range(self, vx):
        return range(math.ceil(self.find_vy_min(vx)), math.floor(self.find_vy_max(vx)) + 1)

    def find_valid_trajectories(self):
        trajectories = []

        for vx in self.vx_range:
            for vy in self.find_vy_range(vx):
                if self.trajectory_is_valid(vx, vy):
                    trajectories.append((vx, vy))

        return trajectories

    def calculate_x(self, t, vx):
        t = min(t, vx)  # v=0 after vx seconds
        return -0.5 * (t ** 2) + vx * t + 0.5 * t

    def calculate_y(self, t, vy):
        return -0.5 * (t ** 2) + vy * t + 0.5 * t

    def trajectory_is_valid(self, vx, vy):
        t = 0

        while True:
            t += 1
            x = self.calculate_x(t, vx)
            y = self.calculate_y(t, vy)

            if (x > self.target_x1 or y < self.target_y0):
                return False

            if (x >= self.target_x0 and x <= self.target_x1 and y >= self.target_y0 and y <= self.target_y1):
                return True


def main():
    with open("input", "r") as f:
        input_str = f.read().strip()

    p = Problem.from_input(input_str)

    print(p)
    print(len(p.find_valid_trajectories()))


if __name__ == "__main__":
    main()

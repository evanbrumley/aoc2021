import re

class Submarine:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.aim = 0

    def move_forward(self, distance):
        self.x = self.x + distance
        self.z = self.z + self.aim * distance

    def aim_up(self, distance):
        self.aim = self.aim - distance

    def aim_down(self, distance):
        self.aim = self.aim + distance

    def process_command(self, command_str):
        match = re.match(r"(?P<command>forward|down|up) (?P<distance>\d+)", command_str)

        if not match:
            raise Exception("Invalid command: %s" % command_str)

        command = match.group("command")
        distance = int(match.group("distance"))

        old_x = self.x
        old_z = self.z
        old_aim = self.aim

        if command == "forward":
            self.move_forward(distance)
        elif command == "up":
            self.aim_up(distance)
        elif command == "down":
            self.aim_down(distance)

        print(f"{command_str}: {old_x},{old_z} ({old_aim}) -> {self.x},{self.z} ({self.aim})")

def main():
    with open("input", "r") as f:
        commands = f.read().splitlines()

    submarine = Submarine()

    for command in commands:
        submarine.process_command(command)

    print(submarine.x)
    print(submarine.z)
    print(submarine.x * submarine.z)



if __name__ == "__main__":
    main()

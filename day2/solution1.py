import re

class Submarine:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def move_forward(self, distance):
        self.x = self.x + distance

    def move_backward(self, distance):
        self.x = self.x - distance

    def move_up(self, distance):
        self.z = self.z + distance

    def move_down(self, distance):
        self.z = self.z - distance

    def process_command(self, command_str):
        match = re.match(r"(?P<command>forward|backward|down|up) (?P<distance>\d+)", command_str)

        if not match:
            raise Exception("Invalid command: %s" % command_str)

        command = match.group("command")
        distance = int(match.group("distance"))

        if command == "forward":
            self.move_forward(distance)
        elif command == "backward":
            self.move_backward(distance)
        elif command == "up":
            self.move_up(distance)
        elif command == "down":
            self.move_down(distance)

def main():
    with open("input", "r") as f:
        commands = f.read().splitlines()

    submarine = Submarine()

    for command in commands:
        submarine.process_command(command)

    print(submarine.x * submarine.z)



if __name__ == "__main__":
    main()

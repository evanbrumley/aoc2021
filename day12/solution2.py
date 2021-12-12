import re


class Node:
    def __init__(self, name):
        self.name = name
        self.big = name.isupper()
        self.small = not self.big
        self.start = name == "start"
        self.end = name == "end"

    def __str__(self):
        return self.name

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours


class Path:
    def __init__(self, nodes, repeat_seen=False):
        self.nodes = nodes
        self.repeat_seen = repeat_seen

    def check_for_valid_traverse(self, node):
        if node.start:
            return False

        if node in self.nodes:
            if node.small and self.repeat_seen:
                return False

        return True

    def traverse(self, node):
        repeat = self.repeat_seen or (node.small and node in self.nodes)
        return Path(self.nodes + [node], repeat_seen=repeat)


class TraversalTree:
    def __init__(self, path):
        self.path = path
        self.complete = path.nodes[-1].end
        self.children = self.generate_children()

    def generate_children(self):
        if self.complete:
            return []

        children = []
        for node in self.path.nodes[-1].neighbours:
            if self.path.check_for_valid_traverse(node):
                new_path = self.path.traverse(node)
                children.append(TraversalTree(new_path))

        return children

    @property
    def complete_ancestors(self):
        result = []

        for c in self.children:
            if c.complete:
                result.append(c)

            result = result + c.complete_ancestors

        return result

    @property
    def paths(self):
        return [a.path for a in self.complete_ancestors]


class Network:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.start = None
        self.end = None

        for node in nodes:
            if node.start:
                self.start = node

            if node.end:
                self.end = node

        if not self.start and self.end:
            raise Exception("Network Incomplete")

        for node in self.nodes:
            node.set_neighbours(self.find_neighbours(node))

        self.traversal_tree = self.build_traversal_tree()
        self.paths = self.traversal_tree.paths

    def build_traversal_tree(self):
        return TraversalTree(Path([self.start]))

    def find_neighbours(self, node):
        neighbours = []

        for n1, n2 in self.edges:
            if n1 == node:
                neighbours.append(n2)
            if n2 == node:
                neighbours.append(n1)

        return set(neighbours)

    @classmethod
    def from_raw_lines(cls, lines):
        nodes_by_name = {}
        edges = []

        for line in lines:
            match = re.match(r"(?P<n1>[a-zA-z]+)-(?P<n2>[a-zA-z]+)", line)
            if not match:
                raise Exception("Invalid input: %s", line)

            n1_name = match.group("n1")
            n2_name = match.group("n2")

            if n1_name in nodes_by_name:
                n1 = nodes_by_name[n1_name]
            else:
                n1 = Node(n1_name)
                nodes_by_name[n1_name] = n1

            if n2_name in nodes_by_name:
                n2 = nodes_by_name[n2_name]
            else:
                n2 = Node(n2_name)
                nodes_by_name[n2_name] = n2

            edges.append((n1, n2))

        return cls(nodes_by_name.values(), edges)

    def __str__(self):
        output = ""

        for n1, n2 in self.edges:
            output = output + f"{n1.name}-{n2.name}\n"

        output = output + "\n"

        for node in self.nodes:
            neighbours_str = ",".join([n.name for n in node.neighbours])
            output = output + f"{node} -> {neighbours_str}\n"

        return output

def main():
    with open("input", "r") as f:
        lines = f.read().splitlines()

    network = Network.from_raw_lines(lines)

    print(len(network.paths))



if __name__ == "__main__":
    main()

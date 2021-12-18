from construct import Struct, Bitwise, BitsInteger, GreedyRange, Bytes, this, IfThenElse, RepeatUntil, Array, LazyBound, FixedSized
import math


operator_content_format = Struct(
    "length_type_id" / BitsInteger(1),
    "length" / IfThenElse(this.length_type_id == 0, BitsInteger(15), BitsInteger(11)),
    "subpackets" / IfThenElse(
        this.length_type_id == 0,
        FixedSized(this.length, GreedyRange(LazyBound(lambda: packet_format))),
        Array(this.length, LazyBound(lambda: packet_format)),
    ),
)

literal_num = Struct(
    "flag" / BitsInteger(1),
    "val" / Array(4, BitsInteger(1)),  # TODO: Figure out how to do this properly
)

literal_content_format = RepeatUntil(lambda obj,lst,ctx: obj.flag == 0, literal_num)

packet_format = Struct(
    "version" / BitsInteger(3),
    "type_id" / BitsInteger(3),
    "content" / IfThenElse(this.type_id == 4, literal_content_format, operator_content_format),
)

message_format = Bitwise(Struct(
    "message" / packet_format,
    "leftovers" / GreedyRange(BitsInteger(1)),
))


class Message:
    def __init__(self, message_str):
        self.message_str = message_str
        self.message_bytes = bytes.fromhex(message_str)
        self.message = message_format.parse(self.message_bytes).message

    def __str__(self):
        return str(self.message.type_id)

    @property
    def all_packets(self):
        return self.find_packets(self.message)

    def find_packets(self, packet):
        packets = [packet]

        if packet.type_id == 4:
            return packets

        for subpacket in packet.content.subpackets:
            packets = packets + self.find_packets(subpacket)

        return packets

    @property
    def version_sum(self):
        return sum([p.version for p in self.all_packets])

    def evaluate(self):
        node = self.build_node(self.message)
        return node.evaluate()

    def build_node(self, packet):
        if packet.type_id == 4:
            return LiteralNode(self.calculate_literal_value(packet))

        subnodes = [self.build_node(subpacket) for subpacket in packet.content.subpackets]
        return OPERATION_NODE_MAPPING[packet.type_id](subnodes)

    def calculate_literal_value(self, packet):
        bits = ""

        for v in packet.content:
            for bit in v.val:
                bits = bits + str(bit)

        return int(bits, 2)


class Node:
    def evaluate(self):
        raise NotImplementedError


class LiteralNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class OperationNode(Node):
    def __init__(self, subnodes):
        self.subnodes = subnodes

    def evaluate(self):
        raise NotImplementedError


class SumNode(OperationNode):
    def evaluate(self):
        return sum([n.evaluate() for n in self.subnodes])


class ProductNode(OperationNode):
    def evaluate(self):
        return math.prod([n.evaluate() for n in self.subnodes])


class MinNode(OperationNode):
    def evaluate(self):
        return min([n.evaluate() for n in self.subnodes])


class MaxNode(OperationNode):
    def evaluate(self):
        return max([n.evaluate() for n in self.subnodes])


class GTNode(OperationNode):
    def evaluate(self):
        n0 = self.subnodes[0].evaluate()
        n1 = self.subnodes[1].evaluate()

        if n0 > n1:
            return 1

        return 0


class LTNode(OperationNode):
    def evaluate(self):
        n0 = self.subnodes[0].evaluate()
        n1 = self.subnodes[1].evaluate()

        if n0 < n1:
            return 1

        return 0


class EQNode(OperationNode):
    def evaluate(self):
        n0 = self.subnodes[0].evaluate()
        n1 = self.subnodes[1].evaluate()

        if n0 == n1:
            return 1

        return 0


OPERATION_NODE_MAPPING = {
    0: SumNode,
    1: ProductNode,
    2: MinNode,
    3: MaxNode,
    5: GTNode,
    6: LTNode,
    7: EQNode,
}


def main():
    with open("input", "r") as f:
        message_str = f.read().strip()

    message = Message(message_str)

    print(message.evaluate())


if __name__ == "__main__":
    main()

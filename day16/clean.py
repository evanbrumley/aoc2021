from construct import Struct, Bitwise, BitsInteger, GreedyRange, this, IfThenElse, RepeatUntil, Array, LazyBound, FixedSized, Computed
import math


LENGTH_TYPE_FIXED = 0
LENGTH_TYPE_NUMPACKETS = 1

PACKET_TYPE_OPERATION_SUM = 0
PACKET_TYPE_OPERATION_PRODUCT = 1
PACKET_TYPE_OPERATION_MIN = 2
PACKET_TYPE_OPERATION_MAX = 3
PACKET_TYPE_LITERAL = 4
PACKET_TYPE_OPERATION_GT = 5
PACKET_TYPE_OPERATION_LT = 6
PACKET_TYPE_OPERATION_EQ = 7


def reconstruct_literal(ctx):
    bitstring = ""

    for seg in ctx.segments:
        for bit in seg.bits:
            bitstring = bitstring + str(bit)

    return int(bitstring, 2)


operator_format = Struct(
    "length_type_id" / BitsInteger(1),
    "length" / IfThenElse(this.length_type_id == LENGTH_TYPE_FIXED, BitsInteger(15), BitsInteger(11)),
    "subpackets" / IfThenElse(
        this.length_type_id == LENGTH_TYPE_FIXED,
        FixedSized(this.length, GreedyRange(LazyBound(lambda: packet_format))),
        Array(this.length, LazyBound(lambda: packet_format)),
    ),
)


literal_format = Struct(
    "segments" / RepeatUntil(lambda obj, lst, ctx: obj.flag == 0, Struct(
        "flag" / BitsInteger(1),
        "bits" / Array(4, BitsInteger(1)),
    )),
    "val" / Computed(reconstruct_literal)
)


packet_format = Struct(
    "version" / BitsInteger(3),
    "type_id" / BitsInteger(3),
    "content" / IfThenElse(this.type_id == PACKET_TYPE_LITERAL, literal_format, operator_format),
)


message_format = Bitwise(Struct(
    "packet" / packet_format,
    "leftovers" / GreedyRange(BitsInteger(1)),
))


class Message:
    def __init__(self, message_str):
        self.message_str = message_str
        self.message_bytes = bytes.fromhex(message_str)
        self.message = message_format.parse(self.message_bytes)

    @property
    def all_packets(self):
        return self.find_packets(self.message.packet)

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
        node = self.build_node(self.message.packet)
        return node.evaluate()

    def build_node(self, packet):
        if packet.type_id == PACKET_TYPE_LITERAL:
            return LiteralNode(packet.content.val)

        subnodes = [self.build_node(subpacket) for subpacket in packet.content.subpackets]
        return OPERATION_NODE_MAPPING[packet.type_id](subnodes)


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
    PACKET_TYPE_OPERATION_SUM: SumNode,
    PACKET_TYPE_OPERATION_PRODUCT: ProductNode,
    PACKET_TYPE_OPERATION_MIN: MinNode,
    PACKET_TYPE_OPERATION_MAX: MaxNode,
    PACKET_TYPE_OPERATION_GT: GTNode,
    PACKET_TYPE_OPERATION_LT: LTNode,
    PACKET_TYPE_OPERATION_EQ: EQNode,
}


def main():
    with open("input", "r") as f:
        message_str = f.read().strip()

    message = Message(message_str)

    print(message.evaluate())


if __name__ == "__main__":
    main()

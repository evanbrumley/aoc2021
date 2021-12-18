from construct import Struct, Bitwise, BitsInteger, GreedyRange, this, IfThenElse, RepeatUntil, Array, LazyBound, Probe, FixedSized


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
    "val" / BitsInteger(4),
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


def main():
    with open("input", "r") as f:
        message_str = f.read().strip()

    message = Message(message_str)

    print(message.version_sum)


if __name__ == "__main__":
    main()

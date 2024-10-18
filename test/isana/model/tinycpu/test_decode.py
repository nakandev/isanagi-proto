from isana.isa import Instruction, parameter, assembly, binary
from isana.model.tinycpu.python.isa import isa_le, isa_be


class instr16(Instruction):
    opn, opc = "instr16", 0x1234
    prm = parameter("", "")
    asm = assembly("$opn")
    bin = binary("$opc[15:0]")


def test_decode():
    values = (
        (0b10000001_00011000_01000000_00000001).to_bytes(4, "little"),  # addi
        (0b10100111_00011000_01000000_00010001).to_bytes(4, "little"),  # add
        (0b00000000_00000000_00000000_00000000).to_bytes(4, "little"),  # unknown
    )
    for value in values:
        instr = isa_le.decode(value)
        print(instr, instr.bitsize)


def test_decode_bigendian():
    isa_be.instructions += [instr16]
    values = (
        b'\x12',
        b'\x12\x34',
        b'\x34\x12',  # correct
        b'\x12\x34\x56\x78',
        b'\x34\x12\x78\x56',  # correct
        b'\x78\x56\x34\x12',
    )
    for value in values:
        instr = isa_be.decode(value)
        print(instr, instr.bitsize)


if __name__ == '__main__':
    test_decode()
    test_decode_bigendian()

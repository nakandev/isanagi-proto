from isana.model.tinycpu.python.isa import isa


def test_decode():
    values = (
        0b10000001_00011000_01000000_00000001,  # addi
        0b10100111_00011000_01000000_00010001,  # add
        0b00000000_00000000_00000000_00000000,  # unknown
    )
    for value in values:
        instr = isa.decode(value)
        print(instr, instr.bitsize)


if __name__ == '__main__':
    test_decode()

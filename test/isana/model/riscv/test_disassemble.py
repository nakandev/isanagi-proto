from isana.model.riscv.python.isa import isa  # noqa


def test_decode():
    values = (
        0b10000000000000000001_10001_0110111,  # lui
        0b10000000000000000001_10001_0010111,  # auipc
        0b00000000000000000000_00000_1101111,  # jal
        0b000000000000_00000_000_00000_1100111,  # jalr
        0b1000001_10001_10001_000_10001_1100011,  # beq
        0b1000001_10001_10001_001_10001_1100011,  # bne
        0b1000001_10001_10001_100_10001_1100011,  # blt
        0b1000001_10001_10001_101_10001_1100011,  # bge
        0b1000001_10001_10001_110_10001_1100011,  # bltu
        0b1000001_10001_10001_111_10001_1100011,  # bgeu
        0b100000000001_10001_000_10001_0000011,  # lb
        0b100000000001_10001_001_10001_0000011,  # lh
        0b100000000001_10001_010_10001_0000011,  # lw
        0b100000000001_10001_100_10001_0000011,  # lbu
        0b100000000001_10001_101_10001_0000011,  # lhu
        0b1000001_10001_10001_000_10001_0100011,  # sb
        0b1000001_10001_10001_001_10001_0100011,  # sh
        0b1000001_10001_10001_010_10001_0100011,  # sw
        0b100000000001_10001_000_10001_0010011,  # addi
        0b100000000001_10001_010_10001_0010011,  # slti
        0b100000000001_10001_011_10001_0010011,  # sltiu
        0b100000000001_10001_100_10001_0010011,  # xori
        0b100000000001_10001_110_10001_0010011,  # ori
        0b100000000001_10001_111_10001_0010011,  # andi
        0b0000000_00001_10001_001_10001_0010011,  # slli
        0b0000000_00001_10001_101_10001_0010011,  # srli
        0b0100000_00001_10001_101_10001_0010011,  # srai
        0b0000000_10001_10001_000_10001_0110011,  # add
        0b0100000_00000_00000_000_00000_0110011,  # sub
        0b0000000_00000_00000_001_00000_0110011,  # sll
        0b0000000_00000_00000_010_00000_0110011,  # slt
        0b0000000_00000_00000_011_00000_0110011,  # sltu
        0b0000000_00000_00000_100_00000_0110011,  # xor
        0b0000000_00000_00000_101_00000_0110011,  # srl
        0b0100000_00000_00000_101_00000_0110011,  # sra
        0b0000000_00000_00000_110_00000_0110011,  # or
        0b0000000_00000_00000_111_00000_0110011,  # and
        0b0000_0000_0000_00000_000_00000_0001111,  # fence
        0b1000_0011_0011_00000_000_00000_0001111,  # fence.tso
        0b000000000000_00000_000_00000_1110011,  # ecall
        0b000000000001_00000_000_00000_1110011,  # ebreak
        0b100000000001_00000_001_00000_0001111,  # fence.i
        0b000000000000_10001_001_10001_1110011,  # csrrw
        0b000000000000_10001_010_10001_1110011,  # csrrs
        0b000000000000_10001_011_10001_1110011,  # csrrc
        0b000000000000_10001_101_10001_1110011,  # csrrwi
        0b000000000000_10001_110_10001_1110011,  # csrrsi
        0b000000000000_10001_111_10001_1110011,  # csrrci
        0b0000001_00000_00000_000_00000_0110011,  # mul
        0b0000001_00000_00000_001_00000_0110011,  # mulh
        0b0000001_00000_00000_010_00000_0110011,  # mulhsu
        0b0000001_00000_00000_011_00000_0110011,  # mulhu
        0b0000001_00000_00000_100_00000_0110011,  # div
        0b0000001_00000_00000_101_00000_0110011,  # divu
        0b0000001_00000_00000_110_00000_0110011,  # rem
        0b0000001_00000_00000_111_00000_0110011,  # remu
        0b00010_0_0_00000_00000_010_00000_0101111,  # lr.w
        0b00011_0_0_00000_00000_010_00000_0101111,  # sc.w
        0b00001_0_0_00000_00000_010_00000_0101111,  # amoswap.w
        0b00000_0_0_00000_00000_010_00000_0101111,  # amoadd.w
        0b00100_0_0_00000_00000_010_00000_0101111,  # amoxor.w
        0b01100_0_0_00000_00000_010_00000_0101111,  # amoand.w
        0b01000_0_0_00000_00000_010_00000_0101111,  # amoor.w
        0b10000_0_0_00000_00000_010_00000_0101111,  # amomin.w
        0b10100_0_0_00000_00000_010_00000_0101111,  # amomax.w
        0b11000_0_0_00000_00000_010_00000_0101111,  # amominu.w
        0b11100_0_0_00000_00000_010_00000_0101111,  # amomaxu.w

        0b000_00000000_000_00,  # illegal
        0b000_00000001_000_00,  # c.addi4spn
    )

    for value in values:
        instr = isa.decode(value)
        s = instr.disassemble()
        print(s)


if __name__ == '__main__':
    test_decode()
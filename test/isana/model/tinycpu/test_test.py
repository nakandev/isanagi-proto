from isana.model.tinycpu.python.isa import isa_le, isa_be  # noqa
from isana.test import InstructionTest


def test_binary_case():
    isa = isa_le
    for instr in isa.instructions[:1]:
        print("opn:{}".format(instr.opn))
        test = InstructionTest(isa, instr)
        testcases = test.gen_binary_edge_case()
        print("  edge case")
        for tc in testcases:
            print("    value: {:08x} {}".format(tc['value'], tc['func']))
        print("  random case")
        testcases = test.gen_binary_random_case(repeat=10)
        for tc in testcases:
            print("    value: {:08x} {}".format(tc['value'], tc['func']))


def test_asm_case():
    isa = isa_le
    for instr in isa.instructions[:1]:
        print("opn:{}".format(instr.opn))
        test = InstructionTest(isa, instr)
        testcases = test.gen_asm_edge_case()
        print("  edge case")
        for tc in testcases:
            print("    asm: '{}' {}".format(tc['asm'], tc['func']))
        print("  random case")
        testcases = test.gen_asm_random_case(repeat=10)
        for tc in testcases:
            print("    asm: '{}' {}".format(tc['asm'], tc['func']))


if __name__ == '__main__':
    # test_binary_case()
    test_asm_case()

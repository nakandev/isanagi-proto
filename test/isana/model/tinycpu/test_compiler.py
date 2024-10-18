from isana.model.tinycpu.python.isa import isa
import os

def test_compiler_generation():
    curdir = os.path.dirname(__file__)

    llvmcc = isa.compiler()
    llvmcc.outdir = os.path.join(curdir, "out")

    llvmcc.gen_registerinfo_td()
    llvmcc.gen_instrinfo_td()


if __name__ == '__main__':
    test_compiler_generation()

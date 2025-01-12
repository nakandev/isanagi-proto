from okojo.elf import ElfObject
import os


def main():
    curdir = os.path.dirname(os.path.abspath(__file__))
    elfpath = os.path.join(curdir, "src", "test1-gcc-rv32i.elf")
    elf = ElfObject(elfpath)
    elf.read_all()
    print(elf.elf_header)


if __name__ == "__main__":
    main()

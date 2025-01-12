GCC_X86 = gcc
GCC_RV32I = riscv32-unknown-elf-gcc
CLANG_X86 = clang

.PHONY = all test1 test2 clean

all: test1 test2

test1:
	$(GCC_X86) $@.c -o $@-gcc-x86.elf
	$(GCC_RV32I) $@.c -o $@-gcc-rv32i.elf
	$(CLANG_X86) $@.c -o $@-clang-x86.elf

test2:
	$(GCC_X86) $@.c -o $@-gcc-x86.elf
	$(GCC_RV32I) $@.c -o $@-gcc-rv32i.elf
	$(CLANG_X86) $@.c -o $@-clang-x86.elf

clean:
	rm -rf *.elf *.elf.*

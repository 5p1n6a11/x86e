#!/usr/bin/env python3

import sys
import struct

E_IDENT_IDX = {
    "EI_MAG0"    :  0,
    "EI_MAG1"    :  1,
    "EI_MAG2"    :  2,
    "EI_MAG3"    :  3,
    "EI_CLASS"   :  4,
    "EI_DATA"    :  5,
    "EI_VERSION" :  6,
    "EI_OSABI"   :  7,
    "EI_PAD"     :  8,
    "EI_NIDENT"  : 16,
}


EI_CLASS = {
    0: "ELFCLASSNONE",
    1: "ELFCLASS32",
    2: "ELFCLASS64",
}

EI_DATA = {
    0: "ELFDATANONE",
    1: "ELFDATA2LSB",
    2: "ELFDATA2MSB",
}

EI_VERSION = {
    0: "EV_NONE",
    1: "EV_CURRENT",
}

EI_OSABI = {
    0:  "ELFOSABI_NONE",
    1:  "ELFOSABI_SYSV",
    2:  "ELFOSABI_HPUX",
    3:  "ELFOSABI_NETBSD",
    4:  "ELFOSABI_LINUX",
    5:  "ELFOSABI_SOLARIS",
    6:  "ELFOSABI_IRIX",
    7:  "ELFOSABI_FREEBSD",
    8:  "ELFOSABI_TRU64",
    9:  "ELFOSABI_ARM",
    10: "ELFOSABI_STANDALONE",
}

E_TYPE = {
    0: "ET_NONE",
    1: "ET_REL",
    2: "ET_EXEC",
    3: "ET_DYN",
    4: "ET_CORE",
}

E_MACHINE = {
    0:   "EM_NONE",
    1:   "EM_M32",
    2:   "EM_SPARC",
    3:   "EM_386",
    4:   "EM_68K",
    5:   "EM_88K",
    6:   "EM_486",
    7:   "EM_860",
    8:   "EM_MIPS",
    15:  "EM_PARISC",
    18:  "EM_SPARC32PLUS",
    20:  "EM_PPC",
    21:  "EM_PPC64",
    23:  "EM_SPU",
    40:  "EM_ARM",
    42:  "EM_SH",
    43:  "EM_SPARCV9",
    46:  "EM_H8_300",
    50:  "EM_IA_64",
    62:  "EM_X86_64",
    22:  "EM_S390",
    76:  "EM_CRIS",
    88:  "EM_M32R",
    89:  "EM_MN10300",
    92:  "EM_OPENRISC",
    93:  "EM_ARCOMPACT",
    94:  "EM_XTENSA",
    106: "EM_BLACKFIN",
    110: "EM_UNICORE",
    113: "EM_ALTERA_NIOS2",
    140: "EM_TI_C6000",
    164: "EM_HEXAGON",
    167: "EM_NDS32",
    183: "EM_AARCH64",
    188: "EM_TILEPRO",
    189: "EM_MICROBLAZE",
    191: "EM_TILEGX",
    195: "EM_ARCV2",
    243: "EM_RISCV",
    247: "EM_BPF",
    252: "EM_CSKY",
}

E_VERSION = {
    0: "EV_NONE",
    1: "EV_CURRENT",
}

class readelf_h:
    def print_magic(e_ident):
        print("  Magic:", end ="")
        print("\t", end="")
        print("{0:02x} {1:02x} {2:02x} {3:02x} ".format(e_ident[0], e_ident[1], e_ident[2], e_ident[3]), end="")
        print("{0:02x} {1:02x} {2:02x} {3:02x} ".format(e_ident[4], e_ident[5], e_ident[6], e_ident[7]), end="")
        print("{0:02x} {1:02x} {2:02x} {3:02x} ".format(e_ident[8], e_ident[9], e_ident[10], e_ident[11]), end="")
        print("{0:02x} {1:02x} {2:02x} {3:02x} ".format(e_ident[12], e_ident[13], e_ident[14], e_ident[15]))

    def print_class(ei_class_idx):
        print("  Class:", end="")
        print("\t\t\t\t", end="")
        if EI_CLASS[ei_class_idx] == "ELFCLASS64":
            s = "ELF64"
        else:
            s = "None"
        print(s)

    def print_data(ei_data_idx): 
        print("  Data:", end="")
        print("\t\t\t\t\t", end="")
        if EI_DATA[ei_data_idx] == "ELFDATA2LSB":
            s = "2's complement, little endian"
        else:
            s = "None"
        print(s)

    def print_version(ei_version_idx):
        print("  Version:", end="")
        print("\t\t\t\t", end="")
        if EI_VERSION[ei_version_idx] == "EV_CURRENT":
            s = "1 (current)"
        else:
            s = "None"
        print(s)

    def print_osabi(ei_osabi_idx):
        print("  OS/ABI:", end="")
        print("\t\t\t\t", end="")
        if EI_OSABI[ei_osabi_idx] == "ELFOSABI_NONE":
            s = "UNIX - System V"
        else:
            s = "None"
        print(s)

    def print_abi_version(ei_abi_version):
        print("  ABI Version:", end="")
        print("\t\t\t\t", end="")
        print(ei_abi_version)

    def print_e_type(e_type_idx):
        print("  Type:", end="")
        print("\t\t\t\t\t", end="")
        if E_TYPE[e_type_idx] == "ET_DYN":
            s = "DYN (Shared object file)"
        else:
            s = "None"
        print(s)

    def print_e_machine(e_machine_idx):
        print("  Machine:", end="")
        print("\t\t\t\t", end="")
        if E_MACHINE[e_machine_idx] == "EM_X86_64": 
            s = "Advanced Micro Devices X86-64"
        else:
            s = "None"
        print(s)

    def print_e_version(e_version_idx):
        print("  Version:", end="")
        print("\t\t\t\t", end="")
        if E_VERSION[e_version_idx] == "EV_CURRENT":
            print(hex(e_version_idx))
        else:
            print("None")

    def print_e_entry(e_entry):
        print("  Entry point address:", end="")
        print("\t\t\t", end="")
        print(hex(e_entry))

    def print_e_phoff(e_phoff):
        print("  Start of program headers:", end="")
        print("\t\t", end="")
        print(e_phoff, end="")
        print(" (bytes into file)")

    def print_e_shoff(e_shoff):
        print("  Start of section headers:", end="")
        print("\t\t", end="")
        print(e_shoff, end="")
        print(" (bytes into file)")

    def print_e_flags(e_flags):
        print("  Flags:", end="")
        print("\t\t\t\t", end="")
        print(hex(e_flags))

    def print_e_ehsize(e_ehsize):
        print("  Size of this header:", end="")
        print("\t\t\t", end="")
        print(e_ehsize, end="")
        print(" (bytes)")

    def print_e_phentsize(e_phentsize):
        print("  Size of program headers:", end="")
        print("\t\t", end="")
        print(e_phentsize, end="")
        print(" (bytes)")

    def print_e_phnum(e_phnum):
        print("  Number of program headers:", end="")
        print("\t\t", end="")
        print(e_phnum)

    def print_e_shentsize(e_shentsize):
        print("  Sizo of section headers:", end="")
        print("\t\t", end="")
        print(e_shentsize, end="")
        print(" (bytes)")

    def print_e_shnum(e_shnum):
        print("  Number of section headers:", end="")
        print("\t\t", end="")
        print(e_shnum)

    def print_e_shstrndx(e_shstrndx):
        print("  Section header string table index:", end="")
        print("\t", end="")
        print(e_shstrndx)

    def print_readelf_h(elf_hdr):
        elf_hdr_offset = 0
        elf64_hdr = struct.unpack_from("16BHHIQQQIHHHHHH", elf_hdr, elf_hdr_offset)
        print("ELF Header:")
        e_ident = elf64_hdr[0:16]
        readelf_h.print_magic(e_ident)
        readelf_h.print_class(e_ident[E_IDENT_IDX["EI_CLASS"]])
        readelf_h.print_data(e_ident[E_IDENT_IDX["EI_DATA"]])
        readelf_h.print_version(e_ident[E_IDENT_IDX["EI_VERSION"]])
        readelf_h.print_osabi(e_ident[E_IDENT_IDX["EI_OSABI"]])
        readelf_h.print_abi_version(e_ident[8])
        e_type = elf64_hdr[16]
        readelf_h.print_e_type(e_type)
        e_machine = elf64_hdr[17]
        readelf_h.print_e_machine(e_machine)
        e_version = elf64_hdr[18]
        readelf_h.print_e_version(e_version)
        e_entry = elf64_hdr[19]
        readelf_h.print_e_entry(e_entry)
        e_phoff = elf64_hdr[20]
        readelf_h.print_e_phoff(e_phoff)
        e_shoff = elf64_hdr[21]
        readelf_h.print_e_shoff(e_shoff)
        e_flags = elf64_hdr[22]
        readelf_h.print_e_flags(e_flags)
        e_ehsize = elf64_hdr[23]
        readelf_h.print_e_ehsize(e_ehsize)
        e_phentsize = elf64_hdr[24]
        readelf_h.print_e_phentsize(e_phentsize)
        e_phnum = elf64_hdr[25]
        readelf_h.print_e_phnum(e_phnum)
        e_shentsize = elf64_hdr[26]
        readelf_h.print_e_shentsize(e_shentsize)
        e_shnum = elf64_hdr[27]
        readelf_h.print_e_shnum(e_shnum)
        e_shstrndx = elf64_hdr[28]
        readelf_h.print_e_shstrndx(e_shstrndx)

P_TYPE = {
    0: "PT_NULL",
    1: "PT_LOAD",
    2: "PT_DYNAMIC",
    3: "PT_INTERP",
    4: "PT_NOTE",
    5: "PT_SHLIB",
    6: "PT_PHDR",
    7: "PT_TLS",
}

P_FLAGS = {
    0x4: "PF_R",
    0x2: "PF_W",
    0x1: "PF_X",
}

if __name__ == '__main__':
    filename = sys.argv[1]

    with open(filename, 'rb') as f:
        elf = f.read()

    readelf_h.print_readelf_h(elf)

#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from emulator import *
from emulator_function import *
from instruction import *
import sys

MEMORY_SIZE = 1024 * 1024


def read_binary(emu, filename):
    offset = 0x7c00
    
    try:
        with open(filename, "rb") as binary:
            for _ in range(0x200):
                b = binary.read(1)
                if b == b'':
                    break
                emu.memory[offset] = b
                offset += 1
    except:
        print("{0}: cannot open file".format(filename))
        sys.exit(1)
        
def dump_registers(emu):
    for i in range(len(emu.registers)):
        reg_name = emu.registers_name[i]
        print("{0} = {1:#08x}".format(reg_name, get_register32(emu, i)))
    print("EIP = {0:#08x}".format(emu.eip))

def create_emu(size, eip, esp):
    eip &= 0xffffffff
    esp &= 0xffffffff
    emu = Emulator()

    emu.registers_name = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]

    emu.memory = [0x00 for _ in range(size)]

    emu.registers = {
        "EAX": 0x00,
        "ECX": 0x00,
        "EDX": 0x00,
        "EBX": 0x00,
        "ESP": 0x00,
        "EBP": 0x00,
        "ESI": 0x00,
        "EDI": 0x00,
    }

    emu.eip = eip & 0xffffffff
    emu.registers["ESP"] = esp

    return emu

def destroy_emu(emu):
    del emu

def main(argc, argv):

    if argc != 2:
        print("usage: px86 filename")
        return 1

    emu = create_emu(MEMORY_SIZE, 0x7c00, 0x7c00)

    init_instructions(emu)

    read_binary(emu, argv[1])

    while emu.eip < MEMORY_SIZE:
        code = get_code8(emu, 0)
        code &= 0xff
        print("EIP = {0:X}, Code = {1:02X}".format(emu.eip, code))

        if emu.instructions[code] == None:
            print("\n\nNot Implemented: {0:x}".format(code))
            break

        emu.instructions[code](emu)

        if emu.eip == 0:
            print("\n\nend of program.\n")
            break

    dump_registers(emu)
    destroy_emu(emu)
    return 0

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

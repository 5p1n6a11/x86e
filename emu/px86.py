#!/usr/bin/env python3

import sys
import numpy as np

MEMORY_SIZE = 1024 * 1024

Register = {
    "EAX": 0,
    "ECX": 1,
    "EDX": 2,
    "EBX": 3,
    "ESP": 4,
    "EBP": 5,
    "ESI": 6,
    "EDI": 7,
    "REGISTERS_COUNT": 8,
}

registers_name = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]

class Emulator():

    def create_emu(self, size, eip, esp):

        self.size = size

        self.registers = {
            "EAX": 0,
            "ECX": 0,
            "EDX": 0,
            "EBX": 0,
            "ESP": 0,
            "EBP": 0,
            "ESI": 0,
            "EDI": 0,
        }

        self.eip = eip
        self.registers["ESP"] = esp

        self.eflags = 0

    def dump_registers(self):

        for i in range(Register["REGISTERS_COUNT"]):
            print("{0} = {1:#08x}\n".format(registers_name[i], self.registers[registers_name[i]]))

        print("EIP = {0:#08x}\n".format(self.eip))

    def get_code8(self, index):
        return self.memory[self.eip + index]

    def get_sign_code8(self, index):
        return self.memory[self.eip + index]

    def get_code32(self, index):
        ret = 0

        for i in range(4):
            ret |= self.get_code8(index + i) << (i * 8)

        return ret

    def mov_r32_imm32(self):
        reg = self.get_code8(0) - 0xB8
        value = self.get_code32(1)
        self.registers[registers_name[reg]] = value
        self.eip += 5

    def short_jump(self):
        diff = self.get_sign_code8(1)
        self.eip += (diff + 2);

    def init_instructions(self):
        self.instructions = {}
        for i in range(8):
            self.instructions[0xB8 + i] = self.mov_r32_imm32
        self.instructions[0xEB] = self.short_jump

def main(argc, argv):

    if argc != 2:
        print("usage: px86 filename\n")
        return

    emu = Emulator()
    emu.create_emu(MEMORY_SIZE, 0x0000, 0x7c00)

    with open(argv[1], "rb") as binary:
        emu.memory = binary.read(0x200)

    emu.init_instructions()

    while emu.eip < MEMORY_SIZE:
        code = emu.get_code8(0)

        print("EIP = {0:#X}, Code = {1:#02X}\n".format(emu.eip, code))

        if code not in emu.instructions:
            print("\n\nNot Implemented: {0:#x}\n".format(code))
            break

        emu.instructions[code]()

        if emu.eip == 0x00:
            print("\n\nend of program.\n\n")
            break

    emu.dump_registers()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

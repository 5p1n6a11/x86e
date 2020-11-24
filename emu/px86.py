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
    def __init__(self):
        self.elfags = None
        self.memory = None
        self.size = None
        self.eip = None
        self.registers = None
        self.instructions = None

    def create_emu(self, size, eip, esp):

        self.size = size
        self.memory = [0x00 for _ in range(self.size)]

        self.registers = {
            "EAX": 0x00,
            "ECX": 0x00,
            "EDX": 0x00,
            "EBX": 0x00,
            "ESP": 0x00,
            "EBP": 0x00,
            "ESI": 0x00,
            "EDI": 0x00,
        }

        self.eip = eip & 0xffffffff
        self.registers["ESP"] = esp

    def dump_registers(self):

        for i in range(len(self.registers)):
            reg_name = registers_name[i]
            print("{0} = {1:#08x}".format(reg_name, self.registers[reg_name]))

        print("EIP = {0:#08x}".format(self.eip))

    def get_code8(self, index):
        code = self.memory[(self.eip + index) & 0xffffffff]
        if not type(code) == int:
            code = int.from_bytes(code, 'little')
        return code

    def get_sign_code8(self, index):
        code = self.memory[(self.eip + index) & 0xffffffff]
        code = int.from_bytes(code, 'little')
        return code & 0xff

    def get_code32(self, index):
        ret = 0

        for i in range(4):
            ret |= self.get_code8(index + i) << (i * 8)

        return ret

    def get_sign_code32(self, index):
        return self.get_code32(index)

    def mov_r32_imm32(self):
        reg = self.get_code8(0) - 0xB8
        value = self.get_code32(1)
        reg_name = registers_name[reg]
        self.registers[reg_name] = value
        self.eip += 5
        if self.eip >= 0x100000000:
            self.eip ^= 0x100000000

    def short_jump(self):
        diff = self.get_sign_code8(1)
        if diff & 0x80:
            diff -= 0x100
        self.eip += (diff + 2)
        self.eip &= 0xffffffff

    def near_jump(self):
        diff = self.get_sign_code32(1)
        self.eip += (diff + 5)
        self.eip &= 0xffffffff

    def init_instructions(self):
        self.instructions = [None for _ in range(256)]
        for i in range(8):
            self.instructions[0xB8 + i] = self.mov_r32_imm32
        self.instructions[0xE9] = self.near_jump
        self.instructions[0xEB] = self.short_jump

def main(argc, argv):

    if argc != 2:
        print("usage: px86 filename\n")
        return

    emu = Emulator()
    emu.create_emu(MEMORY_SIZE, 0x7c00, 0x7c00)

    offset = 0x7c00

    with open(argv[1], "rb") as binary:
        while True:
            b = binary.read(1)
            if b == b'':
                break
            emu.memory[offset] = b
            offset += 1

    emu.init_instructions()

    while emu.eip < MEMORY_SIZE:
        code = emu.get_code8(0)

        print("EIP = {0:#X}, Code = {1:#02X}".format(emu.eip, code))

        if emu.instructions[code] == None:
            print("\n\nNot Implemented: {0:#x}\n".format(code))
            break

        emu.instructions[code]()

        if emu.eip == 0x00:
            print("\n\nend of program.\n\n")
            break

    emu.dump_registers()

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

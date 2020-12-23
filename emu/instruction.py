#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import emulator
import emulator_function
import modrm
import sys

instructions = None

def mov_r32_imm32(emu):
    reg = get_code8(emu, 0) - 0xB8
    value = get_code32(emu, 1)
    set_register32(emu, reg, value)
    emu.eip += 5
    emu.eip &= 0xffffffff

def mov_r32_rm32(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)
    rm32 = get_rm32(emu, modrm)
    set_r32(emu, modrm, rm32)

def add_rm32_r32(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)
    r32 = get_r32(emu, modrm)
    rm32 = get_rm32(emu, modrm)
    set_rm32(emu, modrm, rm32 + r32)

def mov_rm32_r32(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)
    r32 = get_r32(emu, modrm)
    set_rm32(emu, modrm, r32)

def sub_rm32_imm8(emu, modrm):
    rm32 = get_rm32(emu, modrm)
    imm8 = get_sign_code8(emu, 0)
    emu.eip += 1
    emu.eip &= 0xffffffff
    set_rm32(emu, modrm, rm32 - imm8)

def code_83(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)

    if modrm.opecode == 5:
        sub_rm32_imm8(emu, modrm)
    else:
        print("not implemented: 83 /{0:d}".format(modrm.opecode))
        sys.exit(1)

def mov_rm32_imm32(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)
    value = get_code32(emu, 0)
    emu.eip += 4
    emu.eip &= 0xffffffff
    set_rm32(emu, modrm, value)

def inc_rm32(emu, modrm):
    value = get_rm32(emu, modrm)
    set_rm32(emu, modrm, value + 1)

def code_ff(emu):
    emu.eip += 1
    emu.eip &= 0xffffffff
    modrm = ModRM()
    parse_modrm(emu, modrm)

    if modrm.opecode == 0:
        inc_rm32(emu, modrm)
    else:
        print("not implemented: FF /{0:d}".format(modrm.opecode))
        sys.exit(1)

def short_jump(emu):
    diff = get_sign_code8(emu, 1)
    if diff & 0x80:
        diff -= 0x100
    emu.eip += (diff + 2)
    emu.eip &= 0xffffffff

def near_jump(emu):
    diff = get_sign_code32(emu, 1)
    emu.eip += (diff + 5)
    emu.eip &= 0xffffffff

def init_instructions():
    instructions = [None for _ in range(256)]
    instructions[0x01] = add_rm32_r32
    instructions[0x83] = code_83
    instructions[0x89] = mov_rm32_r32
    instructions[0x8B] = mov_r32_rm32
    for i in range(8):
        instructions[0xB8 + i] = mov_r32_imm32
    instructions[0xC7] = mov_rm32_imm32
    instructions[0xE9] = near_jump
    instructions[0xEB] = short_jump
    instructions[0xFF] = code_ff


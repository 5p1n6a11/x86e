#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from emulator import *

def get_code8(emu, index):
    index &= 0xffffffff
    code = emu.memory[(emu.eip + index) & 0xffffffff]
    code = int.from_bytes(code, 'little')
    return code

def get_sign_code8(emu, index):
    index &= 0xffffffff
    code = emu.memory[(emu.eip + index) & 0xffffffff]
    code = int.from_bytes(code, 'little')
    return code & 0xff

def get_code32(emu, index):
    index &= 0xffffffff
    ret = 0

    for i in range(4):
        ret |= get_code8(emu, index + i) << (i * 8)
        ret &= 0xffffffff

    return ret 

def get_sign_code32(emu, index):
    index &= 0xffffffff
    return get_code32(emu, index) & 0xffffffff

def get_register32(emu, index):
    index &= 0xffffffff
    reg_name = emu.registers_name[index]
    return emu.registers[reg_name]

def set_register32(emu, index, value):
    index &= 0xffffffff
    value &= 0xffffffff
    reg_name = emu.registers_name[index]
    emu.registers[reg_name] = value

def set_memory8(emu, address, value):
    address &= 0xffffffff
    value &= 0xffffffff
    emu.memory[address] = value & 0xff

def set_memory32(emu, address, value):
    address &= 0xffffffff
    value &= 0xffffffff

    for i in range(4):
        set_memory8(emu, address + i, value >> (i * 8))

def get_memory8(emu, address):
    address &= 0xffffffff
    return emu.memory[address]

def get_memory32(emu, address):
    ret = 0

    for i in range(4):
        ret |= get_memory8(emu, address + i) << (8 * i)
        ret &= 0xffffffff

    return ret

def push32(emu, value):
    value &= 0xffffffff
    reg_esp_idx = Register["ESP"]
    address = get_register32(emu, reg_esp_idx) - 4
    address &= 0xffffffff
    set_register32(emu, reg_esp_idx, address)
    set_memory32(emu, address, value)

def pop32(emu):
    reg_esp_idx = Register["ESP"]
    address = get_register32(emu, reg_esp_idx)
    address &= 0xffffffff
    ret = get_memory32(emu, address)
    ret &= 0xffffffff
    set_register32(emu, reg_esp_idx, address + 4)

    return ret


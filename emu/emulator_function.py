#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from emulator import *

def get_code8(emu, index):
    code = emu.memory[(emu.eip + index) & 0xffffffff]
    if not type(code) == int:
        code = int.from_bytes(code, 'little')
    return code

def get_sign_code8(emu, index):
    code = emu.memory[(emu.eip + index) & 0xffffffff]
    code = int.from_bytes(code, 'little')
    return code & 0xff

def get_code32(emu, index):
    ret = 0
    for i in range(4):
        ret |= get_code8(emu, index + i) << (i * 8)
    return ret

def get_sign_code32(emu, index):
    return get_code32(emu, index)

def get_register32(emu, index):
    reg_name = emu.registers_name[index]
    return emu.registers[reg_name]

def set_register32(emu, index, value):
    reg_name = emu.registers_name[index]
    emu.registers[reg_name] = value

def set_memory8(emu, address, value):
    emu.memory[address] = value & 0xff

def set_memory32(emu, address, value):
    for i in range(4):
        set_memory8(emu, address + i, value >> (i * 8))

def get_memory8(emu, address):
    return emu.memory[address]

def get_memory32(emu, address):
    ret = 0
    for i in range(4):
        ret |= get_memory8(emu, address + i) << (8 * i)
    return ret

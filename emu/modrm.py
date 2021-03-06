#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from emulator import *
from emulator_function import *
import ctypes

class ModRM():
    def __init__(self):
        self.mod = None
        self.opecode = None
        self.reg_index = None
        self.opecode = None
        self.rm = None
        self.sib = None
        self.disp8 = None
        self.disp32 = None

def parse_modrm(emu, modrm): # ???
    assert emu != None and modrm != None

    code = get_code8(emu, 0)
    code &= 0xff
    modrm.mod = ((code & 0xc0) >> 6)
    modrm.mod &= 0xff
    modrm.opecode = ((code & 0x38) >> 3)
    modrm.opecode &= 0xff
    modrm.reg_index = modrm.opecode
    modrm.reg_index &= 0xff
    modrm.rm = code & 0x07
    modrm.rm &= 0xff

    emu.eip += 1
    emu.eip &= 0xffffffff

    if modrm.mod != 3 and modrm.rm == 4:
        modrm.sib = get_code8(emu, 0)
        modrm.sib &= 0xff
        emu.eip += 1
        emu.eip &= 0xffffffff

    if (modrm.mod == 0 and modrm.rm == 5) or modrm.mod == 2:
        modrm.disp32 = get_sign_code32(emu, 0)
        modrm.disp32 &= 0xffffffff
        modrm.disp8 = ctypes.c_int8(modrm.disp32)
        emu.eip += 4
        emu.eip &= 0xffffffff
    elif modrm.mod == 1:
        modrm.disp8 = get_sign_code8(emu, 0)
        modrm.disp8 &= 0xff
        modrm.disp32 = ctypes.c_unit32(modrm.dips8)
        emu.eip += 1
        emu.eip &= 0xffffffff

def calc_memory_address(emu, modrm):
    if modrm.mod == 0:
        if modrm.mod == 4:
            print("not implemented ModRM mod = 0, rm = 4")
            exit(0)
        elif modrm.rm == 5:
            return modrm.disp32
        else:
            return get_register32(emu, modrm.rm)

    elif modrm.mod == 1:
        if modrm.rm == 4:
            print("not implemented ModRM mod = 1, rm = 4")
            exit(0)
        else:
            return get_register32(emu, modrm.rm) + modrm.disp8

    elif modrm.rm == 2:
        if modrm.rm == 4:
            print("not implemented ModRM mod = 2, rm = 4")
            exit(0)
        else:
            return get_register32(emu, modrm.rm) + modrm.disp32

    else:
        print("not implemented ModRM mod = 3")
        exit(0)

def set_rm32(emu, modrm, value):
    value &= 0xffffffff
    if modrm.mod == 3:
        set_register32(emu, modrm.rm, value)
    else:
        address = calc_memory_address(emu, modrm)
        address &= 0xffffffff
        set_memory32(emu, address, value)

def get_rm32(emu, modrm):
    if modrm.mod == 3:
        return get_register32(emu, modrm.rm)
    else:
        address = calc_memory_address(emu, modrm)
        address &= 0xffffffff
        return get_memory32(emu, address)

def set_r32(emu, modrm, value):
    value &= 0xffffffff
    set_register32(emu, modrm.reg_index, value)

def get_r32(emu, modrm):
    return get_register32(emu, modrm.reg_index)


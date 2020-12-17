#!/usr/bin/env python
#-*- coding: utf-8 -*-
# reference: unicorn/bindings/python/sample_x86.py

from __future__ import print_function # python2.7 ?
from unicorn import *
from unicorn.x86_const import *
from capstone import *

# エミュレーション対象の機械語
X86_CODE32 = b"\x41\x4a" # INC ecx; DEC edx

# memory address where emulation starts
ADDRESS = 0x1000000

# 各基本ブロックに対するコールバック
def hook_block(uc, address, size, user_data):
    print(">>> Tracing basic block at 0x%x, block size = 0x%x" %(address, size))

# 各命令に対するコールバック
# def hook_code(uc, address, size, user_data):
#     print(">>> Tracing instruction at 0x%x, instruction size = %u" %(address, size))

# x86 32bitのコードをエミュレーション
def test_i386():
    print("Emulate i386 code")
    try:
        # x86-32bitモードでエミュレータを初期化
        mu = Uc(UC_ARCH_X86, UC_MODE_32)
        # エミュレーション用に2MBのメモリを割り当て
        mu.mem_map(ADDRESS, 2 * 1024 * 1024)
        # 割り当てられたメモリに機械語を書き込み
        mu.mem_write(ADDRESS, X86_CODE32)
        # レジスタ初期化
        mu.reg_write(UC_X86_REG_ECX, 0x1234) # エミュレーション中に加算される
        mu.reg_write(UC_X86_REG_EDX, 0x7890) # エミュレーション中に減算される
        # 各基本ブロックに対するコールバックを設定
        mu.hook_add(UC_HOOK_BLOCK, hook_block)
        # 各命令に対するコールバックを設定
        mu.hook_add(UC_HOOK_CODE, hook_code)
        # エミュレーション開始
        mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE32))
        # レジスタの表示
        print(">>> Emulation done. Below is the CPU context")
        r_ecx = mu.reg_read(UC_X86_REG_ECX)
        r_edx = mu.reg_read(UC_X86_REG_EDX)
        print(">>> ECX = 0x%x" %r_ecx)
        print(">>> EDX = 0x%x" %r_edx)
        # メモリから命令列を読む
        tmp = mu.mem_read(ADDRESS, 2)
        print(">>> Read 2 bytes from [0x%x] =" %(ADDRESS), end="")
        for i in tmp:
            print(" 0x%x" %i, end="")
        print("")
    except UcError as e:
        print("ERROR: %s" % e)


class SimpleEngine:
    def __init__(self):
        self.capmd = Cs(CS_ARCH_X86, CS_MODE_32) # アーキテクチャ指定
    def disas_single(self, data):
        for i in self.capmd.disasm(data, 16): # 逆アセンブル
            print("\t%s\t%s" % (i.mnemonic, i.op_str))
            break
disasm = SimpleEngine()

def hook_code(uc, address, size, user_data):
    print(">>> Tracing instruction at 0x%x, instruction size = %u, " %(address, size), end="")
    # メモリから実行される命令を読む
    ins = uc.mem_read(address, size)
    disasm.disas_single(ins)

if __name__ == '__main__':
    test_i386()


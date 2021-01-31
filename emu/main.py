#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from emulator import *
from emulator_function import *
from instruction import *

MEMORY_SIZE = 1024 * 1024

registers_name = ["EAX", "ECX", "EDX", "EBX", "ESP", "EBP", "ESI", "EDI"]

def read_binary(emu, filename):
    
    try:
        with open(filename, "rb") as binary:
            pass
    except:
        print("{0}: cannot open file".format(filename))
        exit(1)
        

#!/usr/bin/env python3

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

class Emulator():
    def __init__(self):
        self.registers = None
        self.elfags    = None
        self.memory    = None
        self.eip       = None

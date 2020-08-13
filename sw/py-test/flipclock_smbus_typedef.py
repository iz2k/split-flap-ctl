from enum import Enum

class SMB_REGS(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, a, b, c, d):
        self.address: int = a
        self.len: int = b
        self.type: int = c
        self.content: int = d

    SMB_FW_VERSION = 1, 2, int, 0
    SMB_DESIRED_DIGIT = 2, 1, int, 0
    SMB_CURRENT_DIGIT = 3, 1, int, 0
    SMB_HALL_FIND = 4, 1, int, 0
    SMB_HALL_THRESHOLD = 5, 2, int, 0
    SMB_HALL_DIGIT = 6, 1, int, 0
    SMB_IR_THRESHOLD = 7, 2, int, 0
    SMB_IR_TURNON_TIME = 8, 2, int, 0
    SMB_IR_DEBOUNCE_TIME = 9, 2, int, 0

class SMB_OPS(Enum):
    SMB_OP_NONE = 0b00000000
    SMB_OP_READ = 0b01000000
    SMB_OP_WRITE = 0b10000000
    SMB_OP_MASK = 0b11000000

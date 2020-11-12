from smbus2 import SMBus
from termcolor import colored

SMBUS_REGS = {
    'Firmware version': {'address': 1, 'type': 'msp43xFwVersion', 'len' : 2},
    'Desired Digit': {'address': 2, 'type': int, 'len' : 1},
    'Current Digit': {'address': 3, 'type': int, 'len' : 1},
    'Sync trigger': {'address': 4, 'type': int, 'len' : 1},
    'Sync Threshold': {'address': 5, 'type': int, 'len' : 2},
    'Sync Digit': {'address': 6, 'type': int, 'len' : 1},
    'IR Threshold': {'address': 7, 'type': int, 'len' : 2},
    'IR turn-on': {'address': 8, 'type': int, 'len' : 2},
    'IR debounce': {'address': 9, 'type': int, 'len' : 2},
}

SMBUS_OPS = {
    'SMB_OP_NONE': 0b00000000,
    'SMB_OP_READ': 0b01000000,
    'SMB_OP_WRITE': 0b10000000,
    'SMB_OP_MASK': 0b11000000
}

SMBUS_ADDR = {
    0x16 : 'hh',
    0x17 : 'mm'
}

class SplitFlap:

    def __init__(self, i2cAddress, nFlaps, SMBusChannel=1):
        self.bus = SMBus(SMBusChannel)
        self.i2cAddress = i2cAddress
        self.nFlaps = nFlaps

    def read_register(self, key):
        data = self.bus.read_i2c_block_data(self.i2cAddress, SMBUS_REGS[key]['address'] + SMBUS_OPS['SMB_OP_READ'], SMBUS_REGS[key]['len'])
        return int.from_bytes(data, byteorder='little')

    def write_register(self, key, value):
        value_byte_array = value.to_bytes(SMBUS_REGS[key]['len'], byteorder='little')
        self.bus.write_i2c_block_data(self.i2cAddress, SMBUS_REGS[key]['address'] + SMBUS_OPS['SMB_OP_WRITE'], [b for b in value_byte_array])

    def readAllRegisters(self):
        print(colored('>> Reading all registers', 'magenta'))
        for reg in SMBUS_REGS:
            print('\t* ' + reg + ' = ' + self.show_reg(reg))
        return True

    def show_reg(self, reg):
        raw = self.read_register(reg)
        if SMBUS_REGS[reg]['type'] == int:
            return str(raw)
        if SMBUS_REGS[reg]['type'] == 'msp43xFwVersion':
            major = raw >> 8
            minor = raw & 0xFF
            return str(major) + '.' + str(minor)
        if isinstance(SMBUS_REGS[reg]['type'],dict):
            return SMBUS_REGS[reg]['type'][str(raw)]

    def getDigit(self):
        return self.read_register('Desired Digit')

    def setDigit(self, val):
        self.write_register('Desired Digit', val)

    def incDigit(self):
        val = self.getDigit()
        newval = val + 1
        if (newval >= self.nFlaps):
            newval = 0
        self.setDigit(newval)

    def getStatus(self):
        status = {}
        for reg in SMBUS_REGS:
            status[reg] = self.read_register(reg)
        return status

    def setParameter(self, parameter, value):
        print('[' + SMBUS_ADDR[self.i2cAddress] + '] Setting parameter \'' + parameter + '\' to \'' + str(value) + '\'')
        self.write_register(parameter, value)
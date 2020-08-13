import smbus
from flipclock_smbus_typedef import SMB_REGS, SMB_OPS

class msp430smbus:

    def __init__(self, SMBusChannel=1, i2cAddress=0x16):
        self.bus = smbus.SMBus(SMBusChannel)
        self.i2c_address = i2cAddress
        self.regs = SMB_REGS

    def read_register(self, reg):
        data = self.bus.read_i2c_block_data(self.i2c_address, reg.address + SMB_OPS.SMB_OP_READ.value, reg.len)
        reg.content = int.from_bytes(data, byteorder='little')

    def write_register(self, reg, value):
        value_byte_array = value.to_bytes(reg.len, byteorder='little')
        self.bus.write_i2c_block_data(self.i2c_address, reg.address + SMB_OPS.SMB_OP_WRITE.value, [b for b in value_byte_array])

    def get_fw_str(self):
        major = int(self.regs.SMB_FW_VERSION.content / 256)
        minor = self.regs.SMB_FW_VERSION.content - major * 256
        return (str(major) + '.' + str(minor))

    def get_hex_str(self, value, len=2):
        return '0x' + hex(value)[2:].zfill(len)

    def read_all(self):
        print('Read full content of MSP432-SMBUS... ', end = '')
        for r in self.regs:
            self.read_register(r)
        print('Done!')

    def print_report(self):
        print('______ MSP430-SMBUS SLAVE REPORT ______')
        print('[FW]\tv' + self.get_fw_str())
        print('[DESIRED DIGIT] ' + str(self.regs.SMB_DESIRED_DIGIT.content))
        print('[CURRENT DIGIT] ' + str(self.regs.SMB_CURRENT_DIGIT.content))
        print('[HALL FIND] ' + str(self.regs.SMB_HALL_FIND.content))
        print('[HALL THRESHOLD] ' + str(self.regs.SMB_HALL_THRESHOLD.content))
        print('[HALL DIGIT] ' + str(self.regs.SMB_HALL_DIGIT.content))
        print('[IR THRESHOLD] ' + str(self.regs.SMB_IR_THRESHOLD.content))
        print('[IR TURNON TIME] ' + str(self.regs.SMB_IR_TURNON_TIME.content))
        print('[IR DEBOUNCE TIME] ' + str(self.regs.SMB_IR_DEBOUNCE_TIME.content))
        print('----------------------------------------')


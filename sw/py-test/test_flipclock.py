#!/usr/bin/python3
import sys
from flipclock_smbus_typedef import SMB_REGS
from flipclock_smbus import msp430smbus
import time

def menu():
    print('----------------------------------------')
    print('1 - Read and report all registers')
    print('2 - Write  register HH')
    print('3 - Write  register MM')
    print('4 - Do Sync HH')
    print('5 - Do Sync MM')
    print('6 - Increment digit HH')
    print('7 - Increment digit MM')
    print('q - Quit')
    print('----------------------------------------')

def select_register():
    for r in SMB_REGS:
        print(str(r.value) + ' - ' + r.name)
    return int(input('Select register: '))

# Create instance of msp432smbus
hh_smbus=msp430smbus(i2cAddress=0x16)
mm_smbus=msp430smbus(i2cAddress=0x17)

flipclock_smbus=mm_smbus
i=0
# Loop on menu
run=True
while run:
    menu()
    option = input('Input: ')

    # Do option
    if(option is '1'):
        print('******* HH **********')
        hh_smbus.read_all()
        hh_smbus.print_report()
        print('******* MM **********')
        #mm_smbus.read_all()
        #mm_smbus.print_report()
    if (option is '2'):
        reg = hh_smbus.regs(select_register())
        if(reg.type is int):
            val = int(input('Set new value: '), 0)
        hh_smbus.write_register(reg, val)
    if (option is '3'):
        reg = mm_smbus.regs(select_register())
        if(reg.type is int):
            val = int(input('Set new value: '), 0)
        mm_smbus.write_register(reg, val)
    if (option is '4'):
        hh_smbus.write_register(hh_smbus.regs.SMB_HALL_FIND, 1)
    if (option is '5'):
        mm_smbus.write_register(mm_smbus.regs.SMB_HALL_FIND, 1)
    if (option is '6'):
        hh_smbus.read_register(hh_smbus.regs.SMB_DESIRED_DIGIT)
        newval = hh_smbus.regs.SMB_DESIRED_DIGIT.content + 1
        if (newval > 23):
            newval = 0
        hh_smbus.write_register(hh_smbus.regs.SMB_DESIRED_DIGIT, newval)
        print('New digit request: ' + str(newval))
    if (option is '7'):
        mm_smbus.read_register(mm_smbus.regs.SMB_DESIRED_DIGIT)
        newval = mm_smbus.regs.SMB_DESIRED_DIGIT.content + 1
        if (newval > 59):
            newval = 0
        mm_smbus.write_register(mm_smbus.regs.SMB_DESIRED_DIGIT, newval)
        print('New digit request: ' + str(newval))
    if (option is 'q'):
        run=False
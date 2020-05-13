#!/usr/bin/python3
import sys
from flipclock_smbus_typedef import SMB_REGS
from flipclock_smbus import msp430smbus

def menu():
    print('----------------------------------------')
    print('1 - Read and report all registers')
    print('2 - Read specific register')
    print('3 - Write specific register')
    print('q - Quit')
    print('----------------------------------------')

def select_register():
    for r in SMB_REGS:
        print(str(r.value) + ' - ' + r.name)
    return int(input('Select register: '))

# Create instance of msp432smbus
flipclock_smbus=msp430smbus()

# Loop on menu
run=True
while run:
    menu()
    option = input('Input: ')

    # Do option
    if(option is '1'):
        flipclock_smbus.read_all()
        flipclock_smbus.print_report()
    if (option is '2'):
        reg = flipclock_smbus.regs(select_register())
        flipclock_smbus.read_register(reg)
    if (option is '3'):
        reg = flipclock_smbus.regs(select_register())
        if(reg.type is int):
            val = int(input('Set new value: '), 0)
        flipclock_smbus.write_register(reg, val)
    if (option is 'q'):
        run=False
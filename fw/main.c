/*
 * main.c
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */

#include <msp430.h> 
#include <stdint.h>
#include "hal/mcu.h"
#include "hal/i2c-slave.h"
#include "hal/ir-sensor.h"
#include "hal/stepper.h"

// External flags
extern uint8_t fSystick;

int main(void)
{

    setup_mcu();
    setup_systick();
    setup_stepper();

    unlock_GPIOs();

    __bis_SR_register(GIE);

    while(1)
    {
        if (fSystick)
        {
            // Deassert flag
            fSystick=0;

            // Continuous stepper move for testing
            stepper_move();
        }
    }
}

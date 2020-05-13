/*
 * main.c
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */
#include <msp430.h> 
#include <typedefs.h>
#include <constants.h>
#include <drivers/mcu.h>
#include <drivers/smbus-slave.h>
#include <drivers/ir-sensor.h>
#include <drivers/stepper.h>
#include <drivers/adc.h>

#define VAR_DECLS
#include <global_variables.h>

int main(void)
{
    uint8_t current_digit_code = 0;

    setup_mcu();
    setup_systick();
    setup_stepper();
    setup_smbus_slave();

    init_smbus_slave(adc_get_role());

    unlock_GPIOs();

    __bis_SR_register(GIE);

    // Get ROLE with ADC

    while(1)
    {
        if (fSystick>0)
        {
            // Deassert flag
            fSystick=0;

            if (current_digit_code != reg_digit_code){
                // Continuous stepper move for testing
                stepper_move();
            }
        }
    }
}

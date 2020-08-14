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
#include <drivers/hall-sensor.h>
#include <drivers/ir-sensor.h>
#include <drivers/stepper.h>
#include <drivers/adc.h>

#define VAR_DECLS
#include <global_variables.h>

int main(void)
{
    setup_mcu();
    setup_stepper();
    setup_smbus_slave();
    setup_adc();
    setup_ir_sensor();

    unlock_GPIOs();

    __bis_SR_register(GIE);

    // Get ROLE with ADC
    adc_config_id();
    init_smbus_slave(adc_get_role());

    // Configure ADC for IR
    adc_config_ir();

    // Trigger a Sync as device just turned ON
    reg_hall_find=1;

    // Create systick
    setup_systick();

    while(1)
    {
        if (fSystick>0)
        {
            // Deassert flag
            fSystick=0;

            if(reg_hall_find != 0)
            {
                adc_meas_ir_n_hall();
                if(hall_sense())
                {
                    reg_hall_find=0;
                    reg_current_digit = reg_hall_digit;
                }else{
                    stepper_move();
                }
            }else{
                // Do normal function
                if(reg_current_digit != reg_desired_digit)
                {
                    // Check if IR is ON
                    if(!ir_is_on())
                    {
                        ir_power_on();
                    }else{
                        adc_meas_ir_n_hall();

                        // Check if IR detected
                        if(ir_sense())
                        {
                            reg_current_digit++;
                            if(reg_current_digit >= reg_max_digit)
                            {
                                reg_current_digit = 0;
                            }
                        }else{
                            if(!ir_is_debounce())
                            {
                                stepper_move();
                            }
                        }

                        // Check if HALL detected
                        if(hall_sense())
                        {
                            reg_current_digit = reg_hall_digit;
                        }

                    }
                }else{
                    ir_power_off();
                    stepper_stop();
                }
            }
        }
    }
}

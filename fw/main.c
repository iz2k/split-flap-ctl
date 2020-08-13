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
    setup_systick();
    setup_stepper();
    setup_smbus_slave();
    setup_adc();
    setup_ir_sensor();

    unlock_GPIOs();

    __bis_SR_register(GIE);

    // Get ROLE with ADC
    adc_config_id();
    //init_smbus_slave(adc_get_role());
    init_smbus_slave(ROLE_HOURS);

    // Configure ADC for IR
    adc_config_ir();

    // Trigger a Sync as deivce just turned ON
    reg_find_sync=1;

    while(1)
    {
        if (fSystick>0)
        {
            // Deassert flag
            fSystick=0;

            if(reg_find_sync != 0)
            {
                adc_meas_ir_n_hall();
                if(hall_sense())
                {
                    reg_find_sync=0;
                    stepper_stop();
                }else{
                    stepper_move();
                }
            }else{
                // Do normal function
            }
/*
            if (reg_current_digit != reg_digit_code){
                if(ir_is_on()==false)
                {
                    ir_power_on();
                }else{
                    stepper_move();
                    // End of detection
                    if(ir_sense())
                    {
                        //if (flap_detected)
                            reg_current_digit++;
                    }
                }
            }else{
                stepper_stop();
                ir_power_off();
            }*/
        }
    }
}

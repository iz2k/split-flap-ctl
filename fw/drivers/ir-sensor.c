/*
 * ir-sensor.c
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <typedefs.h>
#include <constants.h>
#include <global_variables.h>
#include <drivers/ir-sensor.h>
#include <drivers/filter.h>

ir_sensor_state ir_status;
uint16_t turnon_counter;
uint16_t debounce_counter;

float ir_filter;

void setup_ir_sensor()
{
    P2DIR |= BIT6;
    P2OUT &= ~(BIT6);

    ir_power_off();
}

void ir_power_on()
{
    if(turnon_counter++ >= reg_ir_turnon_time/reg_systick_period)
    {
        ir_status = IR_STATE_ON;
        ir_filter = 0;
        // Enable IR sensor
        P2OUT |= BIT6;
    }
}

void ir_power_off()
{
    ir_status = IR_STATE_OFF;
    turnon_counter=0;
    debounce_counter=0;
    // Disable IR sensor
    P2OUT &= ~BIT6;
}


bool ir_is_on()
{
    if (ir_status==IR_STATE_OFF)
    {
        return false;
    }else{
        return true;
    }
}

bool ir_is_debounce()
{
    if (ir_status==IR_STATE_DEBOUNCE)
    {
        return true;
    }else{
        return false;
    }
}

bool ir_sense()
{
    // Add new value to filter
    ir_filter = filter(ir_filter, ir_val, 0.5);

    switch(ir_status)
    {
    case IR_STATE_ON:
        if(ir_filter > reg_ir_threshold)
        {
            ir_status = IR_STATE_DEBOUNCE;
            return true;
        }
        break;
    case IR_STATE_DEBOUNCE:
        if(debounce_counter++ >= reg_ir_debounce_time/reg_systick_period)
        {
            ir_status = IR_STATE_ON;
            debounce_counter=0;
        }
        break;
    }

    return false;
}


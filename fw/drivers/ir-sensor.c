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
#include <drivers/adc.h>

ir_sensor_state ir_status;
uint16_t turnon_counter;
uint16_t debounce_counter;
uint16_t dephase_counter;
float slow_flapfilter, fast_flapfilter;
float slow_syncfilter, fast_syncfilter;
float flap_filter_dif, sync_filter_dif;


void setup_ir_sensor()
{
    P2DIR |= BIT6 | BIT7;
    P2OUT &= ~(BIT6 | BIT7);

    ir_status = IR_STATE_OFF;
    turnon_counter=0;
}

void ir_flap_enable()
{
    P2OUT |= BIT6;
}

void ir_flap_disable()
{
    P2OUT &= ~BIT6;
}

void ir_sync_enable()
{
    P2OUT |= BIT7;
}

void ir_sync_disable()
{
    P2OUT &= ~BIT7;
}

void ir_power_on()
{
    P1OUT |= BIT7;
    // Switch ON IR LEDs
    ir_flap_enable();
    turnon_counter++;
    // Wait for turnon time
    if(turnon_counter==reg_turnon_time)
    {
        // Reset counter for future powerups
        turnon_counter=0;

        // Change status
        ir_status = IR_STATE_CAL;
        P1OUT &= ~BIT7;
    }
}

void ir_power_off()
{
    ir_flap_disable();
    ir_status = IR_STATE_OFF;
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

bool ir_sense()
{
    switch(ir_status)
    {
    case IR_STATE_CAL:
        // Get initial measurements for reference
        adc_meas_ir();
        slow_flapfilter=flap_val;
        fast_flapfilter=flap_val;
        slow_syncfilter=sync_val;
        fast_syncfilter=sync_val;

        // Reset detection flags
        flap_detected=false;
        sync_detected=false;

        // Reset counters
        dephase_counter=0;
        debounce_counter=0;

        // Change state
        ir_status = IR_STATE_ON;
        break;
    case IR_STATE_ON:
        // Get new values
        adc_meas_ir();

        // Do filter
        slow_flapfilter = filter(slow_flapfilter, flap_val, 0.01);
        fast_flapfilter = filter(fast_flapfilter, flap_val, 0.5);
        slow_syncfilter = filter(slow_syncfilter, sync_val, 0.01);
        fast_syncfilter = filter(fast_syncfilter, sync_val, 0.5);

        // Update difs
        flap_filter_dif = fast_flapfilter - slow_flapfilter;
        if (flap_filter_dif<0) flap_filter_dif=-flap_filter_dif;
        sync_filter_dif = fast_syncfilter - slow_syncfilter;
        if (sync_filter_dif<0) sync_filter_dif=-sync_filter_dif;

        // Detect event
        if(flap_filter_dif>reg_ir_threshold_flap) flap_detected=true;
        if(sync_filter_dif>reg_ir_threshold_sync) sync_detected=true;

        flap_detected=false;
        // Check event
        if(flap_detected || sync_detected)
        {
            // Wait for dephased detection
            if(dephase_counter++>reg_dephase_time){
                // Go to debounce when detected
                ir_status = IR_STATE_DEBOUNCE;
                P1OUT |= BIT7;

                // Notify about end of detection
                return true;
            }
        }
        break;
    case IR_STATE_DEBOUNCE:
        debounce_counter++;
        if(debounce_counter==reg_debounce_time)
        {
            ir_status = IR_STATE_CAL;
            P1OUT &= ~BIT7;
        }
        break;
    default:
        break;
    }

    // Detection in curse yet
    return false;

}

float filter(float oldval, float newval, float speed)
{
    return (1-speed)*oldval + speed*newval;
}


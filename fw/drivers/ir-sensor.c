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

ir_sensor_state status;
uint16_t floor_flapval, floor_syncval;
int32_t integral_flapval, integral_syncval;
uint8_t debounce_counter;
uint8_t dephase_counter;
uint8_t turn_on_counter;
float slow_flapfilter, fast_flapfilter;

void setup_ir_sensor()
{
    P2DIR |= BIT6 | BIT7;
    P2OUT &= ~(BIT6 | BIT7);

    status = IR_STATE_OFF;
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

void ir_start_sensing()
{
    ir_flap_enable();
    ir_sync_enable();

    status = IR_STATE_TURN_ON;
    turn_on_counter=0;

    // Reset integrals to 0
    integral_flapval=0;
    integral_syncval=0;
    slow_flapfilter=0;

    // Reset detection flags
    flap_detected=false;
    sync_detected=false;

    // Reset counters
    dephase_counter=0;
    debounce_counter=0;
}

void ir_stop_sensing()
{
    ir_flap_disable();
    ir_sync_disable();
}

void ir_systick()
{
   if(status == IR_STATE_DEBOUNCE)
   {
       debounce_counter++;
       if(debounce_counter==reg_debounce_time)
       {
           status = IR_STATE_OFF;
       }
   }
}

bool ir_sense()
{
    switch(status)
    {
    case IR_STATE_OFF:
        // Discard ADC data and switch IR sensor ON
        ir_start_sensing();
        break;
    case IR_STATE_TURN_ON:
        adc_meas_ir();
        // Switch IR sensor ON
        if(turn_on_counter++>5)
        {
            status = IR_STATE_CAL;
        }
        break;
    case IR_STATE_CAL:
        adc_meas_ir();
        // Set ADC data as floor
        floor_flapval=flap_val;
        floor_syncval=sync_val;
        slow_flapfilter=flap_val;
        status = IR_STATE_ON;
        break;
    case IR_STATE_ON:
        adc_meas_ir();
        // Integrate
        //integral_flapval += ((int16_t) flap_val - (int16_t) floor_flapval);
        //integral_syncval += ((int16_t) sync_val - (int16_t) floor_syncval);
        // Detect each sensor
        //if (integral_flapval > reg_ir_threshold_flap) flap_detected= true;
        //if (integral_syncval > reg_ir_threshold_sync) sync_detected= true;
        // Filter
        slow_flapfilter = filter(slow_flapfilter, flap_val, 0.01);
        fast_flapfilter = filter(fast_flapfilter, flap_val, 0.5);
        // Detect each sensor
        if (fast_flapfilter > slow_flapfilter + reg_ir_threshold_flap) flap_detected= true;
        if(flap_detected || sync_detected)
        {
            // Wait for dephased detection
            if(dephase_counter++>reg_dephase_time){
                // Go to debounce when detected
                status = IR_STATE_DEBOUNCE;
                // Notify about end of detection
                return true;
            }
        }
        break;
    case IR_STATE_DEBOUNCE:
        // Do nothing
        break;
    }

    // Detection in curse yet
    return false;

}

bool ir_sensor_ready()
{
    switch(status)
    {
    case IR_STATE_OFF:
    case IR_STATE_CAL:
        return false;
    case IR_STATE_ON:
    case IR_STATE_DEBOUNCE:
        return true;
    }
}

float filter(float oldval, float newval, float speed)
{
    return (1-speed)*oldval + speed*newval;
}

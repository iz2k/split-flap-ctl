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

#define VECTOR_LENGTH   2
ir_sensor_state status;
uint16_t flapval[VECTOR_LENGTH], syncval[VECTOR_LENGTH];
uint8_t debounce_counter;
uint8_t dephase_counter;
float slow_flapfilter, fast_flapfilter;
float slow_syncfilter, fast_syncfilter;
float flap_filter_dif, sync_filter_dif;

float maxdif=0;

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
    status = IR_STATE_ON;

    // Switch ON IR LEDs
    ir_flap_enable();
    ir_sync_enable();

    // Reset detection flags
    flap_detected=false;
    sync_detected=false;

    // Reset counters
    dephase_counter=0;
    debounce_counter=0;

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
    uint8_t i;

    switch(status)
    {
    case IR_STATE_OFF:
        // Discard ADC data and switch IR sensor ON
        ir_start_sensing();
        break;
    case IR_STATE_CAL:
        // Get value
        adc_meas_ir();
        // Initialize vector with first value
        for(i=0;i<VECTOR_LENGTH;i++)
        {
            flapval[i]=flap_val;
            syncval[i]=sync_val;
        }
        slow_flapfilter=flap_val;
        fast_flapfilter=flap_val;
        slow_syncfilter=sync_val;
        fast_syncfilter=sync_val;
        status = IR_STATE_ON;
        break;
    case IR_STATE_ON:
        // Shift values
        for(i=0;i<VECTOR_LENGTH-1;i++)
        {
            flapval[i]=flapval[i+1];
            syncval[i]=syncval[i+1];
        }
        // Get new values
        adc_meas_ir();
        flapval[VECTOR_LENGTH-1]=flap_val;
        syncval[VECTOR_LENGTH-1]=sync_val;
        // Do filter
        slow_flapfilter = filter(slow_flapfilter, flap_val, 0.01);
        fast_flapfilter = filter(fast_flapfilter, flap_val, 0.5);
        slow_syncfilter = filter(slow_syncfilter, flap_val, 0.01);
        fast_syncfilter = filter(fast_syncfilter, flap_val, 0.5);

        // Update difs
        flap_filter_dif = fast_flapfilter - slow_flapfilter;
        if (flap_filter_dif<0) flap_filter_dif=-flap_filter_dif;
        sync_filter_dif = fast_syncfilter - slow_syncfilter;
        if (sync_filter_dif<0) sync_filter_dif=-sync_filter_dif;

        if(flap_filter_dif>maxdif) maxdif=flap_filter_dif;

        if(flap_filter_dif>reg_ir_threshold_flap) flap_detected=true;
        if(sync_filter_dif>reg_ir_threshold_sync) flap_detected=true;

        // Detect event
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

float filter(float oldval, float newval, float speed)
{
    return (1-speed)*oldval + speed*newval;
}


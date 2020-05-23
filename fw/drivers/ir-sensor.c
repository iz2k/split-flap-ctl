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
uint16_t ir_flapval, ir_syncval;
int16_t flapdif, syncdif;
uint8_t debounce_counter;
uint8_t dephase_counter;
uint8_t ac_counter;

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

    // Reset detection flags
    flap_detected=false;
    sync_detected=false;

    // Reset counters
    dephase_counter=0;
    debounce_counter=0;

    ac_counter=0;
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
    case IR_STATE_ON:
        // Switch ON IR LEDs
        ir_flap_enable();
        ir_sync_enable();
        // Wait until LED is ON
        __delay_cycles(4000);
        // Get
        adc_meas_ir();
        ir_flapval = flap_val;
        ir_syncval = sync_val;
        // Switch OFF IR LEDs
        ir_flap_disable();
        ir_sync_disable();
        // Wait until LED is OFF
        __delay_cycles(4000);
        // Get floors
        adc_meas_ir();
        floor_flapval = flap_val;
        floor_syncval = sync_val;
        // Get difference
        flapdif += ir_flapval - floor_flapval;
        syncdif += ir_syncval - floor_syncval;
        // Detect each sensor
        /*if (fast_flapfilter > slow_flapfilter + reg_ir_threshold_flap) flap_detected= true;
        if(flap_detected || sync_detected)
        {
            // Wait for dephased detection
            if(dephase_counter++>reg_dephase_time){
                // Go to debounce when detected
                status = IR_STATE_DEBOUNCE;
                // Notify about end of detection
                return true;
            }
        }*/
        ac_counter++;
        if(ac_counter>=20)
        {
            ac_counter=0;
            flapdif = 0;
            syncdif=0;
        }
        break;
    case IR_STATE_DEBOUNCE:
        // Do nothing
        break;
    }

    // Detection in curse yet
    return false;

}

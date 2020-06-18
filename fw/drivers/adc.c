/*
 * adc.c
 *
 *  Created on: 8 may. 2020
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <typedefs.h>
#include <constants.h>
#include <global_variables.h>
#include <drivers/adc.h>

void setup_adc()
{
    // Configure ADC A1 pin
    //P1SEL0 |= BIT0 + BIT1 + BIT7;
    //P1SEL1 |= BIT0 + BIT1 + BIT7;
    P1SEL0 |= BIT0 + BIT1;
    P1SEL1 |= BIT0 + BIT1;
}

void adc_config_id()
{
    // Configure ADC10
    ADCCTL0 &= ~ADCENC;                                     // Reset configuration
    ADCCTL0 = ADCSHT_2 | ADCON;                             // ADCON, S&H=16 ADC clks
    ADCCTL1 = ADCSHP;                                       // ADCCLK = MODOSC; sampling timer
    ADCCTL2 = ADCRES;                                       // 10-bit conversion results
    ADCMCTL0 = ADCINCH_7;                                   // A1 ADC input select; Vref=AVCC
}

void adc_config_ir()
{
    // Configure ADC10
    ADCCTL0 &= ~ADCENC;                                     // Reset configuration
    ADCCTL0 = ADCSHT_0 | ADCMSC | ADCON;                    // 16ADCclks, MSC, ADC ON
    ADCCTL1 = ADCSHP | ADCCONSEQ_1;                         // ADCCLK = MODOSC; sampling timer, single sequence
    ADCCTL2 = ADCRES;                                       // 10-bit conversion results
    ADCMCTL0 = ADCINCH_1;                                   // A0~1(EoS);
}

uint16_t adc_meas_id()
{
    // Wait if ADC core is active
    while(ADCCTL1 & ADCBUSY);
    // Sampling and conversion start
    ADCCTL0 |= ADCENC | ADCSC;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update ADC values
    return ADCMEM0;
}

void adc_meas_ir(){
    // Wait if ADC core is active
    while(ADCCTL1 & ADCBUSY);
    // Sampling and conversion start
    ADCCTL0 |= ADCENC | ADCSC;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update ADC values
    flap_val = ADCMEM0;
    // Wait until ADC measurement has been done
    while(!(ADCIFG & ADCIFG0));
    // Update ADC values
    sync_val = ADCMEM0;
}

split_flap_role adc_get_role()
{
    uint16_t id_val = adc_meas_id();
    if(id_val > 900)
        return ROLE_HOURS;
    if(id_val <= 900 && id_val > 100)
        return ROLE_MINUTES;
    if(id_val <= 100)
        return ROLE_WEATHER;
    return ROLE_ERROR;
}

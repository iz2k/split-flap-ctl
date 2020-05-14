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

void setup_ir_sensor()
{
    P2DIR |= BIT6 | BIT7;
    P2OUT &= ~(BIT6 | BIT7);
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

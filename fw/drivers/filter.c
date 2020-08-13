/*
 * filter.c
 *
 *  Created on: 13 ago. 2020
 *      Author: Ibon Zalbide
 */
#include <msp430.h>
#include <typedefs.h>

float filter(float oldval, float newval, float speed)
{
    return (1-speed)*oldval + speed*newval;
}

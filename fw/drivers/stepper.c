/*
 * stepper.c
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */
#include <drivers/stepper.h>
#include <msp430.h>
#include <stdint.h>

const uint8_t stepmtx [8][4] =
{
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1}
};

uint8_t iStp=0;

void setup_stepper()
{
    // Set stepper control pins as output
    STP_1_PDIR |= STP_1_BIT;
    STP_2_PDIR |= STP_2_BIT;
    STP_3_PDIR |= STP_3_BIT;
    STP_4_PDIR |= STP_4_BIT;

    // Set initial value to 0
    STP_1_POUT &= ~ STP_1_BIT;
    STP_2_POUT &= ~ STP_2_BIT;
    STP_3_POUT &= ~ STP_3_BIT;
    STP_4_POUT &= ~ STP_4_BIT;
}

void stepper_move()
{
    stepmtx[iStp][0] ? (STP_1_POUT |= STP_1_BIT) : (STP_1_POUT &= ~ STP_1_BIT);
    stepmtx[iStp][1] ? (STP_2_POUT |= STP_2_BIT) : (STP_2_POUT &= ~ STP_2_BIT);
    stepmtx[iStp][2] ? (STP_3_POUT |= STP_3_BIT) : (STP_3_POUT &= ~ STP_3_BIT);
    stepmtx[iStp][3] ? (STP_4_POUT |= STP_4_BIT) : (STP_4_POUT &= ~ STP_4_BIT);
    if(--iStp>7)iStp=7;
}

void stepper_stop()
{
    // Set signaling to 0
    STP_1_POUT &= ~ STP_1_BIT;
    STP_2_POUT &= ~ STP_2_BIT;
    STP_3_POUT &= ~ STP_3_BIT;
    STP_4_POUT &= ~ STP_4_BIT;
}

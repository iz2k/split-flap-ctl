/*
 * stepper.h
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */

#ifndef HAL_STEPPER_H_
#define HAL_STEPPER_H_

// STEPPER  CTL1:P2.0, CTL2:P1.6, CTL3:P1.5, CTL4:P1.4
#define STP_1_PDIR  P2DIR
#define STP_1_POUT  P2OUT
#define STP_1_BIT   BIT0

#define STP_2_PDIR  P1DIR
#define STP_2_POUT  P1OUT
#define STP_2_BIT   BIT6

#define STP_3_PDIR  P1DIR
#define STP_3_POUT  P1OUT
#define STP_3_BIT   BIT5

#define STP_4_PDIR  P1DIR
#define STP_4_POUT  P1OUT
#define STP_4_BIT   BIT4

void setup_stepper();
void stepper_move();
void stepper_stop();

#endif /* HAL_STEPPER_H_ */

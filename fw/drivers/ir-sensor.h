/*
 * ir-sensor.h
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */

#ifndef DRIVERS_IR_SENSOR_H_
#define DRIVERS_IR_SENSOR_H_


void setup_ir_sensor();

void ir_flap_enable();
void ir_flap_disable();
void ir_sync_enable();
void ir_sync_disable();
bool ir_sense();
void ir_systick();
void ir_stop_sensing();
void ir_start_sensing();

#endif /* DRIVERS_IR_SENSOR_H_ */

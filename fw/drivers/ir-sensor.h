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

void ir_power_on();
void ir_power_off();
bool ir_is_on();
bool ir_is_debounce();



bool ir_sense();
void ir_systick();
void ir_stop_sensing();
void ir_start_sensing();
bool ir_sensor_ready();
float filter(float oldval, float newval, float speed);

#endif /* DRIVERS_IR_SENSOR_H_ */

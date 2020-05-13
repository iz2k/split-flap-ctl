/*
 * adc.h
 *
 *  Created on: 8 may. 2020
 *      Author: IbonZalbide
 */

#ifndef DRIVERS_ADC_H_
#define DRIVERS_ADC_H_

#include <typedefs.h>

void setup_adc();
void adc_config_id();
void adc_config_ir();
uint16_t adc_meas_id();
void adc_meas_ir();
split_flap_role adc_get_role();

#endif /* DRIVERS_ADC_H_ */

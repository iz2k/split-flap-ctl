/*
 * i2c-slave.h
 *
 *  Created on: 24 abr. 2020
 *      Author: IbonZalbide
 */

#ifndef DRIVERS_SMBUS_SLAVE_H_
#define DRIVERS_SMBUS_SLAVE_H_


#include <typedefs.h>

void setup_smbus_slave();
void init_smbus_slave(split_flap_role role);

void I2C_Slave_ProcessCMD(uint8_t cmd);
void I2C_Slave_TransactionDone(uint8_t cmd);
void CopyArray(uint8_t *source, uint8_t *dest, uint8_t count);

uint8_t *get_reg_pointer(smbus_registers address);
uint8_t get_reg_len(smbus_registers address);



#endif /* DRIVERS_SMBUS_SLAVE_H_ */

#ifndef TYPEDEFS_H_
#define TYPEDEFS_H_

#include "stdint.h"

typedef enum {
    false, true
}bool;

typedef enum {
    ROLE_HOURS      = 0,
    ROLE_MINUTES    = 1,
    ROLE_WEATHER    = 2
} split_flap_role;

typedef enum {
    SMB_NONE            = 0,
    SMB_FW_VERSION      = 1,
    SMB_DIGIT_CODE      = 2,
    SMB_IR_THRESHOLD    = 3
} smbus_registers;

typedef enum{
    SMB_OP_NONE     = 0b00000000,
    SMB_OP_READ     = 0b01000000,
    SMB_OP_WRITE    = 0b10000000,
    SMB_OP_MASK     = 0b11000000
} smbus_operation;

typedef enum I2C_ModeEnum{
    IDLE_MODE,
    NACK_MODE,
    TX_REG_ADDRESS_MODE,
    RX_REG_ADDRESS_MODE,
    TX_DATA_MODE,
    RX_DATA_MODE,
    SWITCH_TO_RX_MODE,
    SWITHC_TO_TX_MODE,
    TIMEOUT_MODE
} I2C_Mode;

#endif /* TYPEDEFS_H_ */

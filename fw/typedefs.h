#ifndef TYPEDEFS_H_
#define TYPEDEFS_H_

#include "stdint.h"

typedef enum {
    false, true
}bool;

typedef enum {
    ROLE_HOURS      = 0,
    ROLE_MINUTES    = 1,
    ROLE_WEATHER    = 2,
    ROLE_ERROR      = 255
} split_flap_role;

typedef enum {
    IR_STATE_OFF        = 0,
    IR_STATE_TURN_ON    = 1,
    IR_STATE_CAL        = 2,
    IR_STATE_ON         = 3,
    IR_STATE_DEBOUNCE   = 4
} ir_sensor_state;

typedef enum {
    SMB_NONE                = 0,
    SMB_FW_VERSION          = 1,
    SMB_DIGIT_CODE          = 2,
    SMB_IR_THRESHOLD_FLAP   = 3,
    SMB_IR_THRESHOLD_SYNC   = 4,
    SMB_TURNON_TIME         = 5,
    SMB_DEBOUNCE_TIME       = 6,
    SMB_DEPHASE_TIME        = 7,
    SMB_CURRENT_DIGIT       = 8,
    SMB_CURRENT_SYNC        = 9,
    SMB_FIND_SYNC           = 10
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

/*----------------------------------------------------------------------------
global_variables.h

Note: #define VAR_DECLS 1 before including this file to DECLARE and INITIALIZE
global variables.  Include this file without defining VAR_DECLS to extern
these variables.
----------------------------------------------------------------------------*/

#include "typedefs.h"


#ifndef VAR_DEFS          // Make sure this file is included only once
#define VAR_DEFS 1

/*----------------------------------------------
Setup variable declaration macros.
----------------------------------------------*/
#ifndef VAR_DECLS
# define _DECL extern
# define _INIT(x)
#else
# define _DECL
# define _INIT(x)  = x
#endif

/*----------------------------------------------
Declare variables as follows:

_DECL [standard variable declaration] _INIT(x);

where x is the value with which to initialize
the variable.  If there is no initial value for
the variable, it may be declared as follows:

_DECL [standard variable declaration];
----------------------------------------------*/

// TIMER generated SysTick flag
_DECL uint8_t fSystick  _INIT(0);

// SMBUS VOLATILE REGISTERS

_DECL const uint16_t  reg_fw_version    _INIT(0x0106);
_DECL uint16_t  reg_ir_threshold        _INIT(0);
_DECL uint8_t  reg_digit_code          _INIT(0);
// SMBUS FLAGS
_DECL smbus_registers  smbus_reg  _INIT(SMB_NONE);
_DECL smbus_operation  smbus_op   _INIT(SMB_OP_NONE);

#endif
/*----------------------------------------------------------------------------
----------------------------------------------------------------------------*/

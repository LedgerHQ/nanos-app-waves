#ifndef __UI_MENUS_BUTTONS_H__X
#define __UI_MENUS_BUTTONS_H__X

#include "os.h"
#include "cx.h"

#if defined(TARGET_NANOX)
unsigned int ui_verify_transfer_nanos_button(unsigned int button_mask, unsigned int button_mask_counter);
unsigned int ui_verify_transaction_nanos_button(unsigned int button_mask, unsigned int button_mask_counter);
unsigned int ui_address_nanos_button(unsigned int button_mask, unsigned int button_mask_counter);
#endif

#endif
#ifndef _TAMA_HAL_
#define _TAMA_HAL_

#include "lib/hw.h"
#include "lib/hal.h"

static uint16_t current_freq = 0;
static uint16_t play_freq = 0; 
static bool_t matrix_buffer[LCD_HEIGHT][LCD_WIDTH/8] = {{0}};
static bool_t icon_buffer[ICON_NUM] = {0};
static bool_t button_buffer[4];

static hal_t hal;

#endif
#include <chrono> // high resolution clock
#include <thread> // sleep_for
#include "hal_types.h"
#include "lib/hw.h"
#include "lib/hal.h"
#include "hal2.h"

static const auto epochTime = std::chrono::system_clock::from_time_t(0);

static void hal_malloc(u32_t size) {
}

static void hal_free(void *ptr) {
}

static void hal_halt(void) {
}

static bool_t hal_is_log_enabled(){
  return 0;
}

static void hal_log(log_level_t level, char *buff, ...) {
}

static void hal_update_screen(void) {
}


static timestamp_t hal_get_timestamp(void) {
  auto currentTime = std::chrono::system_clock::now();
  auto usec = std::chrono::duration_cast<std::chrono::microseconds>(currentTime - epochTime);
  timestamp_t t_usec = usec.count();
  return  t_usec ;
}

static void hal_sleep_until(timestamp_t ts) {
  int32_t diff_usec = (int32_t) (ts - hal_get_timestamp());
  if (diff_usec > 0) {
    std::this_thread::sleep_for(std::chrono::microseconds(diff_usec));
  }
}

static void hal_play_frequency(bool_t en) {
  if(en){
    play_freq = current_freq;
  } else{
    play_freq = 0;
  }
}

static void hal_set_lcd_matrix(u8_t x, u8_t y, bool_t val)
{
	matrix_buffer[y][x] = val;
}

static void hal_set_lcd_icon(u8_t icon, bool_t val)
{
	icon_buffer[icon] = val;
}

static void hal_set_frequency(u32_t freq)
{
	if (current_freq != freq) {
		current_freq = freq;
	}
}

static int hal_handler(void) {
  if (button_buffer[0] != 0) {
    hw_set_button(BTN_LEFT, BTN_STATE_PRESSED );
  } else {
    hw_set_button(BTN_LEFT, BTN_STATE_RELEASED );
  }
  if (button_buffer[1] != 0) {
    hw_set_button(BTN_MIDDLE, BTN_STATE_PRESSED );
  } else {
    hw_set_button(BTN_MIDDLE, BTN_STATE_RELEASED );
  }
  if (button_buffer[2] != 0) {
    hw_set_button(BTN_RIGHT, BTN_STATE_PRESSED );
  } else {
    hw_set_button(BTN_RIGHT, BTN_STATE_RELEASED );
  }
  if (button_buffer[3] != 0) {
    hw_set_button(BTN_RIGHT, BTN_STATE_PRESSED );
  } else {
    hw_set_button(BTN_RIGHT, BTN_STATE_RELEASED );
  }
  return 0;
}

static hal_t hal = {
	.malloc = &hal_malloc,
	.free = &hal_free,
	.halt = &hal_halt,
	.is_log_enabled = &hal_is_log_enabled,
	.log = &hal_log,
	.sleep_until = &hal_sleep_until,
	.get_timestamp = &hal_get_timestamp,
	.update_screen = &hal_update_screen,
	.set_lcd_matrix = &hal_set_lcd_matrix,
	.set_lcd_icon = &hal_set_lcd_icon,
	.set_frequency = &hal_set_frequency,
	.play_frequency = &hal_play_frequency,
	.handler = &hal_handler,
};


#ifndef _TAMALIB_H_
#define _TAMALIB_H_

#include <stdint.h> // uint8_t etc
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

#include "hal_types.h"
#include "lib/hal.h"
#include "lib/hw.h"
#include "lib/cpu.h"

#define BUTTON_NUM 3

bool_t hw_init(void);
void hw_set_lcd_pin(u8_t seg, u8_t com, u8_t val);
void hw_set_button(button_t btn, btn_state_t state);
void hw_set_buzzer_freq(u4_t freq);
void hw_enable_buzzer(bool_t en);
bool_t tamalib_init(u32_t freq);
void tamalib_set_framerate(u8_t framerate);
void tamalib_register_hal(hal_t *hal);
void tamalib_mainloop_step_by_step(void);
void cpu_get_state(cpu_state_t *cpustate);
void cpu_set_state(cpu_state_t *cpustate);
u32_t cpu_get_depth(void);
void cpu_set_input_pin(pin_t pin, pin_state_t state);
void cpu_sync_ref_timestamp(void);
void cpu_refresh_hw(void);
void cpu_reset(void);
bool_t cpu_init(u32_t freq);
int cpu_step(void);
typedef enum {
    EXEC_MODE_PAUSE,
    EXEC_MODE_RUN,
    EXEC_MODE_STEP,
    EXEC_MODE_NEXT,
    EXEC_MODE_TO_CALL,
    EXEC_MODE_TO_RET,
  } exec_mode_t;

static exec_mode_t exec_mode = EXEC_MODE_RUN;
static u32_t step_depth = 0;
static u32_t ts_freq;
hal_t *g_hal;
static uint16_t current_freq = 0;
static uint16_t play_freq = 0; 
static bool_t matrix_buffer[LCD_HEIGHT][LCD_WIDTH/8] = {{0}};
static bool_t icon_buffer[ICON_NUM] = {0};
static cpu_state_t cpuState;
static bool_t button_buffer[BUTTON_NUM];
static bool keep_going = false;

class Tama {
public:

  // Constructor
  Tama();

  // Getters
  std::vector<bool> GetIcons();
  std::vector<std::vector<bool>> GetMatrix();
  int GetFreq();
  std::vector<bool> GetButton();
  std::vector<int> GetCPU();
  std::vector<int> GetROM();

  // Setters
  void SetButton(int n, bool state);
  void SetCPU(const std::vector<int> res);
  void SetROM(const std::vector<int> rom);

  // public methods
  bool Runs();
  void Start();
  void Stop();

private: 
};

#endif
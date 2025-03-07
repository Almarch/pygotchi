#include <pthread.h>
#include <thread> // sleep_for
#include <chrono> // high resolution clock
#include <cstring> // memcpy
#include <stdlib.h> // exit

#include "hal_types.h"
#include "lib/hal.h"
#include "lib/hw.h"
#include "lib/cpu.h"
#include "tamalib.h"

// ROM
static unsigned char g_program[12288];

// time
static const auto epochTime = std::chrono::high_resolution_clock::from_time_t(0);

// handlers
static void hal_set_lcd_matrix(u8_t x, u8_t y, bool_t val) {
    uint8_t mask;
    int i;
    if (val) {
        mask = 0b10000000 >> (x % 8);
        matrix_buffer[y][x/8] = matrix_buffer[y][x/8] | mask;   
    } else { 
        mask = 0b01111111;
        for(i=0;i<(x % 8);i++) {
            mask = (mask >> 1) | 0b10000000;
        }
        matrix_buffer[y][x/8] = matrix_buffer[y][x/8] & mask;  
    }
}

static void hal_set_lcd_icon(u8_t icon, bool_t val) {
    icon_buffer[icon] = val;
}

static void hal_set_frequency(u32_t freq) {
    current_freq = freq;
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
  return 0;
}

static void hal_log(log_level_t level, char *buff, ...) {
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

static hal_t hal = {
  .log = &hal_log,
  .sleep_until = &hal_sleep_until,
  .get_timestamp = &hal_get_timestamp,
  .set_lcd_matrix = &hal_set_lcd_matrix,
  .set_lcd_icon = &hal_set_lcd_icon,
  .set_frequency = &hal_set_frequency,
  .play_frequency = &hal_play_frequency,
  .handler = &hal_handler,
};

bool_t tamalib_init(u32_t freq)
//bool_t tamalib_init(breakpoint_t *breakpoints, u32_t freq)
{
  bool_t res = 0;
  res |= cpu_init( freq);

//  res |= cpu_init(program, breakpoints, freq);
  res |= hw_init();

  ts_freq = freq;

  return res;
}

void tamalib_register_hal(hal_t *hal)
{
  g_hal = hal;
}

void tamalib_mainloop_step_by_step(void)
{
  if (!g_hal->handler()) {
    //tamalib_step();

    if (exec_mode == EXEC_MODE_RUN) {
      if (cpu_step()) {
        exec_mode = EXEC_MODE_PAUSE;
        step_depth = cpu_get_depth();
      }
    }
  }
}

void* tamalib_mainloop(void* nada){
  while(keep_going){
    tamalib_mainloop_step_by_step();
  };
  return nada;
}

bool_t hw_init(void)
{
  /* Buttons are active LOW */
  cpu_set_input_pin(PIN_K00, PIN_STATE_HIGH);
  cpu_set_input_pin(PIN_K01, PIN_STATE_HIGH);
  cpu_set_input_pin(PIN_K02, PIN_STATE_HIGH);
  return 0;
}

void hw_set_lcd_pin(u8_t seg, u8_t com, u8_t val)
{
  if (seg_pos[seg] < LCD_WIDTH) {
    g_hal->set_lcd_matrix(seg_pos[seg], com, val);
  } else {
    if (seg == 8 && com < 4) {
      g_hal->set_lcd_icon(com, val);
    } else if (seg == 28 && com >= 12) {
      g_hal->set_lcd_icon(com - 8, val);
    }
  }
}

void hw_set_button(button_t btn, btn_state_t state)
{
  pin_state_t pin_state = (state == BTN_STATE_PRESSED) ? PIN_STATE_LOW : PIN_STATE_HIGH;

  switch (btn) {
    case BTN_LEFT:
      cpu_set_input_pin(PIN_K02, pin_state);
      break;

    case BTN_MIDDLE:
      cpu_set_input_pin(PIN_K01, pin_state);
      break;

    case BTN_RIGHT:
      cpu_set_input_pin(PIN_K00, pin_state);
      break;
  }
}

const static uint16_t snd_freq[]= {4096,3279,2731,2341,2048,1638,1365,1170};
void hw_set_buzzer_freq(u4_t freq)
{
  if (freq>7) return;
  g_hal->set_frequency(snd_freq[freq]);
}

void hw_enable_buzzer(bool_t en)
{
  g_hal->play_frequency(en);
}

// Constructor
Tama::Tama() {
    tamalib_register_hal(&hal);
    tamalib_init(1000000);
}

void Tama::Start(){
    pthread_t thread;
    keep_going = true;
    pthread_create(&thread, 0, tamalib_mainloop, 0);
}

void Tama::Stop(){
    keep_going = false;
}

bool Tama::Runs() {
  return keep_going;
}

std::vector<bool> Tama::GetIcons() { 

    std::vector<bool> icon (ICON_NUM) ;

    int i;
    for (i = 0 ; i < ICON_NUM ; i++) {
        icon[i] = icon_buffer[(u8_t)i] != 0;
    }
    
    return icon;
  }

  std::vector<std::vector<bool>> Tama::GetMatrix() {
    std::vector<std::vector<bool>> matrix(LCD_HEIGHT, std::vector<bool>(LCD_WIDTH, false));
    int i, j, k;
    for (i = 0 ; i < LCD_HEIGHT ; i++) {
        for (j = 0 ; j < LCD_WIDTH/8 ; j++) {
          for (k = 0; k < 8; k++) {
            matrix[i][8 * j + 7 - k] = (int)(matrix_buffer[(u8_t)i][(u8_t)j] >> k) & 1;
          }
        }
    }
    return matrix;
  }

int Tama::GetFreq() { return play_freq; }

void Tama::SetButton(int n, bool state){
  if (state) {
    button_buffer[n] = 1;
  } else {
    button_buffer[n] = 0;
  }
}

std::vector<bool> Tama::GetButton(){
    std::vector<bool> button (BUTTON_NUM) ;

    int i;
    for (i = 0 ; i < BUTTON_NUM ; i++) {
        button[i] = button_buffer[(u8_t)i] != 0;
    }
    
    return button; 
}

std::vector<int> Tama::GetCPU(){
    uint32_t i = 0;
    unsigned char cpu[sizeof(cpu_state_t) + MEMORY_SIZE];
    std::vector<int> res(sizeof(cpu));

    cpu_get_state(&cpuState);

    memcpy(&cpu, &cpuState, sizeof(cpu_state_t));

    for (i = 0; i < MEMORY_SIZE; i++)
    {
        cpu[sizeof(cpu_state_t) + i] = cpuState.memory[i];
    }

    for(i = 0; i < sizeof(cpu); i++){
        res[i] = cpu[i];
    }
    return res;
}

void Tama::SetCPU(const std::vector<int> res){
    uint32_t i = 0;
    unsigned char cpu[sizeof(cpu_state_t) + MEMORY_SIZE];
    for (i = 0; i < sizeof(cpu) ; i++){
       cpu[i] = res[i];
    }

    cpu_get_state(&cpuState);
    u4_t *memTemp = cpuState.memory;
    memcpy(&cpuState, &cpu, sizeof(cpu_state_t));
    cpu_set_state(&cpuState);

    for (i = 0; i < MEMORY_SIZE; i++)
    {
        memTemp[i] = (uint8_t)cpu[sizeof(cpu_state_t) + i];
    }
}

std::vector<int> Tama::GetROM() {
  uint32_t i = 0;
  std::vector<int> rom(sizeof(g_program));
  for (i = 0; i < sizeof(g_program); i++)
    {
        rom[i] = (unsigned int)g_program[i];
    }
    return rom;
}

void Tama::SetROM(const std::vector<int> rom) {
  uint32_t i = 0;
  for (i = 0; i < sizeof(g_program); i++)
    {
        g_program[i] = (unsigned char)rom[i];
    }
}


namespace py = pybind11;

PYBIND11_MODULE(_tamalib, m) {
    py::class_<Tama>(m, "Tama")
        .def(py::init<>())
        .def("Start", &Tama::Start)
        .def("Stop", &Tama::Stop)
        .def("Runs", &Tama::Runs)
        .def("GetFreq", &Tama::GetFreq)
        .def("GetMatrix", &Tama::GetMatrix)
        .def("GetIcons", &Tama::GetIcons)
        .def("SetCPU", &Tama::SetCPU)
        .def("GetCPU", &Tama::GetCPU)
        .def("GetROM", &Tama::GetROM)
        .def("SetROM", &Tama::SetROM)
        .def("SetButton", &Tama::SetButton)
        .def("GetButton", &Tama::GetButton);
}

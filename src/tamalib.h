#ifndef Tama_H
#define Tama_H

#include <stdint.h> // uint8_t etc
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

#define tamalib_set_button(btn, state)		hw_set_button(btn, state)
#define tamalib_set_speed(speed)			cpu_set_speed(speed)
#define tamalib_refresh_hw()				cpu_refresh_hw()
#define tamalib_reset()						cpu_reset()

#define LCD_WIDTH		32
#define LCD_HEIGHT		16
#define ICON_NUM		 8
#define ROM_SIZE      9216
#define BUTTON_NUM       3

#define MEMORY_SIZE           0x140 // MEM_RAM_SIZE + MEM_IO_SIZE
#define MEM_RAM_ADDR          0x000
#define MEM_RAM_SIZE          0x280
#define MEM_DISPLAY1_ADDR     0xE00
#define MEM_DISPLAY1_ADDR_OFS 0xB80
#define MEM_DISPLAY1_SIZE     0x050
#define MEM_DISPLAY2_ADDR     0xE80
#define MEM_DISPLAY2_ADDR_OFS 0xBB0
#define MEM_DISPLAY2_SIZE     0x050
#define MEM_IO_ADDR           0xF00
#define MEM_IO_ADDR_OFS       0xF00
#define MEM_IO_SIZE           0x080

typedef uint8_t bool_t;
typedef uint8_t u4_t;
typedef uint8_t u5_t;
typedef uint8_t u8_t;
typedef uint16_t u12_t;
typedef uint16_t u13_t;
typedef uint32_t u32_t;
typedef uint32_t timestamp_t; // WARNING: Must be an unsigned type to properly handle wrapping (u32 wraps in around 1h11m when expressed in us)

typedef enum {
	LOG_ERROR	= 0x1,
	LOG_INFO	= (0x1 << 1),
	LOG_MEMORY	= (0x1 << 2),
	LOG_CPU		= (0x1 << 3),
} log_level_t;

typedef struct {
	void (*log)(log_level_t level, char *buff, ...);
	void (*sleep_until)(timestamp_t ts);
	timestamp_t (*get_timestamp)(void);
	void (*set_lcd_matrix)(u8_t x, u8_t y, bool_t val);
	void (*set_lcd_icon)(u8_t icon, bool_t val);
	void (*set_frequency)(u32_t freq);
	void (*play_frequency)(bool_t en);
	int (*handler)(void);
} hal_t;

typedef enum {
	BTN_STATE_RELEASED = 0,
	BTN_STATE_PRESSED,
} btn_state_t;

typedef enum {
	BTN_LEFT = 0,
	BTN_MIDDLE,
	BTN_RIGHT,
} button_t;

typedef enum {
	EXEC_MODE_PAUSE,
	EXEC_MODE_RUN,
	EXEC_MODE_STEP,
	EXEC_MODE_NEXT,
	EXEC_MODE_TO_CALL,
	EXEC_MODE_TO_RET,
} exec_mode_t;

typedef struct breakpoint {
  u13_t addr;
  struct breakpoint *next;
} breakpoint_t;

typedef struct {
  u4_t factor_flag_reg;
  u4_t mask_reg;
  bool_t triggered; /* 1 if triggered, 0 otherwise */
  u8_t vector;
} interrupt_t;

typedef struct {
  u13_t pc;
  u12_t x;
  u12_t y;
  u4_t a;
  u4_t b;
  u5_t np;
  u8_t sp;
  u4_t flags;
  u32_t tick_counter;
  u32_t clk_timer_timestamp;
  u32_t prog_timer_timestamp;
  bool_t prog_timer_enabled;
  u8_t prog_timer_data;
  u8_t prog_timer_rld;
  u32_t call_depth;
  u4_t *memory;
  interrupt_t interrupts[6];  
 } cpu_state_t;

typedef enum {
  PIN_K00 = 0x0,
  PIN_K01 = 0x1,
  PIN_K02 = 0x2,
  PIN_K03 = 0x3,
  PIN_K10 = 0X4,
  PIN_K11 = 0X5,
  PIN_K12 = 0X6,
  PIN_K13 = 0X7,
} pin_t;

typedef enum {
  PIN_STATE_LOW = 0,
  PIN_STATE_HIGH = 1,
} pin_state_t;

typedef enum {
  INT_PROG_TIMER_SLOT = 0,
  INT_SERIAL_SLOT = 1,
  INT_K10_K13_SLOT = 2,
  INT_K00_K03_SLOT = 3,
  INT_STOPWATCH_SLOT = 4,
  INT_CLOCK_TIMER_SLOT = 5,
  INT_SLOT_NUM,
} int_slot_t;

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

class Tama {
public:

  // Constructor
  Tama();

  // Getters
  std::vector<bool> GetIcon();
  std::vector<std::vector<bool>> GetMatrix();
  int GetFreq();
  std::vector<bool> GetButton();
  std::vector<double> GetCPU();
  std::vector<double> GetROM();
  
  // Setters
  void SetButton(int n, bool state);
  void SetCPU(const std::vector<double>& res);
  void SetROM(const std::vector<double>& rom);

  // public methods
  void start();
  void stop();

private: 
};

#endif

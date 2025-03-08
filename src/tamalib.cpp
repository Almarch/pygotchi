#include <pthread.h>
#include <thread> // sleep_for
#include <chrono> // high resolution clock

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

#include "hal_types.h"
#include "lib/hal.h"
#include "lib/hw.h"
#include "lib/cpu.h"
#include "lib/tamalib.h"

#define DEFAULT_FRAMERATE				30 // fps

static exec_mode_t exec_mode = EXEC_MODE_RUN;
static u32_t step_depth = 0;
static timestamp_t screen_ts = 0;
static u32_t ts_freq;
static u8_t g_framerate = DEFAULT_FRAMERATE;
static const auto epochTime = std::chrono::high_resolution_clock::from_time_t(0);

hal_t *g_hal;

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


bool_t tamalib_init(const u12_t *program, breakpoint_t *breakpoints, u32_t freq)
{
	bool_t res = 0;

	res |= cpu_init(program, breakpoints, freq);
	res |= hw_init();

	ts_freq = freq;

	return res;
}

void tamalib_release(void)
{
	hw_release();
	cpu_release();
}

void tamalib_set_framerate(u8_t framerate)
{
	g_framerate = framerate;
}

u8_t tamalib_get_framerate(void)
{
	return g_framerate;
}

void tamalib_register_hal(hal_t *hal)
{
	g_hal = hal;
}

void tamalib_set_exec_mode(exec_mode_t mode)
{
	exec_mode = mode;
	step_depth = cpu_get_depth();
	cpu_sync_ref_timestamp();
}

void tamalib_step(void)
{
	if (exec_mode == EXEC_MODE_PAUSE) {
		return;
	}

	if (cpu_step()) {
		exec_mode = EXEC_MODE_PAUSE;
		step_depth = cpu_get_depth();
	} else {
		switch (exec_mode) {
			case EXEC_MODE_PAUSE:
			case EXEC_MODE_RUN:
				break;

			case EXEC_MODE_STEP:
				exec_mode = EXEC_MODE_PAUSE;
				break;

			case EXEC_MODE_NEXT:
				if (cpu_get_depth() <= step_depth) {
					exec_mode = EXEC_MODE_PAUSE;
					step_depth = cpu_get_depth();
				}
				break;

			case EXEC_MODE_TO_CALL:
				if (cpu_get_depth() > step_depth) {
					exec_mode = EXEC_MODE_PAUSE;
					step_depth = cpu_get_depth();
				}
				break;

			case EXEC_MODE_TO_RET:
				if (cpu_get_depth() < step_depth) {
					exec_mode = EXEC_MODE_PAUSE;
					step_depth = cpu_get_depth();
				}
				break;
		}
	}
}

void tamalib_mainloop(void)
{
	timestamp_t ts;

	while (!g_hal->handler()) {
		tamalib_step();

		/* Update the screen @ g_framerate fps */
		ts = g_hal->get_timestamp();
		if (ts - screen_ts >= ts_freq/g_framerate) {
			screen_ts = ts;
			g_hal->update_screen();
		}
	}
}

class Tama {
  public:
    Tama();
    std::vector<bool> GetIcons();
    std::vector<std::vector<bool>> GetMatrix();
    int GetFreq();
    std::vector<int> GetCPU();
    std::vector<int> GetROM();
    void SetButton(int n, bool state);
    void SetCPU(const std::vector<int> res);
    void SetROM(const std::vector<int> rom);
    bool Runs();
    void Start();
    void Stop();
  private: 
};

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

std::vector<bool> Tama::GetIcons()
{

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

void Tama::SetButton(int n, uint8_t pressed){
  switch(n) {
    case 0:
      tamalib_set_button(BTN_LEFT, pressed ? BTN_STATE_PRESSED : BTN_STATE_RELEASED);
    case 1:
      tamalib_set_button(BTN_MIDDLE, pressed ? BTN_STATE_PRESSED : BTN_STATE_RELEASED);
    case 2:
      tamalib_set_button(BTN_RIGHT, pressed ? BTN_STATE_PRESSED : BTN_STATE_RELEASED);
    case 3:
      tamalib_set_button(BTN_TAP, pressed ? BTN_STATE_PRESSED : BTN_STATE_RELEASED);
  }
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

PYBIND11_MODULE(_tamalib, m) {
  pybind11::class_<Tama>(m, "Tama")
    .def(pybind11::init<>())
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
    .def("SetButton", &Tama::SetButton);
}

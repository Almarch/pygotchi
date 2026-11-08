#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <atomic>
#include <chrono>
#include <cstdarg>
#include <cstdlib>
#include <cstring>
#include <thread>
#include <vector>

extern "C" {
#include "tamalib.h"
}

#define TAMA_FREQ 1000000 // Timestamps are expressed in microseconds

/* The Python side stores ROMs as packed 12-bit words (3 bytes for 2 words).
 * TamaLIB expects one u12_t per instruction. */
#define ROM_WORDS 8192
/* Includes BTN_TAP, the 4th TamaLIB input (tap sensor). */
#define BUTTON_NUM (BTN_TAP + 1)

static std::vector<u8_t> rom_buffer;
static std::vector<u12_t> program(ROM_WORDS, 0);
static std::atomic<bool> keep_going{false};
static std::thread mainloop_thread;

static u8_t matrix_buffer[LCD_HEIGHT][LCD_WIDTH / 8] = {{0}};
static u8_t icon_buffer[ICON_NUM] = {0};
static u8_t button_buffer[BUTTON_NUM] = {0};

static u32_t current_freq = 0;
static u32_t play_freq = 0;

/* CPU snapshot used by dump()/load() for save states. */
#pragma pack(push, 1)
struct cpu_snapshot_t {
  u13_t pc;
  u12_t x;
  u12_t y;
  u4_t a;
  u4_t b;
  u5_t np;
  u8_t sp;
  u4_t flags;

  u32_t tick_counter;
  u32_t clk_timer_2hz_timestamp;
  u32_t clk_timer_4hz_timestamp;
  u32_t clk_timer_8hz_timestamp;
  u32_t clk_timer_16hz_timestamp;
  u32_t clk_timer_32hz_timestamp;
  u32_t clk_timer_64hz_timestamp;
  u32_t clk_timer_128hz_timestamp;
  u32_t clk_timer_256hz_timestamp;
  u32_t prog_timer_timestamp;
  bool_t prog_timer_enabled;
  u8_t prog_timer_data;
  u8_t prog_timer_rld;
  u32_t call_depth;
  bool_t cpu_halted;

  interrupt_t interrupts[INT_SLOT_NUM];
  u8_t memory[MEM_BUFFER_SIZE];
  u8_t pad[3];
};
#pragma pack(pop)

static_assert(sizeof(cpu_snapshot_t) % 2 == 0,
              "The CPU snapshot must have an even size for int2bin()");
static_assert((2 * sizeof(cpu_snapshot_t) + ((2 * sizeof(cpu_snapshot_t) - 1) / 3 + 1)) % 2 == 0,
              "int2bin() must produce an even number of hex digits");

static void *hal_malloc(u32_t size) {
  return malloc(size);
}

static void hal_free(void *ptr) {
  free(ptr);
}

static void hal_halt(void) {
}

static bool_t hal_is_log_enabled(log_level_t) {
  return 0;
}

static void hal_log(log_level_t, char *, ...) {
}

static timestamp_t hal_get_timestamp(void) {
  auto now = std::chrono::steady_clock::now().time_since_epoch();
  return (timestamp_t) std::chrono::duration_cast<std::chrono::microseconds>(now).count();
}

static void hal_sleep_until(timestamp_t ts) {
  int32_t diff = (int32_t) (ts - hal_get_timestamp());
  if (diff > 0) {
    std::this_thread::sleep_for(std::chrono::microseconds(diff));
  }
}

static void hal_update_screen(void) {
}

static void hal_set_lcd_matrix(u8_t x, u8_t y, bool_t val) {
  u8_t mask = 0x80 >> (x % 8);
  if (val) {
    matrix_buffer[y][x / 8] |= mask;
  } else {
    matrix_buffer[y][x / 8] &= ~mask;
  }
}

static void hal_set_lcd_icon(u8_t icon, bool_t val) {
  icon_buffer[icon] = val;
}

static void hal_set_frequency(u32_t freq) {
  current_freq = freq;
}

static void hal_play_frequency(bool_t en) {
  play_freq = en ? current_freq : 0;
}

static int hal_handler(void) {
  for (u8_t i = 0; i < BUTTON_NUM; i++) {
    hw_set_button((button_t) i, button_buffer[i] ? BTN_STATE_PRESSED : BTN_STATE_RELEASED);
  }
  return keep_going ? 0 : 1;
}

static hal_t hal = {
  hal_malloc,
  hal_free,
  hal_halt,
  hal_is_log_enabled,
  hal_log,
  hal_sleep_until,
  hal_get_timestamp,
  hal_update_screen,
  hal_set_lcd_matrix,
  hal_set_lcd_icon,
  hal_set_frequency,
  hal_play_frequency,
  hal_handler,
};

static void unpack_rom(const std::vector<u8_t> &rom, std::vector<u12_t> &words) {
  words.assign(ROM_WORDS, 0);

  size_t word = 0;
  for (size_t i = 0; i + 2 < rom.size() && word < ROM_WORDS; i += 3) {
    words[word++] = (u12_t) (((rom[i] << 4) | (rom[i + 1] >> 4)) & 0xFFF);
    if (word < ROM_WORDS) {
      words[word++] = (u12_t) (((rom[i + 1] << 8) | rom[i + 2]) & 0xFFF);
    }
  }
}

static cpu_snapshot_t get_cpu_snapshot(void) {
  cpu_snapshot_t snap;
  memset(&snap, 0, sizeof(snap));

  state_t *state = cpu_get_state();
  snap.pc = *state->pc;
  snap.x = *state->x;
  snap.y = *state->y;
  snap.a = *state->a;
  snap.b = *state->b;
  snap.np = *state->np;
  snap.sp = *state->sp;
  snap.flags = *state->flags;

  snap.tick_counter = *state->tick_counter;
  snap.clk_timer_2hz_timestamp = *state->clk_timer_2hz_timestamp;
  snap.clk_timer_4hz_timestamp = *state->clk_timer_4hz_timestamp;
  snap.clk_timer_8hz_timestamp = *state->clk_timer_8hz_timestamp;
  snap.clk_timer_16hz_timestamp = *state->clk_timer_16hz_timestamp;
  snap.clk_timer_32hz_timestamp = *state->clk_timer_32hz_timestamp;
  snap.clk_timer_64hz_timestamp = *state->clk_timer_64hz_timestamp;
  snap.clk_timer_128hz_timestamp = *state->clk_timer_128hz_timestamp;
  snap.clk_timer_256hz_timestamp = *state->clk_timer_256hz_timestamp;
  snap.prog_timer_timestamp = *state->prog_timer_timestamp;
  snap.prog_timer_enabled = *state->prog_timer_enabled;
  snap.prog_timer_data = *state->prog_timer_data;
  snap.prog_timer_rld = *state->prog_timer_rld;
  snap.call_depth = *state->call_depth;
  snap.cpu_halted = *state->cpu_halted;

  memcpy(snap.interrupts, state->interrupts, sizeof(snap.interrupts));
  memcpy(snap.memory, state->memory, MEM_BUFFER_SIZE);

  return snap;
}

static void set_cpu_snapshot(const cpu_snapshot_t &snap) {
  state_t *state = cpu_get_state();
  *state->pc = snap.pc;
  *state->x = snap.x;
  *state->y = snap.y;
  *state->a = snap.a;
  *state->b = snap.b;
  *state->np = snap.np;
  *state->sp = snap.sp;
  *state->flags = snap.flags;

  *state->tick_counter = snap.tick_counter;
  *state->clk_timer_2hz_timestamp = snap.clk_timer_2hz_timestamp;
  *state->clk_timer_4hz_timestamp = snap.clk_timer_4hz_timestamp;
  *state->clk_timer_8hz_timestamp = snap.clk_timer_8hz_timestamp;
  *state->clk_timer_16hz_timestamp = snap.clk_timer_16hz_timestamp;
  *state->clk_timer_32hz_timestamp = snap.clk_timer_32hz_timestamp;
  *state->clk_timer_64hz_timestamp = snap.clk_timer_64hz_timestamp;
  *state->clk_timer_128hz_timestamp = snap.clk_timer_128hz_timestamp;
  *state->clk_timer_256hz_timestamp = snap.clk_timer_256hz_timestamp;
  *state->prog_timer_timestamp = snap.prog_timer_timestamp;
  *state->prog_timer_enabled = snap.prog_timer_enabled;
  *state->prog_timer_data = snap.prog_timer_data;
  *state->prog_timer_rld = snap.prog_timer_rld;
  *state->call_depth = snap.call_depth;
  *state->cpu_halted = snap.cpu_halted;

  memcpy(state->interrupts, snap.interrupts, sizeof(snap.interrupts));
  memcpy(state->memory, snap.memory, MEM_BUFFER_SIZE);

  cpu_refresh_hw();
  cpu_sync_ref_timestamp();
}

class Tama {
public:
  Tama();
  ~Tama();

  std::vector<bool> GetIcons();
  u8_t GetIconsByte();
  std::vector<std::vector<bool>> GetMatrix();
  std::vector<u8_t> GetMatrixBytes();
  int GetFreq();
  std::vector<bool> GetButton();
  std::vector<int> GetCPU();
  std::vector<int> GetROM();

  void SetButton(int n, bool state);
  void SetCPU(const std::vector<int> res);
  void SetROM(const std::vector<int> rom);

  bool Runs();
  void Start();
  void Stop();
};

Tama::Tama() {
  tamalib_register_hal(&hal);
  tamalib_init(program.data(), NULL, TAMA_FREQ);
}

Tama::~Tama() {
  Stop();
}

std::vector<bool> Tama::GetIcons() {
  std::vector<bool> icons(ICON_NUM);
  for (int i = 0; i < ICON_NUM; i++) {
    icons[i] = icon_buffer[i] != 0;
  }
  return icons;
}

u8_t Tama::GetIconsByte() {
  u8_t byte = 0;
  for (int i = 0; i < ICON_NUM; i++) {
    if (icon_buffer[i] != 0) {
      byte |= (1 << i);
    }
  }
  return byte;
}

std::vector<std::vector<bool>> Tama::GetMatrix() {
  std::vector<std::vector<bool>> matrix(LCD_HEIGHT, std::vector<bool>(LCD_WIDTH, false));
  for (int i = 0; i < LCD_HEIGHT; i++) {
    for (int j = 0; j < LCD_WIDTH / 8; j++) {
      for (int k = 0; k < 8; k++) {
        matrix[i][8 * j + 7 - k] = (matrix_buffer[i][j] >> k) & 1;
      }
    }
  }
  return matrix;
}

std::vector<u8_t> Tama::GetMatrixBytes() {
  std::vector<u8_t> bytes(LCD_HEIGHT * (LCD_WIDTH / 8));
  for (int i = 0; i < LCD_HEIGHT; i++) {
    for (int j = 0; j < LCD_WIDTH / 8; j++) {
      bytes[i * (LCD_WIDTH / 8) + j] = matrix_buffer[i][j];
    }
  }
  return bytes;
}

int Tama::GetFreq() {
  /* TamaLIB exposes frequencies in deciHz, the web UI expects Hz. */
  return play_freq / 10;
}

std::vector<bool> Tama::GetButton() {
  std::vector<bool> buttons(BUTTON_NUM);
  for (int i = 0; i < BUTTON_NUM; i++) {
    buttons[i] = button_buffer[i] != 0;
  }
  return buttons;
}

std::vector<int> Tama::GetCPU() {
  cpu_snapshot_t snap = get_cpu_snapshot();
  std::vector<int> res(sizeof(snap));
  const u8_t *bytes = reinterpret_cast<const u8_t *>(&snap);
  for (size_t i = 0; i < sizeof(snap); i++) {
    res[i] = bytes[i];
  }
  return res;
}

std::vector<int> Tama::GetROM() {
  std::vector<int> rom(rom_buffer.size());
  for (size_t i = 0; i < rom_buffer.size(); i++) {
    rom[i] = rom_buffer[i];
  }
  return rom;
}

void Tama::SetButton(int n, bool state) {
  if (n < 0 || n >= BUTTON_NUM) {
    return;
  }
  button_buffer[n] = state ? 1 : 0;
}

void Tama::SetCPU(const std::vector<int> res) {
  if (res.size() != sizeof(cpu_snapshot_t)) {
    return;
  }

  cpu_snapshot_t snap;
  u8_t *bytes = reinterpret_cast<u8_t *>(&snap);
  for (size_t i = 0; i < sizeof(snap); i++) {
    bytes[i] = (u8_t) res[i];
  }

  set_cpu_snapshot(snap);
}

void Tama::SetROM(const std::vector<int> rom) {
  rom_buffer.assign(rom.size(), 0);
  for (size_t i = 0; i < rom.size(); i++) {
    rom_buffer[i] = (u8_t) rom[i];
  }

  unpack_rom(rom_buffer, program);
  tamalib_release();
  tamalib_init(program.data(), NULL, TAMA_FREQ);
}

bool Tama::Runs() {
  return keep_going;
}

void Tama::Start() {
  if (keep_going.exchange(true)) {
    return;
  }
  if (mainloop_thread.joinable()) {
    mainloop_thread.join();
  }
  mainloop_thread = std::thread([] { tamalib_mainloop(); });
}

void Tama::Stop() {
  keep_going = false;
  if (mainloop_thread.joinable()) {
    mainloop_thread.join();
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
      .def("GetMatrixBytes", &Tama::GetMatrixBytes)
      .def("GetIcons", &Tama::GetIcons)
      .def("GetIconsByte", &Tama::GetIconsByte)
      .def("SetCPU", &Tama::SetCPU)
      .def("GetCPU", &Tama::GetCPU)
      .def("GetROM", &Tama::GetROM)
      .def("SetROM", &Tama::SetROM)
      .def("SetButton", &Tama::SetButton)
      .def("GetButton", &Tama::GetButton);
}

#include <pthread.h>
#include <thread> // sleep_for
#include <chrono> // high resolution clock
#include <cstring> // memcpy
#include <stdlib.h> // exit

#include <vector>

#include "hal_types.h"
#include "lib/hal.h"
#include "lib/hw.h"
#include "lib/cpu.h"
#include "lib/tamalib.h"
#include "binder.h"

bool keep_going

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

void Tama::SetButton(int n, bool state){
  if (state) {
    button_buffer[n] = 1;
  } else {
    button_buffer[n] = 0;
  }
}

std::vector<bool> Tama::GetButton(){
    std::vector<bool> button (4) ;

    int i;
    for (i = 0 ; i < 4 ; i++) {
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

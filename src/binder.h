
#ifndef _BINDER_H_
#define _BINDER_H_

#include <stdint.h> // uint8_t etc
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

#include "hal_types.h"
#include "lib/hal.h"
#include "lib/hw.h"
#include "lib/cpu.h"
#include "lib/tamalib.h"

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
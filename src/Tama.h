#ifndef _TAMA_
#define _TAMA_

#include <vector>

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

#endif
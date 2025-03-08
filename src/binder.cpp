#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "Tama.h"

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

#include <pybind11/pybind11.h>
#include "tamalib.h"

namespace py = pybind11;

PYBIND11_MODULE(_tamagotchi, m) {
    py::class_<Tamagotchi>(m, "Tamagotchi")
        .def(py::init<>())
        .def("start", &Tamagotchi::start)
        .def("stop", &Tamagotchi::stop)
        .def("GetFreq", &Tamagotchi::GetFreq)
        .def("GetMatrix", &Tamagotchi::GetMatrix)
        .def("GetIcon", &Tamagotchi::GetIcon)
        .def("SetCPU", &Tamagotchi::SetCPU)
        .def("GetCPU", &Tamagotchi::GetCPU)
        .def("GetROM", &Tamagotchi::GetROM)
        .def("SetROM", &Tamagotchi::SetROM)
        .def("SetButton", &Tamagotchi::SetButton)
        .def("GetButton", &Tamagotchi::GetButton);
}
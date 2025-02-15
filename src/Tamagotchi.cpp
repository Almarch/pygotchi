#include <pybind11/pybind11.h>
#include "tamalib.h"

namespace py = pybind11;

PYBIND11_MODULE(_tamagotchi, m) {
    py::class_<Tama>(m, "Tamagotchi")
        .def(py::init<>())
        .def("start", &Tama::start)
        .def("stop", &Tama::stop)
        .def("GetFreq", &Tama::GetFreq)
        .def("GetMatrix", &Tama::GetMatrix)
        .def("GetIcon", &Tama::GetIcon)
        .def("SetCPU", &Tama::SetCPU)
        .def("GetCPU", &Tama::GetCPU)
        .def("GetROM", &Tama::GetROM)
        .def("SetROM", &Tama::SetROM)
        .def("SetButton", &Tama::SetButton)
        .def("GetButton", &Tama::GetButton);
}
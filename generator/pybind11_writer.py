from typing import List
import pathlib
from .parser import Parser
from .header import Header


def write(package_dir: pathlib.Path, parser: Parser, headers: List[Header]):

    cpp_path = package_dir / 'bind/impl.cpp'
    cpp_path.parent.mkdir(parents=True, exist_ok=True)

    with cpp_path.open('w') as w:
        w.write('''// generated
#include <pybind11/pybind11.h>

int add(int i, int j) {
  return i + j;
}

PYBIND11_MODULE(impl, m) {
  m.doc() = "pybind11 example plugin"; // optional module docstring
  m.def("add", &add, "A function which adds two numbers");
}
''')

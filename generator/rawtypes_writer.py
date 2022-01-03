from typing import List
import pathlib
from .parser import Parser
from .header import Header


def write(package_dir: pathlib.Path, parser: Parser, headers: List[Header]):

    cpp_path = package_dir / 'rawtypes/implmodule.cpp'
    cpp_path.parent.mkdir(parents=True, exist_ok=True)

    with cpp_path.open('w') as w:
        w.write('''// generated
#define PY_SSIZE_T_CLEAN
#include <Python.h>

// IMGUI_API ImGuiContext* CreateContext(ImFontAtlas* shared_font_atlas = NULL);
#include <imgui.h>
static PyObject *
CreateContext(PyObject *self, PyObject *args)
{
  auto result = reinterpret_cast<uintptr_t>(ImGui::CreateContext());
  return PyLong_FromLong(result);
}
//

static PyMethodDef Methods[] = {
    {"CreateContext",  CreateContext, METH_VARARGS, "ImGui::CreateContext"},  
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "impl",   /* name of module */
    nullptr, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    Methods
};

PyMODINIT_FUNC
PyInit_impl(void)
{
    auto m = PyModule_Create(&module);
    if (!m){
        return NULL;
    }

    static auto ImplError = PyErr_NewException("impl.error", NULL, NULL);
    Py_XINCREF(ImplError);
    if (PyModule_AddObject(m, "error", ImplError) < 0) {
        Py_XDECREF(ImplError);
        Py_CLEAR(ImplError);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
''')

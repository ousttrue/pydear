# pydear 🦌

ImGui wrapper generated by clang.cindex. 

- [github repository](https://github.com/ousttrue/pydear)
- [pypi](https://pypi.org/project/pydear/)

Works in conjunction with [PyOpenGL](https://pypi.org/project/PyOpenGL/) and [glfw](https://pypi.org/project/glfw/).

[examples](./examples)

## PreBuild wheel

Only Python-3.10 (Windows 64bit) is provided.
It was developed on Windows and worked on Linux as well.

## Included Bindings

A luajit-like style using ctypes.
Pointer arguments are passed by an array of length 1.

```python
p_open = (ctypes.c_bool * 1)(True)
ImGui.Begin('name', p_open)
```

Also, all C structs are defined as `ctypes.Struct` generated using clang.cindex.

```python
class ImGuiIO(ctypes.Structure):
    _fields_=[
        ("ConfigFlags", ctypes.c_int32), # Int32Type: int,
        ("BackendFlags", ctypes.c_int32), # Int32Type: int,
```

The ImGUi backend is provided in a pure Python module `pydear.backends`.
Currently only glfw and OpenGL3 exist.

Most bindings are available, except for functions that have callback and va_list as arguments.

### ImGui-1.87 docking branch

<https://github.com/ocornut/imgui>

### ImNodes

<https://github.com/Nelarius/imnodes>

### NanoVG modified

<https://github.com/ousttrue/picovg/>

## Detail

<https://ousttrue.github.io/pydear/>

## Build

### Code generation

<https://github.com/ousttrue/rawtypes>

### Package check

```
py -m pip wheel .
twine check pydear-1.12.1-cp310-cp310-linux_x86_64.whl
```

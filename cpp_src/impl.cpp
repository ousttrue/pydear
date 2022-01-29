// generated
#define PY_SSIZE_T_CLEAN
#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#include <iostream>
#else
#include <Python.h>
#endif

#include <string>
#include <string_view>
#include <unordered_map>

static PyObject *s_ctypes = nullptr;
static PyObject *s_ctypes_c_void_p = nullptr;
static PyObject *s_ctypes_addressof = nullptr;
static PyObject *s_ctypes_Array = nullptr;
static PyObject *s_ctypes_Structure = nullptr;
static PyObject *s_ctypes_POINTER = nullptr;
static PyObject *s_ctypes__CFuncPtr = nullptr;
static PyObject *s_ctypes_cast = nullptr;
static PyObject *s_value = nullptr;
static std::unordered_map<std::string, PyObject *> s_pydear_ctypes;
static void s_initialize() {
  if (s_ctypes) {
    return;
  }
  // ctypes
  s_ctypes = PyImport_ImportModule("ctypes");
  s_ctypes_c_void_p = PyObject_GetAttrString(s_ctypes, "c_void_p");
  s_ctypes_addressof = PyObject_GetAttrString(s_ctypes, "addressof");
  s_ctypes_Array = PyObject_GetAttrString(s_ctypes, "Array");
  s_ctypes_Structure = PyObject_GetAttrString(s_ctypes, "Structure");
  s_ctypes_POINTER = PyObject_GetAttrString(s_ctypes, "POINTER");
  s_ctypes__CFuncPtr = PyObject_GetAttrString(s_ctypes, "_CFuncPtr");
  s_ctypes_cast = PyObject_GetAttrString(s_ctypes, "cast");
  //
  s_value = PyUnicode_FromString("value");
  //
}

static void *ctypes_get_addressof(PyObject *src) {
  if (PyObject *p = PyObject_CallFunction(s_ctypes_addressof, "O", src)) {
    auto pp = PyLong_AsVoidPtr(p);
    Py_DECREF(p);
    return pp;
  }
  return nullptr;
}

template <typename T> T ctypes_get_pointer(PyObject *src) {
  if (!src) {
    return (T) nullptr;
  }

  // ctypes.c_void_p
  if (PyObject_IsInstance(src, s_ctypes_c_void_p)) {
    if (PyObject *p = PyObject_GetAttr(src, s_value)) {
      auto pp = PyLong_AsVoidPtr(p);
      Py_DECREF(p);
      return (T)pp;
    }
    PyErr_Clear();
  }

  // ctypes.Array
  // ctypes.Structure
  if (PyObject_IsInstance(src, s_ctypes_Array) ||
      PyObject_IsInstance(src, s_ctypes_Structure) ||
      PyObject_IsInstance(src, s_ctypes__CFuncPtr)) {
    if (void *p = ctypes_get_addressof(src)) {
      return (T)p;
    }
    PyErr_Print();
    PyErr_Clear();
  }

  return (T) nullptr;
}

static PyObject *GetCTypesType(const char *t, const char *sub) {
  static std::unordered_map<std::string, PyObject *> s_map;
  {
    auto found = s_map.find(t);
    if (found != s_map.end()) {
      return found->second;
    }
  }

  PyObject *p = nullptr;
  {
    auto found = s_pydear_ctypes.find(sub);
    if (found == s_pydear_ctypes.end()) {
      p = PyImport_ImportModule((std::string("pydear.") + sub).c_str());
      s_pydear_ctypes.insert(std::make_pair(sub, p));
    } else {
      p = found->second;
    }
  }

  auto T = PyObject_GetAttrString(p, t);
  s_map.insert(std::make_pair(std::string(t), T));
  return T;
}

static PyObject *GetCTypesPointerType(const char *t, const char *sub) {
  static std::unordered_map<std::string, PyObject *> s_map;
  {
    auto found = s_map.find(t);
    if (found != s_map.end()) {
      return found->second;
    }
  }

  auto T = GetCTypesType(t, sub);
  auto result = PyObject_CallFunction(s_ctypes_POINTER, "O", T);
  s_map.insert(std::make_pair(std::string(t), result));
  return result;
}

static PyObject *ctypes_cast(PyObject *src, const char *t, const char *sub) {
  // ctypes.cast(src, ctypes.POINTER(t))[0]
  auto ptype = GetCTypesPointerType(t, sub);
  auto p = PyObject_CallFunction(s_ctypes_cast, "OO", src, ptype);
  Py_DECREF(src);
  auto py_value = PySequence_GetItem(p, 0);
  Py_DECREF(p);
  return py_value;
}

static const char *get_cstring(PyObject *src, const char *default_value) {
  if (src) {
    if (auto p = PyUnicode_AsUTF8(src)) {
      return p;
    }
    PyErr_Clear();

    if (auto p = PyBytes_AsString(src)) {
      return p;
    }
    PyErr_Clear();
  }

  return default_value;
}

static PyObject *py_string(const std::string_view &src) {
  return PyUnicode_FromStringAndSize(src.data(), src.size());
}

static PyObject *c_void_p(const void *address) {
  return PyObject_CallFunction(s_ctypes_c_void_p, "K", (uintptr_t)address);
}

template <typename T>
static PyObject *ctypes_copy(const T &src, const char *t, const char *sub) {
  auto ptype = GetCTypesType(t, sub);
  auto obj = PyObject_CallNoArgs(ptype);
  // get ptr
  auto p = (T*)ctypes_get_addressof(obj);  
  // memcpy
  memcpy(p, &src, sizeof(T));
  return obj;
}

// clang-format off
# include <imgui.h>

static ImVec2 get_ImVec2(PyObject *src)
{
    float x, y;
    if(PyArg_ParseTuple(src, "ff", &x, &y))
    {
        return {x, y};
    }
    PyErr_Clear();

    return {};
}
// clang-format off
static PyObject *imgui_CreateContext(PyObject *self, PyObject *args) {
  // PointerToStructType: ImFontAtlas*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImFontAtlas *p0 = t0 ? ctypes_get_pointer<ImFontAtlas*>(t0) :  NULL;

  
  auto value = ImGui::CreateContext(p0);
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiContext", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DestroyContext(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImGuiContext *p0 = t0 ? ctypes_get_pointer<ImGuiContext*>(t0) :  NULL;

  
  ImGui::DestroyContext(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCurrentContext(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCurrentContext();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiContext", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetCurrentContext(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImGuiContext *p0 = ctypes_get_pointer<ImGuiContext*>(t0);

  
  ImGui::SetCurrentContext(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetIO(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  // ReferenceToStructType: ImGuiIO&
auto value = &ImGui::GetIO();
auto py_value = c_void_p(value);
py_value = ctypes_cast(py_value, "ImGuiIO", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetStyle(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  // ReferenceToStructType: ImGuiStyle&
auto value = &ImGui::GetStyle();
auto py_value = c_void_p(value);
py_value = ctypes_cast(py_value, "ImGuiStyle", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_NewFrame(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::NewFrame();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndFrame(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndFrame();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Render(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::Render();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetDrawData(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetDrawData();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawData", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowDemoWindow(PyObject *self, PyObject *args) {
  // PointerType: bool*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool *p0 = t0 ? ctypes_get_pointer<bool*>(t0) :  NULL;

  
  ImGui::ShowDemoWindow(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowMetricsWindow(PyObject *self, PyObject *args) {
  // PointerType: bool*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool *p0 = t0 ? ctypes_get_pointer<bool*>(t0) :  NULL;

  
  ImGui::ShowMetricsWindow(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowStackToolWindow(PyObject *self, PyObject *args) {
  // PointerType: bool*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool *p0 = t0 ? ctypes_get_pointer<bool*>(t0) :  NULL;

  
  ImGui::ShowStackToolWindow(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowAboutWindow(PyObject *self, PyObject *args) {
  // PointerType: bool*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool *p0 = t0 ? ctypes_get_pointer<bool*>(t0) :  NULL;

  
  ImGui::ShowAboutWindow(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowStyleEditor(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiStyle*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImGuiStyle *p0 = t0 ? ctypes_get_pointer<ImGuiStyle*>(t0) :  NULL;

  
  ImGui::ShowStyleEditor(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowStyleSelector(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  auto value = ImGui::ShowStyleSelector(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowFontSelector(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::ShowFontSelector(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ShowUserGuide(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::ShowUserGuide();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetVersion(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetVersion();
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_StyleColorsDark(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiStyle*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImGuiStyle *p0 = t0 ? ctypes_get_pointer<ImGuiStyle*>(t0) :  NULL;

  
  ImGui::StyleColorsDark(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_StyleColorsLight(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiStyle*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImGuiStyle *p0 = t0 ? ctypes_get_pointer<ImGuiStyle*>(t0) :  NULL;

  
  ImGui::StyleColorsLight(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_StyleColorsClassic(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiStyle*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImGuiStyle *p0 = t0 ? ctypes_get_pointer<ImGuiStyle*>(t0) :  NULL;

  
  ImGui::StyleColorsClassic(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Begin(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "O|OO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = t1 ? ctypes_get_pointer<bool*>(t1) :  NULL;

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::Begin(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_End(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::End();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginChild(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  bool p2 = t2 ? t2 == Py_True :  false;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::BeginChild(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginChild_2(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  bool p2 = t2 ? t2 == Py_True :  false;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::BeginChild(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndChild(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndChild();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsWindowAppearing(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsWindowAppearing();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsWindowCollapsed(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsWindowCollapsed();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsWindowFocused(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  auto value = ImGui::IsWindowFocused(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsWindowHovered(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  auto value = ImGui::IsWindowHovered(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowDrawList(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowDrawList();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawList", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowDpiScale(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowDpiScale();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowPos();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowSize(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowSize();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowWidth(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowWidth();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowHeight(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowHeight();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowViewport(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowViewport();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiViewport", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowPos(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "O|OO", &t0, &t1, &t2))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImVec2 p2 = t2 ? get_ImVec2(t2) :  ImVec2 ( 0 , 0 );

  
  ImGui::SetNextWindowPos(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowSize(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetNextWindowSize(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowContentSize(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImGui::SetNextWindowContentSize(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowCollapsed(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  bool p0 = t0 == Py_True;

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetNextWindowCollapsed(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowFocus(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::SetNextWindowFocus();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowBgAlpha(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetNextWindowBgAlpha(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowViewport(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  ImGui::SetNextWindowViewport(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowPos(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetWindowPos(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowSize(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetWindowSize(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowCollapsed(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  bool p0 = t0 == Py_True;

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetWindowCollapsed(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowFocus(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::SetWindowFocus();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowFontScale(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetWindowFontScale(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowPos_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImGui::SetWindowPos(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowSize_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImGui::SetWindowSize(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowCollapsed_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool p1 = t1 == Py_True;

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImGui::SetWindowCollapsed(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetWindowFocus_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::SetWindowFocus(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetContentRegionAvail(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetContentRegionAvail();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetContentRegionMax(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetContentRegionMax();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowContentRegionMin(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowContentRegionMin();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowContentRegionMax(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowContentRegionMax();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetScrollX(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetScrollX();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetScrollY(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetScrollY();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollX(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetScrollX(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollY(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetScrollY(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetScrollMaxX(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetScrollMaxX();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetScrollMaxY(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetScrollMaxY();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollHereX(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.5f;

  
  ImGui::SetScrollHereX(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollHereY(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.5f;

  
  ImGui::SetScrollHereY(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollFromPosX(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  0.5f;

  
  ImGui::SetScrollFromPosX(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetScrollFromPosY(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  0.5f;

  
  ImGui::SetScrollFromPosY(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushFont(PyObject *self, PyObject *args) {
  // PointerToStructType: ImFont*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImFont *p0 = ctypes_get_pointer<ImFont*>(t0);

  
  ImGui::PushFont(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopFont(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopFont();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushStyleColor(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  ImGui::PushStyleColor(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushStyleColor_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec4 *p1 = ctypes_get_pointer<ImVec4*>(t1);

  
  ImGui::PushStyleColor(p0, *p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopStyleColor(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  1;

  
  ImGui::PopStyleColor(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushStyleVar(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  ImGui::PushStyleVar(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushStyleVar_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImGui::PushStyleVar(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopStyleVar(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  1;

  
  ImGui::PopStyleVar(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushAllowKeyboardFocus(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  bool p0 = t0 == Py_True;

  
  ImGui::PushAllowKeyboardFocus(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopAllowKeyboardFocus(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopAllowKeyboardFocus();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushButtonRepeat(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  bool p0 = t0 == Py_True;

  
  ImGui::PushButtonRepeat(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopButtonRepeat(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopButtonRepeat();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushItemWidth(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::PushItemWidth(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopItemWidth(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopItemWidth();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextItemWidth(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetNextItemWidth(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_CalcItemWidth(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::CalcItemWidth();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushTextWrapPos(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.0f;

  
  ImGui::PushTextWrapPos(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopTextWrapPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopTextWrapPos();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFont(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFont();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFontSize(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFontSize();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFontTexUvWhitePixel(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFontTexUvWhitePixel();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColorU32(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  1.0f;

  
  auto value = ImGui::GetColorU32(p0, p1);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColorU32_2(PyObject *self, PyObject *args) {
  // ReferenceToStructType: ImVec4&
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec4 *p0 = ctypes_get_pointer<ImVec4*>(t0);

  
  auto value = ImGui::GetColorU32(*p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColorU32_3(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  auto value = ImGui::GetColorU32(p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetStyleColorVec4(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  // ReferenceToStructType: ImVec4&
auto value = &ImGui::GetStyleColorVec4(p0);
auto py_value = c_void_p(value);
py_value = ctypes_cast(py_value, "ImVec4", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_Separator(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::Separator();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SameLine(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.0f;

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  - 1.0f;

  
  ImGui::SameLine(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_NewLine(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::NewLine();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Spacing(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::Spacing();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Dummy(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImGui::Dummy(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Indent(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.0f;

  
  ImGui::Indent(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Unindent(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  float p0 = t0 ? PyFloat_AsDouble(t0) :  0.0f;

  
  ImGui::Unindent(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginGroup(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::BeginGroup();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndGroup(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndGroup();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCursorPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCursorPos();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCursorPosX(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCursorPosX();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCursorPosY(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCursorPosY();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetCursorPos(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImGui::SetCursorPos(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetCursorPosX(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetCursorPosX(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetCursorPosY(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImGui::SetCursorPosY(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCursorStartPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCursorStartPos();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetCursorScreenPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetCursorScreenPos();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetCursorScreenPos(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImGui::SetCursorScreenPos(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_AlignTextToFramePadding(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::AlignTextToFramePadding();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetTextLineHeight(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetTextLineHeight();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetTextLineHeightWithSpacing(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetTextLineHeightWithSpacing();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFrameHeight(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFrameHeight();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFrameHeightWithSpacing(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFrameHeightWithSpacing();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushID(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::PushID(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushID_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  ImGui::PushID(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushID_3(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const void *p0 = ctypes_get_pointer<const void*>(t0);

  
  ImGui::PushID(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushID_4(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImGui::PushID(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopID(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopID();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetID(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  auto value = ImGui::GetID(p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetID_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  auto value = ImGui::GetID(p0, p1);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetID_3(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const void *p0 = ctypes_get_pointer<const void*>(t0);

  
  auto value = ImGui::GetID(p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TextUnformatted(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1,  NULL);

  
  ImGui::TextUnformatted(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Text(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::Text(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TextColored(PyObject *self, PyObject *args) {
  // ReferenceToStructType: ImVec4&
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  ImVec4 *p0 = ctypes_get_pointer<ImVec4*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  ImGui::TextColored(*p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TextDisabled(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::TextDisabled(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TextWrapped(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::TextWrapped(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LabelText(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  ImGui::LabelText(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BulletText(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::BulletText(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Button(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::Button(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SmallButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  auto value = ImGui::SmallButton(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InvisibleButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::InvisibleButton(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ArrowButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = ImGui::ArrowButton(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_Image(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t4 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImVec2 p2 = t2 ? get_ImVec2(t2) :  ImVec2 ( 0 , 0 );

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 1 , 1 );

  
  ImVec4& default_value4 =  ImVec4 ( 1 , 1 , 1 , 1 );
ImVec4 *p4 = t4 ? ctypes_get_pointer<ImVec4*>(t4) : &default_value4;

  
  ImVec4& default_value5 =  ImVec4 ( 0 , 0 , 0 , 0 );
ImVec4 *p5 = t5 ? ctypes_get_pointer<ImVec4*>(t5) : &default_value5;

  
  ImGui::Image(p0, p1, p2, p3, *p4, *p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ImageButton(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t5 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImVec2 p2 = t2 ? get_ImVec2(t2) :  ImVec2 ( 0 , 0 );

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 1 , 1 );

  
  int p4 = t4 ? PyLong_AsLong(t4) :  - 1;

  
  ImVec4& default_value5 =  ImVec4 ( 0 , 0 , 0 , 0 );
ImVec4 *p5 = t5 ? ctypes_get_pointer<ImVec4*>(t5) : &default_value5;

  
  ImVec4& default_value6 =  ImVec4 ( 1 , 1 , 1 , 1 );
ImVec4 *p6 = t6 ? ctypes_get_pointer<ImVec4*>(t6) : &default_value6;

  
  auto value = ImGui::ImageButton(p0, p1, p2, p3, p4, *p5, *p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_Checkbox(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = ctypes_get_pointer<bool*>(t1);

  
  auto value = ImGui::Checkbox(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_RadioButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool p1 = t1 == Py_True;

  
  auto value = ImGui::RadioButton(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_RadioButton_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  auto value = ImGui::RadioButton(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ProgressBar(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "O|OO", &t0, &t1, &t2))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( - FLT_MIN , 0 );

  
  const char *p2 = get_cstring(t2,  NULL);

  
  ImGui::ProgressBar(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Bullet(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::Bullet();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginCombo(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::BeginCombo(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndCombo(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndCombo();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0f;

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  const char *p5 = get_cstring(t5,  "%.3f");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragFloat(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[2]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0f;

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  const char *p5 = get_cstring(t5,  "%.3f");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragFloat2(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0f;

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  const char *p5 = get_cstring(t5,  "%.3f");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragFloat3(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0f;

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  const char *p5 = get_cstring(t5,  "%.3f");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragFloat4(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloatRange2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // PointerType: float*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // CStringType: const char *
PyObject *t7 = NULL;

  
  // Int32Type: int
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float *p2 = ctypes_get_pointer<float*>(t2);

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  1.0f;

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  float p5 = t5 ? PyFloat_AsDouble(t5) :  0.0f;

  
  const char *p6 = get_cstring(t6,  "%.3f");

  
  const char *p7 = get_cstring(t7,  NULL);

  
  int p8 = t8 ? PyLong_AsLong(t8) :  0;

  
  auto value = ImGui::DragFloatRange2(p0, p1, p2, p3, p4, p5, p6, p7, p8);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragInt(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  const char *p5 = get_cstring(t5,  "%d");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragInt(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragInt2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[2]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  const char *p5 = get_cstring(t5,  "%d");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragInt2(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragInt3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[3]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  const char *p5 = get_cstring(t5,  "%d");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragInt3(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragInt4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[4]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  1.0f;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  const char *p5 = get_cstring(t5,  "%d");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::DragInt4(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragIntRange2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // CStringType: const char *
PyObject *t7 = NULL;

  
  // Int32Type: int
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  1.0f;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  const char *p6 = get_cstring(t6,  "%d");

  
  const char *p7 = get_cstring(t7,  NULL);

  
  int p8 = t8 ? PyLong_AsLong(t8) :  0;

  
  auto value = ImGui::DragIntRange2(p0, p1, p2, p3, p4, p5, p6, p7, p8);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragScalar(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  1.0f;

  
  const void *p4 = t4 ? ctypes_get_pointer<const void*>(t4) :  NULL;

  
  const void *p5 = t5 ? ctypes_get_pointer<const void*>(t5) :  NULL;

  
  const char *p6 = get_cstring(t6,  NULL);

  
  int p7 = t7 ? PyLong_AsLong(t7) :  0;

  
  auto value = ImGui::DragScalar(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragScalarN(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // PointerType: void*
PyObject *t6 = NULL;

  
  // CStringType: const char *
PyObject *t7 = NULL;

  
  // Int32Type: int
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  1.0f;

  
  const void *p5 = t5 ? ctypes_get_pointer<const void*>(t5) :  NULL;

  
  const void *p6 = t6 ? ctypes_get_pointer<const void*>(t6) :  NULL;

  
  const char *p7 = get_cstring(t7,  NULL);

  
  int p8 = t8 ? PyLong_AsLong(t8) :  0;

  
  auto value = ImGui::DragScalarN(p0, p1, p2, p3, p4, p5, p6, p7, p8);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4,  "%.3f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderFloat(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[2]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4,  "%.3f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderFloat2(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4,  "%.3f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderFloat3(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4,  "%.3f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderFloat4(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderAngle(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  - 360.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  + 360.0f;

  
  const char *p4 = get_cstring(t4,  "%.0f deg");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderAngle(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderInt(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const char *p4 = get_cstring(t4,  "%d");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderInt(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderInt2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[2]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const char *p4 = get_cstring(t4,  "%d");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderInt2(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderInt3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[3]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const char *p4 = get_cstring(t4,  "%d");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderInt3(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderInt4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[4]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const char *p4 = get_cstring(t4,  "%d");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::SliderInt4(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderScalar(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // PointerType: void*
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  const void *p3 = ctypes_get_pointer<const void*>(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const char *p5 = get_cstring(t5,  NULL);

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::SliderScalar(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderScalarN(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const void *p5 = ctypes_get_pointer<const void*>(t5);

  
  const char *p6 = get_cstring(t6,  NULL);

  
  int p7 = t7 ? PyLong_AsLong(t7) :  0;

  
  auto value = ImGui::SliderScalarN(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_VSliderFloat(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // PointerType: float*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  float *p2 = ctypes_get_pointer<float*>(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const char *p5 = get_cstring(t5,  "%.3f");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::VSliderFloat(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_VSliderInt(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  const char *p5 = get_cstring(t5,  "%d");

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::VSliderInt(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_VSliderScalar(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // PointerType: void*
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO|OO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  void *p3 = ctypes_get_pointer<void*>(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const void *p5 = ctypes_get_pointer<const void*>(t5);

  
  const char *p6 = get_cstring(t6,  NULL);

  
  int p7 = t7 ? PyLong_AsLong(t7) :  0;

  
  auto value = ImGui::VSliderScalar(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputFloat(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  0.0f;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0f;

  
  const char *p4 = get_cstring(t4,  "%.3f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::InputFloat(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputFloat2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[2]
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  const char *p2 = get_cstring(t2,  "%.3f");

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::InputFloat2(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputFloat3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  const char *p2 = get_cstring(t2,  "%.3f");

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::InputFloat3(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputFloat4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  const char *p2 = get_cstring(t2,  "%.3f");

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::InputFloat4(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputInt(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  1;

  
  int p3 = t3 ? PyLong_AsLong(t3) :  100;

  
  int p4 = t4 ? PyLong_AsLong(t4) :  0;

  
  auto value = ImGui::InputInt(p0, p1, p2, p3, p4);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputInt2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[2]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::InputInt2(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputInt3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[3]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::InputInt3(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputInt4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: int[4]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::InputInt4(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputDouble(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: double*
PyObject *t1 = NULL;

  
  // DoubleType: double
PyObject *t2 = NULL;

  
  // DoubleType: double
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  double *p1 = ctypes_get_pointer<double*>(t1);

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  0.0;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  0.0;

  
  const char *p4 = get_cstring(t4,  "%.6f");

  
  int p5 = t5 ? PyLong_AsLong(t5) :  0;

  
  auto value = ImGui::InputDouble(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputScalar(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // PointerType: void*
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  const void *p3 = t3 ? ctypes_get_pointer<const void*>(t3) :  NULL;

  
  const void *p4 = t4 ? ctypes_get_pointer<const void*>(t4) :  NULL;

  
  const char *p5 = get_cstring(t5,  NULL);

  
  int p6 = t6 ? PyLong_AsLong(t6) :  0;

  
  auto value = ImGui::InputScalar(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_InputScalarN(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|OOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const void *p4 = t4 ? ctypes_get_pointer<const void*>(t4) :  NULL;

  
  const void *p5 = t5 ? ctypes_get_pointer<const void*>(t5) :  NULL;

  
  const char *p6 = get_cstring(t6,  NULL);

  
  int p7 = t7 ? PyLong_AsLong(t7) :  0;

  
  auto value = ImGui::InputScalarN(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorEdit3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::ColorEdit3(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorEdit4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::ColorEdit4(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorPicker3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::ColorPicker3(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorPicker4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // PointerType: float*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  const float *p3 = t3 ? ctypes_get_pointer<const float*>(t3) :  NULL;

  
  auto value = ImGui::ColorPicker4(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ReferenceToStructType: ImVec4&
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec4 *p1 = ctypes_get_pointer<ImVec4*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::ColorButton(p0, *p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetColorEditOptions(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImGui::SetColorEditOptions(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNode(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  auto value = ImGui::TreeNode(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNode_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  auto value = ImGui::TreeNode(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNode_3(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const void *p0 = ctypes_get_pointer<const void*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  auto value = ImGui::TreeNode(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNodeEx(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::TreeNodeEx(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNodeEx_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  auto value = ImGui::TreeNodeEx(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeNodeEx_3(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  const void *p0 = ctypes_get_pointer<const void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  auto value = ImGui::TreeNodeEx(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreePush(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::TreePush(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreePush_2(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  const void *p0 = t0 ? ctypes_get_pointer<const void*>(t0) :  NULL;

  
  ImGui::TreePush(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreePop(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::TreePop();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetTreeNodeToLabelSpacing(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetTreeNodeToLabelSpacing();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_CollapsingHeader(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::CollapsingHeader(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_CollapsingHeader_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = ctypes_get_pointer<bool*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::CollapsingHeader(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextItemOpen(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  bool p0 = t0 == Py_True;

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetNextItemOpen(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Selectable(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool p1 = t1 ? t1 == Py_True :  false;

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::Selectable(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_Selectable_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = ctypes_get_pointer<bool*>(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::Selectable(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginListBox(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::BeginListBox(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndListBox(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndListBox();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PlotHistogram(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t7 = NULL;

  
  // Int32Type: int
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const float *p1 = ctypes_get_pointer<const float*>(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  const char *p4 = get_cstring(t4,  NULL);

  
  float p5 = t5 ? PyFloat_AsDouble(t5) :  FLT_MAX;

  
  float p6 = t6 ? PyFloat_AsDouble(t6) :  FLT_MAX;

  
  ImVec2 p7 = t7 ? get_ImVec2(t7) :  ImVec2 ( 0 , 0 );

  
  int p8 = t8 ? PyLong_AsLong(t8) :  sizeof ( float );

  
  ImGui::PlotHistogram(p0, p1, p2, p3, p4, p5, p6, p7, p8);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Value(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool p1 = t1 == Py_True;

  
  ImGui::Value(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Value_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  ImGui::Value(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Value_3(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  ImGui::Value(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Value_4(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float p1 = PyFloat_AsDouble(t1);

  
  const char *p2 = get_cstring(t2,  NULL);

  
  ImGui::Value(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginMenuBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::BeginMenuBar();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndMenuBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndMenuBar();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginMainMenuBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::BeginMainMenuBar();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndMainMenuBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndMainMenuBar();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginMenu(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool p1 = t1 ? t1 == Py_True :  true;

  
  auto value = ImGui::BeginMenu(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndMenu(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndMenu();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_MenuItem(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  
  // BoolType: bool
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1,  NULL);

  
  bool p2 = t2 ? t2 == Py_True :  false;

  
  bool p3 = t3 ? t3 == Py_True :  true;

  
  auto value = ImGui::MenuItem(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_MenuItem_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // PointerType: bool*
PyObject *t2 = NULL;

  
  // BoolType: bool
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|O", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  bool *p2 = ctypes_get_pointer<bool*>(t2);

  
  bool p3 = t3 ? t3 == Py_True :  true;

  
  auto value = ImGui::MenuItem(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginTooltip(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::BeginTooltip();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndTooltip(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndTooltip();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetTooltip(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::SetTooltip(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopup(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::BeginPopup(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopupModal(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "O|OO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = t1 ? ctypes_get_pointer<bool*>(t1) :  NULL;

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::BeginPopupModal(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndPopup(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndPopup();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_OpenPopup(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::OpenPopup(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_OpenPopup_2(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::OpenPopup(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_OpenPopupOnItemClick(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0,  NULL);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  1;

  
  ImGui::OpenPopupOnItemClick(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_CloseCurrentPopup(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::CloseCurrentPopup();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopupContextItem(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0,  NULL);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  1;

  
  auto value = ImGui::BeginPopupContextItem(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopupContextWindow(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0,  NULL);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  1;

  
  auto value = ImGui::BeginPopupContextWindow(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopupContextVoid(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0,  NULL);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  1;

  
  auto value = ImGui::BeginPopupContextVoid(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsPopupOpen(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::IsPopupOpen(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginTable(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OO|OOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  ImVec2 p3 = t3 ? get_ImVec2(t3) :  ImVec2 ( 0.0f , 0.0f );

  
  float p4 = t4 ? PyFloat_AsDouble(t4) :  0.0f;

  
  auto value = ImGui::BeginTable(p0, p1, p2, p3, p4);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndTable(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndTable();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableNextRow(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  0.0f;

  
  ImGui::TableNextRow(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableNextColumn(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::TableNextColumn();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableSetColumnIndex(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::TableSetColumnIndex(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableSetupColumn(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  float p2 = t2 ? PyFloat_AsDouble(t2) :  0.0f;

  
  unsigned int p3 = t3 ? PyLong_AsUnsignedLong(t3) :  0;

  
  ImGui::TableSetupColumn(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableSetupScrollFreeze(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  ImGui::TableSetupScrollFreeze(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableHeadersRow(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::TableHeadersRow();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableHeader(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::TableHeader(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetSortSpecs(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::TableGetSortSpecs();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetColumnCount(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::TableGetColumnCount();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetColumnIndex(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::TableGetColumnIndex();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetRowIndex(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::TableGetRowIndex();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetColumnName(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  auto value = ImGui::TableGetColumnName(p0);
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableGetColumnFlags(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  auto value = ImGui::TableGetColumnFlags(p0);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableSetColumnEnabled(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  bool p1 = t1 == Py_True;

  
  ImGui::TableSetColumnEnabled(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TableSetBgColor(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  - 1;

  
  ImGui::TableSetBgColor(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_Columns(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "|OOO", &t0, &t1, &t2))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  1;

  
  const char *p1 = get_cstring(t1,  NULL);

  
  bool p2 = t2 ? t2 == Py_True :  true;

  
  ImGui::Columns(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_NextColumn(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::NextColumn();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColumnIndex(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetColumnIndex();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColumnWidth(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  auto value = ImGui::GetColumnWidth(p0);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetColumnWidth(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  ImGui::SetColumnWidth(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColumnOffset(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  auto value = ImGui::GetColumnOffset(p0);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetColumnOffset(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  ImGui::SetColumnOffset(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetColumnsCount(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetColumnsCount();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginTabBar(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::BeginTabBar(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndTabBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndTabBar();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginTabItem(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: bool*
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "O|OO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  bool *p1 = t1 ? ctypes_get_pointer<bool*>(t1) :  NULL;

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::BeginTabItem(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndTabItem(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndTabItem();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_TabItemButton(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::TabItemButton(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetTabItemClosed(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::SetTabItemClosed(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_DockSpace(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // PointerToStructType: ImGuiWindowClass*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  const ImGuiWindowClass *p3 = t3 ? ctypes_get_pointer<const ImGuiWindowClass*>(t3) :  NULL;

  
  auto value = ImGui::DockSpace(p0, p1, p2, p3);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DockSpaceOverViewport(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiViewport*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerToStructType: ImGuiWindowClass*
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "|OOO", &t0, &t1, &t2))
    return NULL;
  const ImGuiViewport *p0 = t0 ? ctypes_get_pointer<const ImGuiViewport*>(t0) :  NULL;

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  const ImGuiWindowClass *p2 = t2 ? ctypes_get_pointer<const ImGuiWindowClass*>(t2) :  NULL;

  
  auto value = ImGui::DockSpaceOverViewport(p0, p1, p2);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowDockID(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetNextWindowDockID(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextWindowClass(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiWindowClass*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const ImGuiWindowClass *p0 = ctypes_get_pointer<const ImGuiWindowClass*>(t0);

  
  ImGui::SetNextWindowClass(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowDockID(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowDockID();
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsWindowDocked(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsWindowDocked();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogToTTY(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  ImGui::LogToTTY(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogToFile(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  const char *p1 = get_cstring(t1,  NULL);

  
  ImGui::LogToFile(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogToClipboard(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  - 1;

  
  ImGui::LogToClipboard(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogFinish(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::LogFinish();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogButtons(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::LogButtons();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LogText(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::LogText(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginDragDropSource(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  auto value = ImGui::BeginDragDropSource(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetDragDropPayload(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: void*
PyObject *t1 = NULL;

  
  // SizeType: size_t
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOO|O", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const void *p1 = ctypes_get_pointer<const void*>(t1);

  
  size_t p2 = PyLong_AsSize_t(t2);

  
  int p3 = t3 ? PyLong_AsLong(t3) :  0;

  
  auto value = ImGui::SetDragDropPayload(p0, p1, p2, p3);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndDragDropSource(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndDragDropSource();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginDragDropTarget(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::BeginDragDropTarget();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_AcceptDragDropPayload(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  auto value = ImGui::AcceptDragDropPayload(p0, p1);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndDragDropTarget(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndDragDropTarget();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetDragDropPayload(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetDragDropPayload();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginDisabled(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool p0 = t0 ? t0 == Py_True :  true;

  
  ImGui::BeginDisabled(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndDisabled(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndDisabled();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PushClipRect(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  bool p2 = t2 == Py_True;

  
  ImGui::PushClipRect(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_PopClipRect(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::PopClipRect();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetItemDefaultFocus(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::SetItemDefaultFocus();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetKeyboardFocusHere(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  ImGui::SetKeyboardFocusHere(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemHovered(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  auto value = ImGui::IsItemHovered(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemActive(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemActive();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemFocused(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemFocused();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemClicked(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  auto value = ImGui::IsItemClicked(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemVisible(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemVisible();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemEdited(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemEdited();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemActivated(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemActivated();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemDeactivated(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemDeactivated();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemDeactivatedAfterEdit(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemDeactivatedAfterEdit();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsItemToggledOpen(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsItemToggledOpen();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsAnyItemHovered(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsAnyItemHovered();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsAnyItemActive(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsAnyItemActive();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsAnyItemFocused(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsAnyItemFocused();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetItemRectMin(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetItemRectMin();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetItemRectMax(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetItemRectMax();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetItemRectSize(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetItemRectSize();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetItemAllowOverlap(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::SetItemAllowOverlap();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMainViewport(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetMainViewport();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiViewport", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsRectVisible(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  auto value = ImGui::IsRectVisible(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsRectVisible_2(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  auto value = ImGui::IsRectVisible(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetTime(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetTime();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetFrameCount(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetFrameCount();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetBackgroundDrawList(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetBackgroundDrawList();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawList", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetForegroundDrawList(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetForegroundDrawList();
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawList", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetBackgroundDrawList_2(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiViewport*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImGuiViewport *p0 = ctypes_get_pointer<ImGuiViewport*>(t0);

  
  auto value = ImGui::GetBackgroundDrawList(p0);
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawList", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetForegroundDrawList_2(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiViewport*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImGuiViewport *p0 = ctypes_get_pointer<ImGuiViewport*>(t0);

  
  auto value = ImGui::GetForegroundDrawList(p0);
PyObject* py_value = ctypes_cast(c_void_p(value), "ImDrawList", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetDrawListSharedData(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetDrawListSharedData();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetStyleColorName(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::GetStyleColorName(p0);
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginChildFrame(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  0;

  
  auto value = ImGui::BeginChildFrame(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_EndChildFrame(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::EndChildFrame();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_CalcTextSize(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "O|OOO", &t0, &t1, &t2, &t3))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  const char *p1 = get_cstring(t1,  NULL);

  
  bool p2 = t2 ? t2 == Py_True :  false;

  
  float p3 = t3 ? PyFloat_AsDouble(t3) :  - 1.0f;

  
  auto value = ImGui::CalcTextSize(p0, p1, p2, p3);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorConvertU32ToFloat4(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  auto value = ImGui::ColorConvertU32ToFloat4(p0);
PyObject* py_value = Py_BuildValue("(ffff)", value.x, value.y, value.z, value.w);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorConvertFloat4ToU32(PyObject *self, PyObject *args) {
  // ReferenceToStructType: ImVec4&
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec4 *p0 = ctypes_get_pointer<ImVec4*>(t0);

  
  auto value = ImGui::ColorConvertFloat4ToU32(*p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorConvertRGBtoHSV(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // ReferenceType: float&
PyObject *t3 = NULL;

  
  // ReferenceType: float&
PyObject *t4 = NULL;

  
  // ReferenceType: float&
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float *p3 = ctypes_get_pointer<float*>(t3);

  
  float *p4 = ctypes_get_pointer<float*>(t4);

  
  float *p5 = ctypes_get_pointer<float*>(t5);

  
  ImGui::ColorConvertRGBtoHSV(p0, p1, p2, *p3, *p4, *p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_ColorConvertHSVtoRGB(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // ReferenceType: float&
PyObject *t3 = NULL;

  
  // ReferenceType: float&
PyObject *t4 = NULL;

  
  // ReferenceType: float&
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float *p3 = ctypes_get_pointer<float*>(t3);

  
  float *p4 = ctypes_get_pointer<float*>(t4);

  
  float *p5 = ctypes_get_pointer<float*>(t5);

  
  ImGui::ColorConvertHSVtoRGB(p0, p1, p2, *p3, *p4, *p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetKeyIndex(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::GetKeyIndex(p0);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsKeyDown(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::IsKeyDown(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsKeyPressed(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  bool p1 = t1 ? t1 == Py_True :  true;

  
  auto value = ImGui::IsKeyPressed(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsKeyReleased(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::IsKeyReleased(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetKeyPressedAmount(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  auto value = ImGui::GetKeyPressedAmount(p0, p1, p2);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_CaptureKeyboardFromApp(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool p0 = t0 ? t0 == Py_True :  true;

  
  ImGui::CaptureKeyboardFromApp(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseDown(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::IsMouseDown(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseClicked(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  bool p1 = t1 ? t1 == Py_True :  false;

  
  auto value = ImGui::IsMouseClicked(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseReleased(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::IsMouseReleased(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseDoubleClicked(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::IsMouseDoubleClicked(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMouseClickedCount(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImGui::GetMouseClickedCount(p0);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseHoveringRect(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  bool p2 = t2 ? t2 == Py_True :  true;

  
  auto value = ImGui::IsMouseHoveringRect(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMousePosValid(PyObject *self, PyObject *args) {
  // PointerToStructType: ImVec2*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  const ImVec2 *p0 = t0 ? ctypes_get_pointer<const ImVec2*>(t0) :  NULL;

  
  auto value = ImGui::IsMousePosValid(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsAnyMouseDown(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::IsAnyMouseDown();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMousePos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetMousePos();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMousePosOnOpeningCurrentPopup(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetMousePosOnOpeningCurrentPopup();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_IsMouseDragging(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  - 1.0f;

  
  auto value = ImGui::IsMouseDragging(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMouseDragDelta(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  float p1 = t1 ? PyFloat_AsDouble(t1) :  - 1.0f;

  
  auto value = ImGui::GetMouseDragDelta(p0, p1);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ResetMouseDragDelta(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  0;

  
  ImGui::ResetMouseDragDelta(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetMouseCursor(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetMouseCursor();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetMouseCursor(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImGui::SetMouseCursor(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_CaptureMouseFromApp(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  bool p0 = t0 ? t0 == Py_True :  true;

  
  ImGui::CaptureMouseFromApp(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetClipboardText(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetClipboardText();
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetClipboardText(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::SetClipboardText(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LoadIniSettingsFromDisk(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::LoadIniSettingsFromDisk(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_LoadIniSettingsFromMemory(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // SizeType: size_t
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  size_t p1 = t1 ? PyLong_AsSize_t(t1) :  0;

  
  ImGui::LoadIniSettingsFromMemory(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SaveIniSettingsToDisk(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImGui::SaveIniSettingsToDisk(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SaveIniSettingsToMemory(PyObject *self, PyObject *args) {
  // PointerType: size_t*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  size_t *p0 = t0 ? ctypes_get_pointer<size_t*>(t0) :  NULL;

  
  auto value = ImGui::SaveIniSettingsToMemory(p0);
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DebugCheckVersionAndDataLayout(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // SizeType: size_t
PyObject *t1 = NULL;

  
  // SizeType: size_t
PyObject *t2 = NULL;

  
  // SizeType: size_t
PyObject *t3 = NULL;

  
  // SizeType: size_t
PyObject *t4 = NULL;

  
  // SizeType: size_t
PyObject *t5 = NULL;

  
  // SizeType: size_t
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  size_t p1 = PyLong_AsSize_t(t1);

  
  size_t p2 = PyLong_AsSize_t(t2);

  
  size_t p3 = PyLong_AsSize_t(t3);

  
  size_t p4 = PyLong_AsSize_t(t4);

  
  size_t p5 = PyLong_AsSize_t(t5);

  
  size_t p6 = PyLong_AsSize_t(t6);

  
  auto value = ImGui::DebugCheckVersionAndDataLayout(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_MemAlloc(PyObject *self, PyObject *args) {
  // SizeType: size_t
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  size_t p0 = PyLong_AsSize_t(t0);

  
  auto value = ImGui::MemAlloc(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_MemFree(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  ImGui::MemFree(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetPlatformIO(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  // ReferenceType: ImGuiPlatformIO&
auto *value = &ImGui::GetPlatformIO();
auto py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_UpdatePlatformWindows(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::UpdatePlatformWindows();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_RenderPlatformWindowsDefault(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // PointerType: void*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  void *p0 = t0 ? ctypes_get_pointer<void*>(t0) :  NULL;

  
  void *p1 = t1 ? ctypes_get_pointer<void*>(t1) :  NULL;

  
  ImGui::RenderPlatformWindowsDefault(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_DestroyPlatformWindows(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::DestroyPlatformWindows();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_FindViewportByID(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  auto value = ImGui::FindViewportByID(p0);
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiViewport", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_FindViewportByPlatformHandle(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  auto value = ImGui::FindViewportByPlatformHandle(p0);
PyObject* py_value = ctypes_cast(c_void_p(value), "ImGuiViewport", "imgui");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_CalcListClipping(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // PointerType: int*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  int *p3 = ctypes_get_pointer<int*>(t3);

  
  ImGui::CalcListClipping(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetWindowContentRegionWidth(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetWindowContentRegionWidth();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ListBoxHeader(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = t2 ? PyLong_AsLong(t2) :  - 1;

  
  auto value = ImGui::ListBoxHeader(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ListBoxHeader_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImVec2 p1 = t1 ? get_ImVec2(t1) :  ImVec2 ( 0 , 0 );

  
  auto value = ImGui::ListBoxHeader(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_ListBoxFooter(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::ListBoxFooter();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_OpenPopupContextItem(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0,  NULL);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  1;

  
  ImGui::OpenPopupContextItem(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragScalar_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // FloatType: float
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const void *p5 = ctypes_get_pointer<const void*>(t5);

  
  const char *p6 = get_cstring(t6, nullptr);

  
  float p7 = PyFloat_AsDouble(t7);

  
  auto value = ImGui::DragScalar(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragScalarN_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // PointerType: void*
PyObject *t6 = NULL;

  
  // CStringType: const char *
PyObject *t7 = NULL;

  
  // FloatType: float
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const void *p5 = ctypes_get_pointer<const void*>(t5);

  
  const void *p6 = ctypes_get_pointer<const void*>(t6);

  
  const char *p7 = get_cstring(t7, nullptr);

  
  float p8 = PyFloat_AsDouble(t8);

  
  auto value = ImGui::DragScalarN(p0, p1, p2, p3, p4, p5, p6, p7, p8);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = ImGui::DragFloat(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat2_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[2]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = ImGui::DragFloat2(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat3_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = ImGui::DragFloat3(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_DragFloat4_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = ImGui::DragFloat4(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderScalar_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // PointerType: void*
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  const void *p3 = ctypes_get_pointer<const void*>(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = ImGui::SliderScalar(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderScalarN_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: void*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // PointerType: void*
PyObject *t4 = NULL;

  
  // PointerType: void*
PyObject *t5 = NULL;

  
  // CStringType: const char *
PyObject *t6 = NULL;

  
  // FloatType: float
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  void *p2 = ctypes_get_pointer<void*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const void *p4 = ctypes_get_pointer<const void*>(t4);

  
  const void *p5 = ctypes_get_pointer<const void*>(t5);

  
  const char *p6 = get_cstring(t6, nullptr);

  
  float p7 = PyFloat_AsDouble(t7);

  
  auto value = ImGui::SliderScalarN(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  float p5 = PyFloat_AsDouble(t5);

  
  auto value = ImGui::SliderFloat(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat2_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[2]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  float p5 = PyFloat_AsDouble(t5);

  
  auto value = ImGui::SliderFloat2(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat3_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[3]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  float p5 = PyFloat_AsDouble(t5);

  
  auto value = ImGui::SliderFloat3(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_SliderFloat4_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // ArrayType: float[4]
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  float p5 = PyFloat_AsDouble(t5);

  
  auto value = ImGui::SliderFloat4(p0, p1, p2, p3, p4, p5);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_BeginPopupContextWindow_2(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // BoolType: bool
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  int p1 = PyLong_AsLong(t1);

  
  bool p2 = t2 == Py_True;

  
  auto value = ImGui::BeginPopupContextWindow(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imgui_TreeAdvanceToLabelPos(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImGui::TreeAdvanceToLabelPos();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_SetNextTreeNodeOpen(PyObject *self, PyObject *args) {
  // BoolType: bool
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  bool p0 = t0 == Py_True;

  
  int p1 = t1 ? PyLong_AsLong(t1) :  0;

  
  ImGui::SetNextTreeNodeOpen(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imgui_GetContentRegionAvailWidth(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImGui::GetContentRegionAvailWidth();
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
static PyObject *ImFontAtlas_AddFont(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t0 = NULL;
  if(!PyArg_ParseTuple(args, "OO", &py_this, &t0)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const ImFontConfig *p0 = ctypes_get_pointer<const ImFontConfig*>(t0);
  auto value = ptr->AddFont(p0);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_AddFontDefault(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t0 = NULL;
  if(!PyArg_ParseTuple(args, "O|O", &py_this, &t0)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const ImFontConfig *p0 = t0 ? ctypes_get_pointer<const ImFontConfig*>(t0) :  NULL;
  auto value = ptr->AddFontDefault(p0);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_AddFontFromFileTTF(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // CStringType: const char *
  PyObject *t0 = NULL;
  // FloatType: float
  PyObject *t1 = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t2 = NULL;
  // PointerType: unsigned short*
  PyObject *t3 = NULL;
  if(!PyArg_ParseTuple(args, "OOO|OO", &py_this, &t0, &t1, &t2, &t3)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const char *p0 = get_cstring(t0, nullptr);
  float p1 = PyFloat_AsDouble(t1);
  const ImFontConfig *p2 = t2 ? ctypes_get_pointer<const ImFontConfig*>(t2) :  NULL;
  const unsigned short *p3 = t3 ? ctypes_get_pointer<const unsigned short*>(t3) :  NULL;
  auto value = ptr->AddFontFromFileTTF(p0, p1, p2, p3);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_AddFontFromMemoryTTF(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerType: void*
  PyObject *t0 = NULL;
  // Int32Type: int
  PyObject *t1 = NULL;
  // FloatType: float
  PyObject *t2 = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t3 = NULL;
  // PointerType: unsigned short*
  PyObject *t4 = NULL;
  if(!PyArg_ParseTuple(args, "OOOO|OO", &py_this, &t0, &t1, &t2, &t3, &t4)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  void *p0 = ctypes_get_pointer<void*>(t0);
  int p1 = PyLong_AsLong(t1);
  float p2 = PyFloat_AsDouble(t2);
  const ImFontConfig *p3 = t3 ? ctypes_get_pointer<const ImFontConfig*>(t3) :  NULL;
  const unsigned short *p4 = t4 ? ctypes_get_pointer<const unsigned short*>(t4) :  NULL;
  auto value = ptr->AddFontFromMemoryTTF(p0, p1, p2, p3, p4);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_AddFontFromMemoryCompressedTTF(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerType: void*
  PyObject *t0 = NULL;
  // Int32Type: int
  PyObject *t1 = NULL;
  // FloatType: float
  PyObject *t2 = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t3 = NULL;
  // PointerType: unsigned short*
  PyObject *t4 = NULL;
  if(!PyArg_ParseTuple(args, "OOOO|OO", &py_this, &t0, &t1, &t2, &t3, &t4)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const void *p0 = ctypes_get_pointer<const void*>(t0);
  int p1 = PyLong_AsLong(t1);
  float p2 = PyFloat_AsDouble(t2);
  const ImFontConfig *p3 = t3 ? ctypes_get_pointer<const ImFontConfig*>(t3) :  NULL;
  const unsigned short *p4 = t4 ? ctypes_get_pointer<const unsigned short*>(t4) :  NULL;
  auto value = ptr->AddFontFromMemoryCompressedTTF(p0, p1, p2, p3, p4);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_AddFontFromMemoryCompressedBase85TTF(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // CStringType: const char *
  PyObject *t0 = NULL;
  // FloatType: float
  PyObject *t1 = NULL;
  // PointerToStructType: ImFontConfig*
  PyObject *t2 = NULL;
  // PointerType: unsigned short*
  PyObject *t3 = NULL;
  if(!PyArg_ParseTuple(args, "OOO|OO", &py_this, &t0, &t1, &t2, &t3)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const char *p0 = get_cstring(t0, nullptr);
  float p1 = PyFloat_AsDouble(t1);
  const ImFontConfig *p2 = t2 ? ctypes_get_pointer<const ImFontConfig*>(t2) :  NULL;
  const unsigned short *p3 = t3 ? ctypes_get_pointer<const unsigned short*>(t3) :  NULL;
  auto value = ptr->AddFontFromMemoryCompressedBase85TTF(p0, p1, p2, p3);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFont", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_ClearInputData(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  ptr->ClearInputData();
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_ClearTexData(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  ptr->ClearTexData();
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_ClearFonts(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  ptr->ClearFonts();
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_Clear(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  ptr->Clear();
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_Build(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->Build();
  PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
  return py_value;
}

static PyObject *ImFontAtlas_GetTexDataAsAlpha8(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerType: unsigned char**
  PyObject *t0 = NULL;
  // PointerType: int*
  PyObject *t1 = NULL;
  // PointerType: int*
  PyObject *t2 = NULL;
  // PointerType: int*
  PyObject *t3 = NULL;
  if(!PyArg_ParseTuple(args, "OOOO|O", &py_this, &t0, &t1, &t2, &t3)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  unsigned char* *p0 = ctypes_get_pointer<unsigned char**>(t0);
  int *p1 = ctypes_get_pointer<int*>(t1);
  int *p2 = ctypes_get_pointer<int*>(t2);
  int *p3 = t3 ? ctypes_get_pointer<int*>(t3) :  NULL;
  ptr->GetTexDataAsAlpha8(p0, p1, p2, p3);
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_GetTexDataAsRGBA32(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerType: unsigned char**
  PyObject *t0 = NULL;
  // PointerType: int*
  PyObject *t1 = NULL;
  // PointerType: int*
  PyObject *t2 = NULL;
  // PointerType: int*
  PyObject *t3 = NULL;
  if(!PyArg_ParseTuple(args, "OOOO|O", &py_this, &t0, &t1, &t2, &t3)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  unsigned char* *p0 = ctypes_get_pointer<unsigned char**>(t0);
  int *p1 = ctypes_get_pointer<int*>(t1);
  int *p2 = ctypes_get_pointer<int*>(t2);
  int *p3 = t3 ? ctypes_get_pointer<int*>(t3) :  NULL;
  ptr->GetTexDataAsRGBA32(p0, p1, p2, p3);
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_IsBuilt(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->IsBuilt();
  PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
  return py_value;
}

static PyObject *ImFontAtlas_SetTexID(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerType: void*
  PyObject *t0 = NULL;
  if(!PyArg_ParseTuple(args, "OO", &py_this, &t0)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  void *p0 = ctypes_get_pointer<void*>(t0);
  ptr->SetTexID(p0);
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_GetGlyphRangesDefault(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesDefault();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesKorean(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesKorean();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesJapanese(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesJapanese();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesChineseFull(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesChineseFull();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesChineseSimplifiedCommon(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesChineseSimplifiedCommon();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesCyrillic(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesCyrillic();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesThai(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesThai();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetGlyphRangesVietnamese(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  auto value = ptr->GetGlyphRangesVietnamese();
  PyObject* py_value = c_void_p(value);
  return py_value;
}

static PyObject *ImFontAtlas_AddCustomRectRegular(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // Int32Type: int
  PyObject *t0 = NULL;
  // Int32Type: int
  PyObject *t1 = NULL;
  if(!PyArg_ParseTuple(args, "OOO", &py_this, &t0, &t1)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  int p0 = PyLong_AsLong(t0);
  int p1 = PyLong_AsLong(t1);
  auto value = ptr->AddCustomRectRegular(p0, p1);
  PyObject* py_value = PyLong_FromLong(value);
  return py_value;
}

static PyObject *ImFontAtlas_AddCustomRectFontGlyph(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerToStructType: ImFont*
  PyObject *t0 = NULL;
  // UInt16Type: unsigned short
  PyObject *t1 = NULL;
  // Int32Type: int
  PyObject *t2 = NULL;
  // Int32Type: int
  PyObject *t3 = NULL;
  // FloatType: float
  PyObject *t4 = NULL;
  // ImVec2WrapType: ImVec2
  PyObject *t5 = NULL;
  if(!PyArg_ParseTuple(args, "OOOOOO|O", &py_this, &t0, &t1, &t2, &t3, &t4, &t5)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  ImFont *p0 = ctypes_get_pointer<ImFont*>(t0);
  unsigned short p1 = PyLong_AsUnsignedLong(t1);
  int p2 = PyLong_AsLong(t2);
  int p3 = PyLong_AsLong(t3);
  float p4 = PyFloat_AsDouble(t4);
  ImVec2 p5 = t5 ? get_ImVec2(t5) :  ImVec2 ( 0 , 0 );
  auto value = ptr->AddCustomRectFontGlyph(p0, p1, p2, p3, p4, p5);
  PyObject* py_value = PyLong_FromLong(value);
  return py_value;
}

static PyObject *ImFontAtlas_GetCustomRectByIndex(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // Int32Type: int
  PyObject *t0 = NULL;
  if(!PyArg_ParseTuple(args, "OO", &py_this, &t0)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  int p0 = PyLong_AsLong(t0);
  auto value = ptr->GetCustomRectByIndex(p0);
  PyObject* py_value = ctypes_cast(c_void_p(value), "ImFontAtlasCustomRect", "imgui");
  return py_value;
}

static PyObject *ImFontAtlas_CalcCustomRectUV(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // PointerToStructType: ImFontAtlasCustomRect*
  PyObject *t0 = NULL;
  // PointerType: ImVec2*
  PyObject *t1 = NULL;
  // PointerType: ImVec2*
  PyObject *t2 = NULL;
  if(!PyArg_ParseTuple(args, "OOOO", &py_this, &t0, &t1, &t2)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  const ImFontAtlasCustomRect *p0 = ctypes_get_pointer<const ImFontAtlasCustomRect*>(t0);
  ImVec2 *p1 = ctypes_get_pointer<ImVec2*>(t1);
  ImVec2 *p2 = ctypes_get_pointer<ImVec2*>(t2);
  ptr->CalcCustomRectUV(p0, p1, p2);
  Py_INCREF(Py_None);        
  return Py_None;
}

static PyObject *ImFontAtlas_GetMouseCursorTexData(PyObject *self, PyObject *args){
  // ImFontAtlas
  PyObject *py_this = NULL;
  // Int32Type: int
  PyObject *t0 = NULL;
  // PointerType: ImVec2*
  PyObject *t1 = NULL;
  // PointerType: ImVec2*
  PyObject *t2 = NULL;
  // ArrayType: ImVec2[2]
  PyObject *t3 = NULL;
  // ArrayType: ImVec2[2]
  PyObject *t4 = NULL;
  if(!PyArg_ParseTuple(args, "OOOOOO", &py_this, &t0, &t1, &t2, &t3, &t4)) return NULL;
  ImFontAtlas *ptr = ctypes_get_pointer<ImFontAtlas*>(py_this);
  int p0 = PyLong_AsLong(t0);
  ImVec2 *p1 = ctypes_get_pointer<ImVec2*>(t1);
  ImVec2 *p2 = ctypes_get_pointer<ImVec2*>(t2);
  ImVec2 *p3 = ctypes_get_pointer<ImVec2*>(t3);
  ImVec2 *p4 = ctypes_get_pointer<ImVec2*>(t4);
  auto value = ptr->GetMouseCursorTexData(p0, p1, p2, p3, p4);
  PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
  return py_value;
}

static PyObject *ImGuiViewport_GetCenter(PyObject *self, PyObject *args){
  // ImGuiViewport
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImGuiViewport *ptr = ctypes_get_pointer<ImGuiViewport*>(py_this);
  auto value = ptr->GetCenter();
  PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
  return py_value;
}

static PyObject *ImGuiViewport_GetWorkCenter(PyObject *self, PyObject *args){
  // ImGuiViewport
  PyObject *py_this = NULL;
  if(!PyArg_ParseTuple(args, "O", &py_this)) return NULL;
  ImGuiViewport *ptr = ctypes_get_pointer<ImGuiViewport*>(py_this);
  auto value = ptr->GetWorkCenter();
  PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
  return py_value;
}


# include <imnodes.h>
// clang-format off
static PyObject *imnodes_SetImGuiContext(PyObject *self, PyObject *args) {
  // PointerToStructType: ImGuiContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImGuiContext *p0 = ctypes_get_pointer<ImGuiContext*>(t0);

  
  ImNodes::SetImGuiContext(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_CreateContext(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::CreateContext();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_DestroyContext(PyObject *self, PyObject *args) {
  // PointerType: ImNodesContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  ImNodesContext *p0 = t0 ? ctypes_get_pointer<ImNodesContext*>(t0) :  NULL;

  
  ImNodes::DestroyContext(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetCurrentContext(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::GetCurrentContext();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SetCurrentContext(PyObject *self, PyObject *args) {
  // PointerType: ImNodesContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImNodesContext *p0 = ctypes_get_pointer<ImNodesContext*>(t0);

  
  ImNodes::SetCurrentContext(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextCreate(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::EditorContextCreate();
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextFree(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImNodesEditorContext *p0 = ctypes_get_pointer<ImNodesEditorContext*>(t0);

  
  ImNodes::EditorContextFree(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextSet(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImNodesEditorContext *p0 = ctypes_get_pointer<ImNodesEditorContext*>(t0);

  
  ImNodes::EditorContextSet(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextGetPanning(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::EditorContextGetPanning();
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextResetPanning(PyObject *self, PyObject *args) {
  // ImVec2WrapType: ImVec2
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  ImVec2 p0 = get_ImVec2(t0);

  
  ImNodes::EditorContextResetPanning(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EditorContextMoveToNode(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::EditorContextMoveToNode(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetIO(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  // ReferenceType: ImNodesIO&
auto *value = &ImNodes::GetIO();
auto py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetStyle(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  // ReferenceType: ImNodesStyle&
auto *value = &ImNodes::GetStyle();
auto py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_StyleColorsDark(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::StyleColorsDark();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_StyleColorsClassic(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::StyleColorsClassic();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_StyleColorsLight(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::StyleColorsLight();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginNodeEditor(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::BeginNodeEditor();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndNodeEditor(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndNodeEditor();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PushColorStyle(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  ImNodes::PushColorStyle(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PopColorStyle(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::PopColorStyle();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PushStyleVar(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  ImNodes::PushStyleVar(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PushStyleVar_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImNodes::PushStyleVar(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PopStyleVar(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int p0 = t0 ? PyLong_AsLong(t0) :  1;

  
  ImNodes::PopStyleVar(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginNode(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::BeginNode(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndNode(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndNode();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetNodeDimensions(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::GetNodeDimensions(p0);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginNodeTitleBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::BeginNodeTitleBar();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndNodeTitleBar(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndNodeTitleBar();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginInputAttribute(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  ImNodesPinShape_CircleFilled;

  
  ImNodes::BeginInputAttribute(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndInputAttribute(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndInputAttribute();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginOutputAttribute(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  int p1 = t1 ? PyLong_AsLong(t1) :  ImNodesPinShape_CircleFilled;

  
  ImNodes::BeginOutputAttribute(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndOutputAttribute(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndOutputAttribute();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_BeginStaticAttribute(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::BeginStaticAttribute(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_EndStaticAttribute(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::EndStaticAttribute();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PushAttributeFlag(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::PushAttributeFlag(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_PopAttributeFlag(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::PopAttributeFlag();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_Link(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  ImNodes::Link(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SetNodeDraggable(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  bool p1 = t1 == Py_True;

  
  ImNodes::SetNodeDraggable(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SetNodeScreenSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImNodes::SetNodeScreenSpacePos(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SetNodeEditorSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImNodes::SetNodeEditorSpacePos(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SetNodeGridSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // ImVec2WrapType: ImVec2
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImVec2 p1 = get_ImVec2(t1);

  
  ImNodes::SetNodeGridSpacePos(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetNodeScreenSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::GetNodeScreenSpacePos(p0);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetNodeEditorSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::GetNodeEditorSpacePos(p0);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetNodeGridSpacePos(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::GetNodeGridSpacePos(p0);
PyObject* py_value = Py_BuildValue("(ff)", value.x, value.y);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsEditorHovered(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::IsEditorHovered();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsNodeHovered(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  auto value = ImNodes::IsNodeHovered(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkHovered(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  auto value = ImNodes::IsLinkHovered(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsPinHovered(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  auto value = ImNodes::IsPinHovered(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_NumSelectedNodes(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::NumSelectedNodes();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_NumSelectedLinks(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::NumSelectedLinks();
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetSelectedNodes(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  ImNodes::GetSelectedNodes(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_GetSelectedLinks(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  ImNodes::GetSelectedLinks(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_ClearNodeSelection(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::ClearNodeSelection();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_ClearLinkSelection(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  ImNodes::ClearLinkSelection();
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SelectNode(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::SelectNode(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_ClearNodeSelection_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::ClearNodeSelection(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsNodeSelected(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::IsNodeSelected(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SelectLink(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::SelectLink(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_ClearLinkSelection_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  ImNodes::ClearLinkSelection(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkSelected(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = ImNodes::IsLinkSelected(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsAttributeActive(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = ImNodes::IsAttributeActive();
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsAnyAttributeActive(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  int *p0 = t0 ? ctypes_get_pointer<int*>(t0) :  NULL;

  
  auto value = ImNodes::IsAnyAttributeActive(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkStarted(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  auto value = ImNodes::IsLinkStarted(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkDropped(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  
  // BoolType: bool
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "|OO", &t0, &t1))
    return NULL;
  int *p0 = t0 ? ctypes_get_pointer<int*>(t0) :  NULL;

  
  bool p1 = t1 ? t1 == Py_True :  true;

  
  auto value = ImNodes::IsLinkDropped(p0, p1);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkCreated(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // PointerType: bool*
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OO|O", &t0, &t1, &t2))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  bool *p2 = t2 ? ctypes_get_pointer<bool*>(t2) :  NULL;

  
  auto value = ImNodes::IsLinkCreated(p0, p1, p2);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkCreated_2(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  
  // PointerType: int*
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // PointerType: int*
PyObject *t3 = NULL;

  
  // PointerType: bool*
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO|O", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  int *p1 = ctypes_get_pointer<int*>(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  int *p3 = ctypes_get_pointer<int*>(t3);

  
  bool *p4 = t4 ? ctypes_get_pointer<bool*>(t4) :  NULL;

  
  auto value = ImNodes::IsLinkCreated(p0, p1, p2, p3, p4);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_IsLinkDestroyed(PyObject *self, PyObject *args) {
  // PointerType: int*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int *p0 = ctypes_get_pointer<int*>(t0);

  
  auto value = ImNodes::IsLinkDestroyed(p0);
PyObject* py_value = (value ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False));
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SaveCurrentEditorStateToIniString(PyObject *self, PyObject *args) {
  // PointerType: size_t*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "|O", &t0))
    return NULL;
  size_t *p0 = t0 ? ctypes_get_pointer<size_t*>(t0) :  NULL;

  
  auto value = ImNodes::SaveCurrentEditorStateToIniString(p0);
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SaveEditorStateToIniString(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  
  // PointerType: size_t*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "O|O", &t0, &t1))
    return NULL;
  const ImNodesEditorContext *p0 = ctypes_get_pointer<const ImNodesEditorContext*>(t0);

  
  size_t *p1 = t1 ? ctypes_get_pointer<size_t*>(t1) :  NULL;

  
  auto value = ImNodes::SaveEditorStateToIniString(p0, p1);
PyObject* py_value = PyUnicode_FromString(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *imnodes_LoadCurrentEditorStateFromIniString(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  
  // SizeType: size_t
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  size_t p1 = PyLong_AsSize_t(t1);

  
  ImNodes::LoadCurrentEditorStateFromIniString(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_LoadEditorStateFromIniString(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // SizeType: size_t
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  ImNodesEditorContext *p0 = ctypes_get_pointer<ImNodesEditorContext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  size_t p2 = PyLong_AsSize_t(t2);

  
  ImNodes::LoadEditorStateFromIniString(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SaveCurrentEditorStateToIniFile(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImNodes::SaveCurrentEditorStateToIniFile(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_SaveEditorStateToIniFile(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const ImNodesEditorContext *p0 = ctypes_get_pointer<const ImNodesEditorContext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  ImNodes::SaveEditorStateToIniFile(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_LoadCurrentEditorStateFromIniFile(PyObject *self, PyObject *args) {
  // CStringType: const char *
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  const char *p0 = get_cstring(t0, nullptr);

  
  ImNodes::LoadCurrentEditorStateFromIniFile(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *imnodes_LoadEditorStateFromIniFile(PyObject *self, PyObject *args) {
  // PointerType: ImNodesEditorContext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  ImNodesEditorContext *p0 = ctypes_get_pointer<ImNodesEditorContext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  ImNodes::LoadEditorStateFromIniFile(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on

# include <nanovg.h>
// clang-format off
static PyObject *nanovg_nvgBeginFrame(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  nvgBeginFrame(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCancelFrame(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgCancelFrame(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgEndFrame(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgEndFrame(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgGlobalCompositeOperation(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgGlobalCompositeOperation(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgGlobalCompositeBlendFunc(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  nvgGlobalCompositeBlendFunc(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgGlobalCompositeBlendFuncSeparate(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  nvgGlobalCompositeBlendFuncSeparate(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRGB(PyObject *self, PyObject *args) {
  // UInt8Type: unsigned char
PyObject *t0 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t1 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  unsigned char p0 = PyLong_AsUnsignedLong(t0);

  
  unsigned char p1 = PyLong_AsUnsignedLong(t1);

  
  unsigned char p2 = PyLong_AsUnsignedLong(t2);

  
  auto value = nvgRGB(p0, p1, p2);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRGBf(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  auto value = nvgRGBf(p0, p1, p2);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRGBA(PyObject *self, PyObject *args) {
  // UInt8Type: unsigned char
PyObject *t0 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t1 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t2 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  unsigned char p0 = PyLong_AsUnsignedLong(t0);

  
  unsigned char p1 = PyLong_AsUnsignedLong(t1);

  
  unsigned char p2 = PyLong_AsUnsignedLong(t2);

  
  unsigned char p3 = PyLong_AsUnsignedLong(t3);

  
  auto value = nvgRGBA(p0, p1, p2, p3);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRGBAf(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  auto value = nvgRGBAf(p0, p1, p2, p3);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgLerpRGBA(PyObject *self, PyObject *args) {
  // StructType: NVGcolor
PyObject *t0 = NULL;

  
  // StructType: NVGcolor
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcolor *p0 = ctypes_get_pointer<NVGcolor*>(t0);

  
  NVGcolor *p1 = ctypes_get_pointer<NVGcolor*>(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  auto value = nvgLerpRGBA(*p0, *p1, p2);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransRGBA(PyObject *self, PyObject *args) {
  // StructType: NVGcolor
PyObject *t0 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcolor *p0 = ctypes_get_pointer<NVGcolor*>(t0);

  
  unsigned char p1 = PyLong_AsUnsignedLong(t1);

  
  auto value = nvgTransRGBA(*p0, p1);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransRGBAf(PyObject *self, PyObject *args) {
  // StructType: NVGcolor
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcolor *p0 = ctypes_get_pointer<NVGcolor*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  auto value = nvgTransRGBAf(*p0, p1);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgHSL(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  auto value = nvgHSL(p0, p1, p2);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgHSLA(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // UInt8Type: unsigned char
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  unsigned char p3 = PyLong_AsUnsignedLong(t3);

  
  auto value = nvgHSLA(p0, p1, p2, p3);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgSave(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgSave(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRestore(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgRestore(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgReset(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgReset(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgShapeAntiAlias(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgShapeAntiAlias(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgStrokeColor(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // StructType: NVGcolor
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  NVGcolor *p1 = ctypes_get_pointer<NVGcolor*>(t1);

  
  nvgStrokeColor(p0, *p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgStrokePaint(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // StructType: NVGpaint
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  NVGpaint *p1 = ctypes_get_pointer<NVGpaint*>(t1);

  
  nvgStrokePaint(p0, *p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFillColor(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // StructType: NVGcolor
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  NVGcolor *p1 = ctypes_get_pointer<NVGcolor*>(t1);

  
  nvgFillColor(p0, *p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFillPaint(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // StructType: NVGpaint
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  NVGpaint *p1 = ctypes_get_pointer<NVGpaint*>(t1);

  
  nvgFillPaint(p0, *p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgMiterLimit(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgMiterLimit(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgStrokeWidth(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgStrokeWidth(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgLineCap(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgLineCap(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgLineJoin(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgLineJoin(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgGlobalAlpha(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgGlobalAlpha(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgResetTransform(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgResetTransform(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransform(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  nvgTransform(p0, p1, p2, p3, p4, p5, p6);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTranslate(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgTranslate(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRotate(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgRotate(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgSkewX(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgSkewX(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgSkewY(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgSkewY(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgScale(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgScale(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCurrentTransform(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  nvgCurrentTransform(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformIdentity(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  nvgTransformIdentity(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformTranslate(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgTransformTranslate(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformScale(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgTransformScale(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformRotate(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgTransformRotate(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformSkewX(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgTransformSkewX(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformSkewY(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgTransformSkewY(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformMultiply(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  const float *p1 = ctypes_get_pointer<const float*>(t1);

  
  nvgTransformMultiply(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformPremultiply(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  const float *p1 = ctypes_get_pointer<const float*>(t1);

  
  nvgTransformPremultiply(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformInverse(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  const float *p1 = ctypes_get_pointer<const float*>(t1);

  
  auto value = nvgTransformInverse(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTransformPoint(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // PointerType: float*
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  const float *p2 = ctypes_get_pointer<const float*>(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgTransformPoint(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgDegToRad(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  auto value = nvgDegToRad(p0);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRadToDeg(PyObject *self, PyObject *args) {
  // FloatType: float
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  float p0 = PyFloat_AsDouble(t0);

  
  auto value = nvgRadToDeg(p0);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateImage(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  int p2 = PyLong_AsLong(t2);

  
  auto value = nvgCreateImage(p0, p1, p2);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateImageMem(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: unsigned char*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  unsigned char *p2 = ctypes_get_pointer<unsigned char*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  auto value = nvgCreateImageMem(p0, p1, p2, p3);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateImageRGBA(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // PointerType: unsigned char*
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  const unsigned char *p4 = ctypes_get_pointer<const unsigned char*>(t4);

  
  auto value = nvgCreateImageRGBA(p0, p1, p2, p3, p4);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgUpdateImage(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: unsigned char*
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  const unsigned char *p2 = ctypes_get_pointer<const unsigned char*>(t2);

  
  nvgUpdateImage(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgImageSize(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // PointerType: int*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  int *p3 = ctypes_get_pointer<int*>(t3);

  
  nvgImageSize(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgDeleteImage(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgDeleteImage(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgLinearGradient(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // StructType: NVGcolor
PyObject *t5 = NULL;

  
  // StructType: NVGcolor
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  NVGcolor *p5 = ctypes_get_pointer<NVGcolor*>(t5);

  
  NVGcolor *p6 = ctypes_get_pointer<NVGcolor*>(t6);

  
  auto value = nvgLinearGradient(p0, p1, p2, p3, p4, *p5, *p6);
PyObject* py_value = ctypes_copy(value, "NVGpaint", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgBoxGradient(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  
  // StructType: NVGcolor
PyObject *t7 = NULL;

  
  // StructType: NVGcolor
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  NVGcolor *p7 = ctypes_get_pointer<NVGcolor*>(t7);

  
  NVGcolor *p8 = ctypes_get_pointer<NVGcolor*>(t8);

  
  auto value = nvgBoxGradient(p0, p1, p2, p3, p4, p5, p6, *p7, *p8);
PyObject* py_value = ctypes_copy(value, "NVGpaint", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRadialGradient(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // StructType: NVGcolor
PyObject *t5 = NULL;

  
  // StructType: NVGcolor
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  NVGcolor *p5 = ctypes_get_pointer<NVGcolor*>(t5);

  
  NVGcolor *p6 = ctypes_get_pointer<NVGcolor*>(t6);

  
  auto value = nvgRadialGradient(p0, p1, p2, p3, p4, *p5, *p6);
PyObject* py_value = ctypes_copy(value, "NVGpaint", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgImagePattern(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  
  // FloatType: float
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  int p6 = PyLong_AsLong(t6);

  
  float p7 = PyFloat_AsDouble(t7);

  
  auto value = nvgImagePattern(p0, p1, p2, p3, p4, p5, p6, p7);
PyObject* py_value = ctypes_copy(value, "NVGpaint", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgScissor(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgScissor(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgIntersectScissor(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgIntersectScissor(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgResetScissor(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgResetScissor(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgBeginPath(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgBeginPath(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgMoveTo(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgMoveTo(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgLineTo(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  nvgLineTo(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgBezierTo(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  nvgBezierTo(p0, p1, p2, p3, p4, p5, p6);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgQuadTo(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgQuadTo(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgArcTo(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  nvgArcTo(p0, p1, p2, p3, p4, p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgClosePath(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgClosePath(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgPathWinding(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgPathWinding(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgArc(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  int p6 = PyLong_AsLong(t6);

  
  nvgArc(p0, p1, p2, p3, p4, p5, p6);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRect(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgRect(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRoundedRect(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  nvgRoundedRect(p0, p1, p2, p3, p4, p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgRoundedRectVarying(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  
  // FloatType: float
PyObject *t7 = NULL;

  
  // FloatType: float
PyObject *t8 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7, &t8))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  float p7 = PyFloat_AsDouble(t7);

  
  float p8 = PyFloat_AsDouble(t8);

  
  nvgRoundedRectVarying(p0, p1, p2, p3, p4, p5, p6, p7, p8);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgEllipse(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  nvgEllipse(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCircle(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  nvgCircle(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFill(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgFill(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgStroke(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgStroke(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateFont(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  auto value = nvgCreateFont(p0, p1, p2);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateFontAtIndex(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  int p3 = PyLong_AsLong(t3);

  
  auto value = nvgCreateFontAtIndex(p0, p1, p2, p3);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateFontMem(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // PointerType: unsigned char*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  unsigned char *p2 = ctypes_get_pointer<unsigned char*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  auto value = nvgCreateFontMem(p0, p1, p2, p3, p4);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateFontMemAtIndex(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // PointerType: unsigned char*
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  unsigned char *p2 = ctypes_get_pointer<unsigned char*>(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  int p5 = PyLong_AsLong(t5);

  
  auto value = nvgCreateFontMemAtIndex(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFindFont(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  auto value = nvgFindFont(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgAddFallbackFontId(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  auto value = nvgAddFallbackFontId(p0, p1, p2);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgAddFallbackFont(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  auto value = nvgAddFallbackFont(p0, p1, p2);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgResetFallbackFontsId(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgResetFallbackFontsId(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgResetFallbackFonts(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  nvgResetFallbackFonts(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFontSize(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgFontSize(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFontBlur(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgFontBlur(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextLetterSpacing(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgTextLetterSpacing(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextLineHeight(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  nvgTextLineHeight(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextAlign(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgTextAlign(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFontFaceId(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  nvgFontFaceId(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgFontFace(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  nvgFontFace(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgText(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // CStringType: const char *
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  const char *p3 = get_cstring(t3, nullptr);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  auto value = nvgText(p0, p1, p2, p3, p4);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextBox(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  nvgTextBox(p0, p1, p2, p3, p4, p5);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextBounds(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // CStringType: const char *
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // PointerType: float*
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  const char *p3 = get_cstring(t3, nullptr);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  float *p5 = ctypes_get_pointer<float*>(t5);

  
  auto value = nvgTextBounds(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyFloat_FromDouble(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextBoxBounds(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  
  // PointerType: float*
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  float *p6 = ctypes_get_pointer<float*>(t6);

  
  nvgTextBoxBounds(p0, p1, p2, p3, p4, p5, p6);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextGlyphPositions(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // CStringType: const char *
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // PointerType: NVGglyphPosition*
PyObject *t5 = NULL;

  
  // Int32Type: int
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  const char *p3 = get_cstring(t3, nullptr);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  NVGglyphPosition *p5 = ctypes_get_pointer<NVGglyphPosition*>(t5);

  
  int p6 = PyLong_AsLong(t6);

  
  auto value = nvgTextGlyphPositions(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextMetrics(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  
  // PointerType: float*
PyObject *t2 = NULL;

  
  // PointerType: float*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  float *p2 = ctypes_get_pointer<float*>(t2);

  
  float *p3 = ctypes_get_pointer<float*>(t3);

  
  nvgTextMetrics(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgTextBreakLines(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // PointerType: NVGtextRow*
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  float p3 = PyFloat_AsDouble(t3);

  
  NVGtextRow *p4 = ctypes_get_pointer<NVGtextRow*>(t4);

  
  int p5 = PyLong_AsLong(t5);

  
  auto value = nvgTextBreakLines(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgCreateInternal(PyObject *self, PyObject *args) {
  // PointerType: NVGparams*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGparams *p0 = ctypes_get_pointer<NVGparams*>(t0);

  
  auto value = nvgCreateInternal(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgDeleteInternal(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgDeleteInternal(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgInternalParams(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  auto value = nvgInternalParams(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_nvgDebugDumpPathCache(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgDebugDumpPathCache(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on

# include <glew.h>
// clang-format off
static PyObject *glew_glewInit(PyObject *self, PyObject *args) {if (!PyArg_ParseTuple(args, ""))
    return NULL;
  auto value = glewInit();
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on

#include <GL/glew.h>
# include <nanovg_gl.h>
// clang-format off
static PyObject *nanovg_gl_nvgCreateGL3(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = nvgCreateGL3(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvgDeleteGL3(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgDeleteGL3(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvglCreateImageFromHandleGL3(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  auto value = nvglCreateImageFromHandleGL3(p0, p1, p2, p3, p4);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvglImageHandleGL3(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = nvglImageHandleGL3(p0, p1);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__maxi(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__maxi(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__bindTexture(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  glnvg__bindTexture(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__stencilMask(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  glnvg__stencilMask(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__blendFuncSeparate(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerToStructType: GLNVGblend*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  const GLNVGblend *p1 = ctypes_get_pointer<const GLNVGblend*>(t1);

  
  glnvg__blendFuncSeparate(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__allocTexture(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  auto value = glnvg__allocTexture(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__findTexture(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__findTexture(p0, p1);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__deleteTexture(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__deleteTexture(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__dumpShaderError(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  glnvg__dumpShaderError(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__dumpProgramError(PyObject *self, PyObject *args) {
  // UInt32Type: unsigned int
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  unsigned int p0 = PyLong_AsUnsignedLong(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  glnvg__dumpProgramError(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__checkError(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  glnvg__checkError(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__createShader(PyObject *self, PyObject *args) {
  // PointerType: GLNVGshader*
PyObject *t0 = NULL;

  
  // CStringType: const char *
PyObject *t1 = NULL;

  
  // CStringType: const char *
PyObject *t2 = NULL;

  
  // CStringType: const char *
PyObject *t3 = NULL;

  
  // CStringType: const char *
PyObject *t4 = NULL;

  
  // CStringType: const char *
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  GLNVGshader *p0 = ctypes_get_pointer<GLNVGshader*>(t0);

  
  const char *p1 = get_cstring(t1, nullptr);

  
  const char *p2 = get_cstring(t2, nullptr);

  
  const char *p3 = get_cstring(t3, nullptr);

  
  const char *p4 = get_cstring(t4, nullptr);

  
  const char *p5 = get_cstring(t5, nullptr);

  
  auto value = glnvg__createShader(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__deleteShader(PyObject *self, PyObject *args) {
  // PointerType: GLNVGshader*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  GLNVGshader *p0 = ctypes_get_pointer<GLNVGshader*>(t0);

  
  glnvg__deleteShader(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__getUniforms(PyObject *self, PyObject *args) {
  // PointerType: GLNVGshader*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  GLNVGshader *p0 = ctypes_get_pointer<GLNVGshader*>(t0);

  
  glnvg__getUniforms(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderCreateTexture(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // PointerType: unsigned char*
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  const unsigned char *p5 = ctypes_get_pointer<const unsigned char*>(t5);

  
  auto value = glnvg__renderCreateTexture(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderCreate(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  auto value = glnvg__renderCreate(p0);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderCreateTexture_2(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // PointerType: unsigned char*
PyObject *t5 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOO", &t0, &t1, &t2, &t3, &t4, &t5))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  const unsigned char *p5 = ctypes_get_pointer<const unsigned char*>(t5);

  
  auto value = glnvg__renderCreateTexture(p0, p1, p2, p3, p4, p5);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderDeleteTexture(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__renderDeleteTexture(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderUpdateTexture(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  
  // PointerType: unsigned char*
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  int p5 = PyLong_AsLong(t5);

  
  const unsigned char *p6 = ctypes_get_pointer<const unsigned char*>(t6);

  
  auto value = glnvg__renderUpdateTexture(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderGetTextureSize(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // PointerType: int*
PyObject *t2 = NULL;

  
  // PointerType: int*
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int *p2 = ctypes_get_pointer<int*>(t2);

  
  int *p3 = ctypes_get_pointer<int*>(t3);

  
  auto value = glnvg__renderGetTextureSize(p0, p1, p2, p3);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__xformToMat3x4(PyObject *self, PyObject *args) {
  // PointerType: float*
PyObject *t0 = NULL;

  
  // PointerType: float*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  float *p0 = ctypes_get_pointer<float*>(t0);

  
  float *p1 = ctypes_get_pointer<float*>(t1);

  
  glnvg__xformToMat3x4(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__premulColor(PyObject *self, PyObject *args) {
  // StructType: NVGcolor
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcolor *p0 = ctypes_get_pointer<NVGcolor*>(t0);

  
  auto value = glnvg__premulColor(*p0);
PyObject* py_value = ctypes_copy(value, "NVGcolor", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__convertPaint(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: GLNVGfragUniforms*
PyObject *t1 = NULL;

  
  // PointerToStructType: NVGpaint*
PyObject *t2 = NULL;

  
  // PointerType: NVGscissor*
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  GLNVGfragUniforms *p1 = ctypes_get_pointer<GLNVGfragUniforms*>(t1);

  
  NVGpaint *p2 = ctypes_get_pointer<NVGpaint*>(t2);

  
  NVGscissor *p3 = ctypes_get_pointer<NVGscissor*>(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  auto value = glnvg__convertPaint(p0, p1, p2, p3, p4, p5, p6);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvg__fragUniformPtr(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = nvg__fragUniformPtr(p0, p1);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__setUniforms(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &t0, &t1, &t2))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  glnvg__setUniforms(p0, p1, p2);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderViewport(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  if (!PyArg_ParseTuple(args, "OOOO", &t0, &t1, &t2, &t3))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  glnvg__renderViewport(p0, p1, p2, p3);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__fill(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: GLNVGcall*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  GLNVGcall *p1 = ctypes_get_pointer<GLNVGcall*>(t1);

  
  glnvg__fill(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__convexFill(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: GLNVGcall*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  GLNVGcall *p1 = ctypes_get_pointer<GLNVGcall*>(t1);

  
  glnvg__convexFill(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__stroke(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: GLNVGcall*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  GLNVGcall *p1 = ctypes_get_pointer<GLNVGcall*>(t1);

  
  glnvg__stroke(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__triangles(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // PointerType: GLNVGcall*
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  GLNVGcall *p1 = ctypes_get_pointer<GLNVGcall*>(t1);

  
  glnvg__triangles(p0, p1);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderCancel(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  glnvg__renderCancel(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg_convertBlendFuncFactor(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = glnvg_convertBlendFuncFactor(p0);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__blendCompositeOperation(PyObject *self, PyObject *args) {
  // StructType: NVGcompositeOperationState
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcompositeOperationState *p0 = ctypes_get_pointer<NVGcompositeOperationState*>(t0);

  
  auto value = glnvg__blendCompositeOperation(*p0);
PyObject* py_value = ctypes_copy(value, "GLNVGblend", "nanovg");
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderFlush(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  glnvg__renderFlush(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__maxVertCount(PyObject *self, PyObject *args) {
  // PointerType: NVGpath*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  const NVGpath *p0 = ctypes_get_pointer<const NVGpath*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__maxVertCount(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__allocCall(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  auto value = glnvg__allocCall(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__allocPaths(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__allocPaths(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__allocVerts(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__allocVerts(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__allocFragUniforms(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = glnvg__allocFragUniforms(p0, p1);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvg__fragUniformPtr_2(PyObject *self, PyObject *args) {
  // PointerType: GLNVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  GLNVGcontext *p0 = ctypes_get_pointer<GLNVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = nvg__fragUniformPtr(p0, p1);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__vset(PyObject *self, PyObject *args) {
  // PointerType: NVGvertex*
PyObject *t0 = NULL;

  
  // FloatType: float
PyObject *t1 = NULL;

  
  // FloatType: float
PyObject *t2 = NULL;

  
  // FloatType: float
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGvertex *p0 = ctypes_get_pointer<NVGvertex*>(t0);

  
  float p1 = PyFloat_AsDouble(t1);

  
  float p2 = PyFloat_AsDouble(t2);

  
  float p3 = PyFloat_AsDouble(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  glnvg__vset(p0, p1, p2, p3, p4);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderFill(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // PointerToStructType: NVGpaint*
PyObject *t1 = NULL;

  
  // StructType: NVGcompositeOperationState
PyObject *t2 = NULL;

  
  // PointerType: NVGscissor*
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // PointerType: float*
PyObject *t5 = NULL;

  
  // PointerType: NVGpath*
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  NVGpaint *p1 = ctypes_get_pointer<NVGpaint*>(t1);

  
  NVGcompositeOperationState *p2 = ctypes_get_pointer<NVGcompositeOperationState*>(t2);

  
  NVGscissor *p3 = ctypes_get_pointer<NVGscissor*>(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  const float *p5 = ctypes_get_pointer<const float*>(t5);

  
  const NVGpath *p6 = ctypes_get_pointer<const NVGpath*>(t6);

  
  int p7 = PyLong_AsLong(t7);

  
  glnvg__renderFill(p0, p1, *p2, p3, p4, p5, p6, p7);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderStroke(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // PointerToStructType: NVGpaint*
PyObject *t1 = NULL;

  
  // StructType: NVGcompositeOperationState
PyObject *t2 = NULL;

  
  // PointerType: NVGscissor*
PyObject *t3 = NULL;

  
  // FloatType: float
PyObject *t4 = NULL;

  
  // FloatType: float
PyObject *t5 = NULL;

  
  // PointerType: NVGpath*
PyObject *t6 = NULL;

  
  // Int32Type: int
PyObject *t7 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6, &t7))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  NVGpaint *p1 = ctypes_get_pointer<NVGpaint*>(t1);

  
  NVGcompositeOperationState *p2 = ctypes_get_pointer<NVGcompositeOperationState*>(t2);

  
  NVGscissor *p3 = ctypes_get_pointer<NVGscissor*>(t3);

  
  float p4 = PyFloat_AsDouble(t4);

  
  float p5 = PyFloat_AsDouble(t5);

  
  const NVGpath *p6 = ctypes_get_pointer<const NVGpath*>(t6);

  
  int p7 = PyLong_AsLong(t7);

  
  glnvg__renderStroke(p0, p1, *p2, p3, p4, p5, p6, p7);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderTriangles(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  
  // PointerToStructType: NVGpaint*
PyObject *t1 = NULL;

  
  // StructType: NVGcompositeOperationState
PyObject *t2 = NULL;

  
  // PointerType: NVGscissor*
PyObject *t3 = NULL;

  
  // PointerType: NVGvertex*
PyObject *t4 = NULL;

  
  // Int32Type: int
PyObject *t5 = NULL;

  
  // FloatType: float
PyObject *t6 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOOOO", &t0, &t1, &t2, &t3, &t4, &t5, &t6))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  NVGpaint *p1 = ctypes_get_pointer<NVGpaint*>(t1);

  
  NVGcompositeOperationState *p2 = ctypes_get_pointer<NVGcompositeOperationState*>(t2);

  
  NVGscissor *p3 = ctypes_get_pointer<NVGscissor*>(t3);

  
  const NVGvertex *p4 = ctypes_get_pointer<const NVGvertex*>(t4);

  
  int p5 = PyLong_AsLong(t5);

  
  float p6 = PyFloat_AsDouble(t6);

  
  glnvg__renderTriangles(p0, p1, *p2, p3, p4, p5, p6);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_glnvg__renderDelete(PyObject *self, PyObject *args) {
  // PointerType: void*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  void *p0 = ctypes_get_pointer<void*>(t0);

  
  glnvg__renderDelete(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvgCreateGL3_2(PyObject *self, PyObject *args) {
  // Int32Type: int
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  int p0 = PyLong_AsLong(t0);

  
  auto value = nvgCreateGL3(p0);
PyObject* py_value = c_void_p(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvgDeleteGL3_2(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  if (!PyArg_ParseTuple(args, "O", &t0))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  nvgDeleteGL3(p0);
Py_INCREF(Py_None);        
return Py_None;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvglCreateImageFromHandleGL3_2(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // UInt32Type: unsigned int
PyObject *t1 = NULL;

  
  // Int32Type: int
PyObject *t2 = NULL;

  
  // Int32Type: int
PyObject *t3 = NULL;

  
  // Int32Type: int
PyObject *t4 = NULL;

  if (!PyArg_ParseTuple(args, "OOOOO", &t0, &t1, &t2, &t3, &t4))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  unsigned int p1 = PyLong_AsUnsignedLong(t1);

  
  int p2 = PyLong_AsLong(t2);

  
  int p3 = PyLong_AsLong(t3);

  
  int p4 = PyLong_AsLong(t4);

  
  auto value = nvglCreateImageFromHandleGL3(p0, p1, p2, p3, p4);
PyObject* py_value = PyLong_FromLong(value);
return py_value;

}
// clang-format on
// clang-format off
static PyObject *nanovg_gl_nvglImageHandleGL3_2(PyObject *self, PyObject *args) {
  // PointerType: NVGcontext*
PyObject *t0 = NULL;

  
  // Int32Type: int
PyObject *t1 = NULL;

  if (!PyArg_ParseTuple(args, "OO", &t0, &t1))
    return NULL;
  NVGcontext *p0 = ctypes_get_pointer<NVGcontext*>(t0);

  
  int p1 = PyLong_AsLong(t1);

  
  auto value = nvglImageHandleGL3(p0, p1);
PyObject* py_value = PyLong_FromUnsignedLong(value);
return py_value;

}
// clang-format on

// clang-format on

PyMODINIT_FUNC
PyInit_impl(void) {
#ifdef _DEBUG
  std::cout << "DEBUG_BUILD sizeof: ImGuiIO: " << sizeof(ImGuiIO) << std::endl;
#endif

  auto __dict__ = PyImport_GetModuleDict();
  PyObject *__root__ = nullptr;
  { // create empty root module
    static PyMethodDef Methods[] = {
        {NULL, NULL, 0, NULL} /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "impl", /* name of module */
        nullptr,                       /* module documentation, may be NULL */
        -1, /* size of per-interpreter state of the module,
              or -1 if the module keeps state in global variables. */
        Methods};

    __root__ = PyModule_Create(&module);
    if (!__root__) {
      return NULL;
    }
  }

  // clang-format off
  { // imgui
    static PyMethodDef Methods[] = {
        // clang-format off
        {"CreateContext", imgui_CreateContext, METH_VARARGS, "ImGui::CreateContext"},
        {"DestroyContext", imgui_DestroyContext, METH_VARARGS, "ImGui::DestroyContext"},
        {"GetCurrentContext", imgui_GetCurrentContext, METH_VARARGS, "ImGui::GetCurrentContext"},
        {"SetCurrentContext", imgui_SetCurrentContext, METH_VARARGS, "ImGui::SetCurrentContext"},
        {"GetIO", imgui_GetIO, METH_VARARGS, "ImGui::GetIO"},
        {"GetStyle", imgui_GetStyle, METH_VARARGS, "ImGui::GetStyle"},
        {"NewFrame", imgui_NewFrame, METH_VARARGS, "ImGui::NewFrame"},
        {"EndFrame", imgui_EndFrame, METH_VARARGS, "ImGui::EndFrame"},
        {"Render", imgui_Render, METH_VARARGS, "ImGui::Render"},
        {"GetDrawData", imgui_GetDrawData, METH_VARARGS, "ImGui::GetDrawData"},
        {"ShowDemoWindow", imgui_ShowDemoWindow, METH_VARARGS, "ImGui::ShowDemoWindow"},
        {"ShowMetricsWindow", imgui_ShowMetricsWindow, METH_VARARGS, "ImGui::ShowMetricsWindow"},
        {"ShowStackToolWindow", imgui_ShowStackToolWindow, METH_VARARGS, "ImGui::ShowStackToolWindow"},
        {"ShowAboutWindow", imgui_ShowAboutWindow, METH_VARARGS, "ImGui::ShowAboutWindow"},
        {"ShowStyleEditor", imgui_ShowStyleEditor, METH_VARARGS, "ImGui::ShowStyleEditor"},
        {"ShowStyleSelector", imgui_ShowStyleSelector, METH_VARARGS, "ImGui::ShowStyleSelector"},
        {"ShowFontSelector", imgui_ShowFontSelector, METH_VARARGS, "ImGui::ShowFontSelector"},
        {"ShowUserGuide", imgui_ShowUserGuide, METH_VARARGS, "ImGui::ShowUserGuide"},
        {"GetVersion", imgui_GetVersion, METH_VARARGS, "ImGui::GetVersion"},
        {"StyleColorsDark", imgui_StyleColorsDark, METH_VARARGS, "ImGui::StyleColorsDark"},
        {"StyleColorsLight", imgui_StyleColorsLight, METH_VARARGS, "ImGui::StyleColorsLight"},
        {"StyleColorsClassic", imgui_StyleColorsClassic, METH_VARARGS, "ImGui::StyleColorsClassic"},
        {"Begin", imgui_Begin, METH_VARARGS, "ImGui::Begin"},
        {"End", imgui_End, METH_VARARGS, "ImGui::End"},
        {"BeginChild", imgui_BeginChild, METH_VARARGS, "ImGui::BeginChild"},
        {"BeginChild_2", imgui_BeginChild_2, METH_VARARGS, "ImGui::BeginChild"},
        {"EndChild", imgui_EndChild, METH_VARARGS, "ImGui::EndChild"},
        {"IsWindowAppearing", imgui_IsWindowAppearing, METH_VARARGS, "ImGui::IsWindowAppearing"},
        {"IsWindowCollapsed", imgui_IsWindowCollapsed, METH_VARARGS, "ImGui::IsWindowCollapsed"},
        {"IsWindowFocused", imgui_IsWindowFocused, METH_VARARGS, "ImGui::IsWindowFocused"},
        {"IsWindowHovered", imgui_IsWindowHovered, METH_VARARGS, "ImGui::IsWindowHovered"},
        {"GetWindowDrawList", imgui_GetWindowDrawList, METH_VARARGS, "ImGui::GetWindowDrawList"},
        {"GetWindowDpiScale", imgui_GetWindowDpiScale, METH_VARARGS, "ImGui::GetWindowDpiScale"},
        {"GetWindowPos", imgui_GetWindowPos, METH_VARARGS, "ImGui::GetWindowPos"},
        {"GetWindowSize", imgui_GetWindowSize, METH_VARARGS, "ImGui::GetWindowSize"},
        {"GetWindowWidth", imgui_GetWindowWidth, METH_VARARGS, "ImGui::GetWindowWidth"},
        {"GetWindowHeight", imgui_GetWindowHeight, METH_VARARGS, "ImGui::GetWindowHeight"},
        {"GetWindowViewport", imgui_GetWindowViewport, METH_VARARGS, "ImGui::GetWindowViewport"},
        {"SetNextWindowPos", imgui_SetNextWindowPos, METH_VARARGS, "ImGui::SetNextWindowPos"},
        {"SetNextWindowSize", imgui_SetNextWindowSize, METH_VARARGS, "ImGui::SetNextWindowSize"},
        {"SetNextWindowContentSize", imgui_SetNextWindowContentSize, METH_VARARGS, "ImGui::SetNextWindowContentSize"},
        {"SetNextWindowCollapsed", imgui_SetNextWindowCollapsed, METH_VARARGS, "ImGui::SetNextWindowCollapsed"},
        {"SetNextWindowFocus", imgui_SetNextWindowFocus, METH_VARARGS, "ImGui::SetNextWindowFocus"},
        {"SetNextWindowBgAlpha", imgui_SetNextWindowBgAlpha, METH_VARARGS, "ImGui::SetNextWindowBgAlpha"},
        {"SetNextWindowViewport", imgui_SetNextWindowViewport, METH_VARARGS, "ImGui::SetNextWindowViewport"},
        {"SetWindowPos", imgui_SetWindowPos, METH_VARARGS, "ImGui::SetWindowPos"},
        {"SetWindowSize", imgui_SetWindowSize, METH_VARARGS, "ImGui::SetWindowSize"},
        {"SetWindowCollapsed", imgui_SetWindowCollapsed, METH_VARARGS, "ImGui::SetWindowCollapsed"},
        {"SetWindowFocus", imgui_SetWindowFocus, METH_VARARGS, "ImGui::SetWindowFocus"},
        {"SetWindowFontScale", imgui_SetWindowFontScale, METH_VARARGS, "ImGui::SetWindowFontScale"},
        {"SetWindowPos_2", imgui_SetWindowPos_2, METH_VARARGS, "ImGui::SetWindowPos"},
        {"SetWindowSize_2", imgui_SetWindowSize_2, METH_VARARGS, "ImGui::SetWindowSize"},
        {"SetWindowCollapsed_2", imgui_SetWindowCollapsed_2, METH_VARARGS, "ImGui::SetWindowCollapsed"},
        {"SetWindowFocus_2", imgui_SetWindowFocus_2, METH_VARARGS, "ImGui::SetWindowFocus"},
        {"GetContentRegionAvail", imgui_GetContentRegionAvail, METH_VARARGS, "ImGui::GetContentRegionAvail"},
        {"GetContentRegionMax", imgui_GetContentRegionMax, METH_VARARGS, "ImGui::GetContentRegionMax"},
        {"GetWindowContentRegionMin", imgui_GetWindowContentRegionMin, METH_VARARGS, "ImGui::GetWindowContentRegionMin"},
        {"GetWindowContentRegionMax", imgui_GetWindowContentRegionMax, METH_VARARGS, "ImGui::GetWindowContentRegionMax"},
        {"GetScrollX", imgui_GetScrollX, METH_VARARGS, "ImGui::GetScrollX"},
        {"GetScrollY", imgui_GetScrollY, METH_VARARGS, "ImGui::GetScrollY"},
        {"SetScrollX", imgui_SetScrollX, METH_VARARGS, "ImGui::SetScrollX"},
        {"SetScrollY", imgui_SetScrollY, METH_VARARGS, "ImGui::SetScrollY"},
        {"GetScrollMaxX", imgui_GetScrollMaxX, METH_VARARGS, "ImGui::GetScrollMaxX"},
        {"GetScrollMaxY", imgui_GetScrollMaxY, METH_VARARGS, "ImGui::GetScrollMaxY"},
        {"SetScrollHereX", imgui_SetScrollHereX, METH_VARARGS, "ImGui::SetScrollHereX"},
        {"SetScrollHereY", imgui_SetScrollHereY, METH_VARARGS, "ImGui::SetScrollHereY"},
        {"SetScrollFromPosX", imgui_SetScrollFromPosX, METH_VARARGS, "ImGui::SetScrollFromPosX"},
        {"SetScrollFromPosY", imgui_SetScrollFromPosY, METH_VARARGS, "ImGui::SetScrollFromPosY"},
        {"PushFont", imgui_PushFont, METH_VARARGS, "ImGui::PushFont"},
        {"PopFont", imgui_PopFont, METH_VARARGS, "ImGui::PopFont"},
        {"PushStyleColor", imgui_PushStyleColor, METH_VARARGS, "ImGui::PushStyleColor"},
        {"PushStyleColor_2", imgui_PushStyleColor_2, METH_VARARGS, "ImGui::PushStyleColor"},
        {"PopStyleColor", imgui_PopStyleColor, METH_VARARGS, "ImGui::PopStyleColor"},
        {"PushStyleVar", imgui_PushStyleVar, METH_VARARGS, "ImGui::PushStyleVar"},
        {"PushStyleVar_2", imgui_PushStyleVar_2, METH_VARARGS, "ImGui::PushStyleVar"},
        {"PopStyleVar", imgui_PopStyleVar, METH_VARARGS, "ImGui::PopStyleVar"},
        {"PushAllowKeyboardFocus", imgui_PushAllowKeyboardFocus, METH_VARARGS, "ImGui::PushAllowKeyboardFocus"},
        {"PopAllowKeyboardFocus", imgui_PopAllowKeyboardFocus, METH_VARARGS, "ImGui::PopAllowKeyboardFocus"},
        {"PushButtonRepeat", imgui_PushButtonRepeat, METH_VARARGS, "ImGui::PushButtonRepeat"},
        {"PopButtonRepeat", imgui_PopButtonRepeat, METH_VARARGS, "ImGui::PopButtonRepeat"},
        {"PushItemWidth", imgui_PushItemWidth, METH_VARARGS, "ImGui::PushItemWidth"},
        {"PopItemWidth", imgui_PopItemWidth, METH_VARARGS, "ImGui::PopItemWidth"},
        {"SetNextItemWidth", imgui_SetNextItemWidth, METH_VARARGS, "ImGui::SetNextItemWidth"},
        {"CalcItemWidth", imgui_CalcItemWidth, METH_VARARGS, "ImGui::CalcItemWidth"},
        {"PushTextWrapPos", imgui_PushTextWrapPos, METH_VARARGS, "ImGui::PushTextWrapPos"},
        {"PopTextWrapPos", imgui_PopTextWrapPos, METH_VARARGS, "ImGui::PopTextWrapPos"},
        {"GetFont", imgui_GetFont, METH_VARARGS, "ImGui::GetFont"},
        {"GetFontSize", imgui_GetFontSize, METH_VARARGS, "ImGui::GetFontSize"},
        {"GetFontTexUvWhitePixel", imgui_GetFontTexUvWhitePixel, METH_VARARGS, "ImGui::GetFontTexUvWhitePixel"},
        {"GetColorU32", imgui_GetColorU32, METH_VARARGS, "ImGui::GetColorU32"},
        {"GetColorU32_2", imgui_GetColorU32_2, METH_VARARGS, "ImGui::GetColorU32"},
        {"GetColorU32_3", imgui_GetColorU32_3, METH_VARARGS, "ImGui::GetColorU32"},
        {"GetStyleColorVec4", imgui_GetStyleColorVec4, METH_VARARGS, "ImGui::GetStyleColorVec4"},
        {"Separator", imgui_Separator, METH_VARARGS, "ImGui::Separator"},
        {"SameLine", imgui_SameLine, METH_VARARGS, "ImGui::SameLine"},
        {"NewLine", imgui_NewLine, METH_VARARGS, "ImGui::NewLine"},
        {"Spacing", imgui_Spacing, METH_VARARGS, "ImGui::Spacing"},
        {"Dummy", imgui_Dummy, METH_VARARGS, "ImGui::Dummy"},
        {"Indent", imgui_Indent, METH_VARARGS, "ImGui::Indent"},
        {"Unindent", imgui_Unindent, METH_VARARGS, "ImGui::Unindent"},
        {"BeginGroup", imgui_BeginGroup, METH_VARARGS, "ImGui::BeginGroup"},
        {"EndGroup", imgui_EndGroup, METH_VARARGS, "ImGui::EndGroup"},
        {"GetCursorPos", imgui_GetCursorPos, METH_VARARGS, "ImGui::GetCursorPos"},
        {"GetCursorPosX", imgui_GetCursorPosX, METH_VARARGS, "ImGui::GetCursorPosX"},
        {"GetCursorPosY", imgui_GetCursorPosY, METH_VARARGS, "ImGui::GetCursorPosY"},
        {"SetCursorPos", imgui_SetCursorPos, METH_VARARGS, "ImGui::SetCursorPos"},
        {"SetCursorPosX", imgui_SetCursorPosX, METH_VARARGS, "ImGui::SetCursorPosX"},
        {"SetCursorPosY", imgui_SetCursorPosY, METH_VARARGS, "ImGui::SetCursorPosY"},
        {"GetCursorStartPos", imgui_GetCursorStartPos, METH_VARARGS, "ImGui::GetCursorStartPos"},
        {"GetCursorScreenPos", imgui_GetCursorScreenPos, METH_VARARGS, "ImGui::GetCursorScreenPos"},
        {"SetCursorScreenPos", imgui_SetCursorScreenPos, METH_VARARGS, "ImGui::SetCursorScreenPos"},
        {"AlignTextToFramePadding", imgui_AlignTextToFramePadding, METH_VARARGS, "ImGui::AlignTextToFramePadding"},
        {"GetTextLineHeight", imgui_GetTextLineHeight, METH_VARARGS, "ImGui::GetTextLineHeight"},
        {"GetTextLineHeightWithSpacing", imgui_GetTextLineHeightWithSpacing, METH_VARARGS, "ImGui::GetTextLineHeightWithSpacing"},
        {"GetFrameHeight", imgui_GetFrameHeight, METH_VARARGS, "ImGui::GetFrameHeight"},
        {"GetFrameHeightWithSpacing", imgui_GetFrameHeightWithSpacing, METH_VARARGS, "ImGui::GetFrameHeightWithSpacing"},
        {"PushID", imgui_PushID, METH_VARARGS, "ImGui::PushID"},
        {"PushID_2", imgui_PushID_2, METH_VARARGS, "ImGui::PushID"},
        {"PushID_3", imgui_PushID_3, METH_VARARGS, "ImGui::PushID"},
        {"PushID_4", imgui_PushID_4, METH_VARARGS, "ImGui::PushID"},
        {"PopID", imgui_PopID, METH_VARARGS, "ImGui::PopID"},
        {"GetID", imgui_GetID, METH_VARARGS, "ImGui::GetID"},
        {"GetID_2", imgui_GetID_2, METH_VARARGS, "ImGui::GetID"},
        {"GetID_3", imgui_GetID_3, METH_VARARGS, "ImGui::GetID"},
        {"TextUnformatted", imgui_TextUnformatted, METH_VARARGS, "ImGui::TextUnformatted"},
        {"Text", imgui_Text, METH_VARARGS, "ImGui::Text"},
        {"TextColored", imgui_TextColored, METH_VARARGS, "ImGui::TextColored"},
        {"TextDisabled", imgui_TextDisabled, METH_VARARGS, "ImGui::TextDisabled"},
        {"TextWrapped", imgui_TextWrapped, METH_VARARGS, "ImGui::TextWrapped"},
        {"LabelText", imgui_LabelText, METH_VARARGS, "ImGui::LabelText"},
        {"BulletText", imgui_BulletText, METH_VARARGS, "ImGui::BulletText"},
        {"Button", imgui_Button, METH_VARARGS, "ImGui::Button"},
        {"SmallButton", imgui_SmallButton, METH_VARARGS, "ImGui::SmallButton"},
        {"InvisibleButton", imgui_InvisibleButton, METH_VARARGS, "ImGui::InvisibleButton"},
        {"ArrowButton", imgui_ArrowButton, METH_VARARGS, "ImGui::ArrowButton"},
        {"Image", imgui_Image, METH_VARARGS, "ImGui::Image"},
        {"ImageButton", imgui_ImageButton, METH_VARARGS, "ImGui::ImageButton"},
        {"Checkbox", imgui_Checkbox, METH_VARARGS, "ImGui::Checkbox"},
        {"RadioButton", imgui_RadioButton, METH_VARARGS, "ImGui::RadioButton"},
        {"RadioButton_2", imgui_RadioButton_2, METH_VARARGS, "ImGui::RadioButton"},
        {"ProgressBar", imgui_ProgressBar, METH_VARARGS, "ImGui::ProgressBar"},
        {"Bullet", imgui_Bullet, METH_VARARGS, "ImGui::Bullet"},
        {"BeginCombo", imgui_BeginCombo, METH_VARARGS, "ImGui::BeginCombo"},
        {"EndCombo", imgui_EndCombo, METH_VARARGS, "ImGui::EndCombo"},
        {"DragFloat", imgui_DragFloat, METH_VARARGS, "ImGui::DragFloat"},
        {"DragFloat2", imgui_DragFloat2, METH_VARARGS, "ImGui::DragFloat2"},
        {"DragFloat3", imgui_DragFloat3, METH_VARARGS, "ImGui::DragFloat3"},
        {"DragFloat4", imgui_DragFloat4, METH_VARARGS, "ImGui::DragFloat4"},
        {"DragFloatRange2", imgui_DragFloatRange2, METH_VARARGS, "ImGui::DragFloatRange2"},
        {"DragInt", imgui_DragInt, METH_VARARGS, "ImGui::DragInt"},
        {"DragInt2", imgui_DragInt2, METH_VARARGS, "ImGui::DragInt2"},
        {"DragInt3", imgui_DragInt3, METH_VARARGS, "ImGui::DragInt3"},
        {"DragInt4", imgui_DragInt4, METH_VARARGS, "ImGui::DragInt4"},
        {"DragIntRange2", imgui_DragIntRange2, METH_VARARGS, "ImGui::DragIntRange2"},
        {"DragScalar", imgui_DragScalar, METH_VARARGS, "ImGui::DragScalar"},
        {"DragScalarN", imgui_DragScalarN, METH_VARARGS, "ImGui::DragScalarN"},
        {"SliderFloat", imgui_SliderFloat, METH_VARARGS, "ImGui::SliderFloat"},
        {"SliderFloat2", imgui_SliderFloat2, METH_VARARGS, "ImGui::SliderFloat2"},
        {"SliderFloat3", imgui_SliderFloat3, METH_VARARGS, "ImGui::SliderFloat3"},
        {"SliderFloat4", imgui_SliderFloat4, METH_VARARGS, "ImGui::SliderFloat4"},
        {"SliderAngle", imgui_SliderAngle, METH_VARARGS, "ImGui::SliderAngle"},
        {"SliderInt", imgui_SliderInt, METH_VARARGS, "ImGui::SliderInt"},
        {"SliderInt2", imgui_SliderInt2, METH_VARARGS, "ImGui::SliderInt2"},
        {"SliderInt3", imgui_SliderInt3, METH_VARARGS, "ImGui::SliderInt3"},
        {"SliderInt4", imgui_SliderInt4, METH_VARARGS, "ImGui::SliderInt4"},
        {"SliderScalar", imgui_SliderScalar, METH_VARARGS, "ImGui::SliderScalar"},
        {"SliderScalarN", imgui_SliderScalarN, METH_VARARGS, "ImGui::SliderScalarN"},
        {"VSliderFloat", imgui_VSliderFloat, METH_VARARGS, "ImGui::VSliderFloat"},
        {"VSliderInt", imgui_VSliderInt, METH_VARARGS, "ImGui::VSliderInt"},
        {"VSliderScalar", imgui_VSliderScalar, METH_VARARGS, "ImGui::VSliderScalar"},
        {"InputFloat", imgui_InputFloat, METH_VARARGS, "ImGui::InputFloat"},
        {"InputFloat2", imgui_InputFloat2, METH_VARARGS, "ImGui::InputFloat2"},
        {"InputFloat3", imgui_InputFloat3, METH_VARARGS, "ImGui::InputFloat3"},
        {"InputFloat4", imgui_InputFloat4, METH_VARARGS, "ImGui::InputFloat4"},
        {"InputInt", imgui_InputInt, METH_VARARGS, "ImGui::InputInt"},
        {"InputInt2", imgui_InputInt2, METH_VARARGS, "ImGui::InputInt2"},
        {"InputInt3", imgui_InputInt3, METH_VARARGS, "ImGui::InputInt3"},
        {"InputInt4", imgui_InputInt4, METH_VARARGS, "ImGui::InputInt4"},
        {"InputDouble", imgui_InputDouble, METH_VARARGS, "ImGui::InputDouble"},
        {"InputScalar", imgui_InputScalar, METH_VARARGS, "ImGui::InputScalar"},
        {"InputScalarN", imgui_InputScalarN, METH_VARARGS, "ImGui::InputScalarN"},
        {"ColorEdit3", imgui_ColorEdit3, METH_VARARGS, "ImGui::ColorEdit3"},
        {"ColorEdit4", imgui_ColorEdit4, METH_VARARGS, "ImGui::ColorEdit4"},
        {"ColorPicker3", imgui_ColorPicker3, METH_VARARGS, "ImGui::ColorPicker3"},
        {"ColorPicker4", imgui_ColorPicker4, METH_VARARGS, "ImGui::ColorPicker4"},
        {"ColorButton", imgui_ColorButton, METH_VARARGS, "ImGui::ColorButton"},
        {"SetColorEditOptions", imgui_SetColorEditOptions, METH_VARARGS, "ImGui::SetColorEditOptions"},
        {"TreeNode", imgui_TreeNode, METH_VARARGS, "ImGui::TreeNode"},
        {"TreeNode_2", imgui_TreeNode_2, METH_VARARGS, "ImGui::TreeNode"},
        {"TreeNode_3", imgui_TreeNode_3, METH_VARARGS, "ImGui::TreeNode"},
        {"TreeNodeEx", imgui_TreeNodeEx, METH_VARARGS, "ImGui::TreeNodeEx"},
        {"TreeNodeEx_2", imgui_TreeNodeEx_2, METH_VARARGS, "ImGui::TreeNodeEx"},
        {"TreeNodeEx_3", imgui_TreeNodeEx_3, METH_VARARGS, "ImGui::TreeNodeEx"},
        {"TreePush", imgui_TreePush, METH_VARARGS, "ImGui::TreePush"},
        {"TreePush_2", imgui_TreePush_2, METH_VARARGS, "ImGui::TreePush"},
        {"TreePop", imgui_TreePop, METH_VARARGS, "ImGui::TreePop"},
        {"GetTreeNodeToLabelSpacing", imgui_GetTreeNodeToLabelSpacing, METH_VARARGS, "ImGui::GetTreeNodeToLabelSpacing"},
        {"CollapsingHeader", imgui_CollapsingHeader, METH_VARARGS, "ImGui::CollapsingHeader"},
        {"CollapsingHeader_2", imgui_CollapsingHeader_2, METH_VARARGS, "ImGui::CollapsingHeader"},
        {"SetNextItemOpen", imgui_SetNextItemOpen, METH_VARARGS, "ImGui::SetNextItemOpen"},
        {"Selectable", imgui_Selectable, METH_VARARGS, "ImGui::Selectable"},
        {"Selectable_2", imgui_Selectable_2, METH_VARARGS, "ImGui::Selectable"},
        {"BeginListBox", imgui_BeginListBox, METH_VARARGS, "ImGui::BeginListBox"},
        {"EndListBox", imgui_EndListBox, METH_VARARGS, "ImGui::EndListBox"},
        {"PlotHistogram", imgui_PlotHistogram, METH_VARARGS, "ImGui::PlotHistogram"},
        {"Value", imgui_Value, METH_VARARGS, "ImGui::Value"},
        {"Value_2", imgui_Value_2, METH_VARARGS, "ImGui::Value"},
        {"Value_3", imgui_Value_3, METH_VARARGS, "ImGui::Value"},
        {"Value_4", imgui_Value_4, METH_VARARGS, "ImGui::Value"},
        {"BeginMenuBar", imgui_BeginMenuBar, METH_VARARGS, "ImGui::BeginMenuBar"},
        {"EndMenuBar", imgui_EndMenuBar, METH_VARARGS, "ImGui::EndMenuBar"},
        {"BeginMainMenuBar", imgui_BeginMainMenuBar, METH_VARARGS, "ImGui::BeginMainMenuBar"},
        {"EndMainMenuBar", imgui_EndMainMenuBar, METH_VARARGS, "ImGui::EndMainMenuBar"},
        {"BeginMenu", imgui_BeginMenu, METH_VARARGS, "ImGui::BeginMenu"},
        {"EndMenu", imgui_EndMenu, METH_VARARGS, "ImGui::EndMenu"},
        {"MenuItem", imgui_MenuItem, METH_VARARGS, "ImGui::MenuItem"},
        {"MenuItem_2", imgui_MenuItem_2, METH_VARARGS, "ImGui::MenuItem"},
        {"BeginTooltip", imgui_BeginTooltip, METH_VARARGS, "ImGui::BeginTooltip"},
        {"EndTooltip", imgui_EndTooltip, METH_VARARGS, "ImGui::EndTooltip"},
        {"SetTooltip", imgui_SetTooltip, METH_VARARGS, "ImGui::SetTooltip"},
        {"BeginPopup", imgui_BeginPopup, METH_VARARGS, "ImGui::BeginPopup"},
        {"BeginPopupModal", imgui_BeginPopupModal, METH_VARARGS, "ImGui::BeginPopupModal"},
        {"EndPopup", imgui_EndPopup, METH_VARARGS, "ImGui::EndPopup"},
        {"OpenPopup", imgui_OpenPopup, METH_VARARGS, "ImGui::OpenPopup"},
        {"OpenPopup_2", imgui_OpenPopup_2, METH_VARARGS, "ImGui::OpenPopup"},
        {"OpenPopupOnItemClick", imgui_OpenPopupOnItemClick, METH_VARARGS, "ImGui::OpenPopupOnItemClick"},
        {"CloseCurrentPopup", imgui_CloseCurrentPopup, METH_VARARGS, "ImGui::CloseCurrentPopup"},
        {"BeginPopupContextItem", imgui_BeginPopupContextItem, METH_VARARGS, "ImGui::BeginPopupContextItem"},
        {"BeginPopupContextWindow", imgui_BeginPopupContextWindow, METH_VARARGS, "ImGui::BeginPopupContextWindow"},
        {"BeginPopupContextVoid", imgui_BeginPopupContextVoid, METH_VARARGS, "ImGui::BeginPopupContextVoid"},
        {"IsPopupOpen", imgui_IsPopupOpen, METH_VARARGS, "ImGui::IsPopupOpen"},
        {"BeginTable", imgui_BeginTable, METH_VARARGS, "ImGui::BeginTable"},
        {"EndTable", imgui_EndTable, METH_VARARGS, "ImGui::EndTable"},
        {"TableNextRow", imgui_TableNextRow, METH_VARARGS, "ImGui::TableNextRow"},
        {"TableNextColumn", imgui_TableNextColumn, METH_VARARGS, "ImGui::TableNextColumn"},
        {"TableSetColumnIndex", imgui_TableSetColumnIndex, METH_VARARGS, "ImGui::TableSetColumnIndex"},
        {"TableSetupColumn", imgui_TableSetupColumn, METH_VARARGS, "ImGui::TableSetupColumn"},
        {"TableSetupScrollFreeze", imgui_TableSetupScrollFreeze, METH_VARARGS, "ImGui::TableSetupScrollFreeze"},
        {"TableHeadersRow", imgui_TableHeadersRow, METH_VARARGS, "ImGui::TableHeadersRow"},
        {"TableHeader", imgui_TableHeader, METH_VARARGS, "ImGui::TableHeader"},
        {"TableGetSortSpecs", imgui_TableGetSortSpecs, METH_VARARGS, "ImGui::TableGetSortSpecs"},
        {"TableGetColumnCount", imgui_TableGetColumnCount, METH_VARARGS, "ImGui::TableGetColumnCount"},
        {"TableGetColumnIndex", imgui_TableGetColumnIndex, METH_VARARGS, "ImGui::TableGetColumnIndex"},
        {"TableGetRowIndex", imgui_TableGetRowIndex, METH_VARARGS, "ImGui::TableGetRowIndex"},
        {"TableGetColumnName", imgui_TableGetColumnName, METH_VARARGS, "ImGui::TableGetColumnName"},
        {"TableGetColumnFlags", imgui_TableGetColumnFlags, METH_VARARGS, "ImGui::TableGetColumnFlags"},
        {"TableSetColumnEnabled", imgui_TableSetColumnEnabled, METH_VARARGS, "ImGui::TableSetColumnEnabled"},
        {"TableSetBgColor", imgui_TableSetBgColor, METH_VARARGS, "ImGui::TableSetBgColor"},
        {"Columns", imgui_Columns, METH_VARARGS, "ImGui::Columns"},
        {"NextColumn", imgui_NextColumn, METH_VARARGS, "ImGui::NextColumn"},
        {"GetColumnIndex", imgui_GetColumnIndex, METH_VARARGS, "ImGui::GetColumnIndex"},
        {"GetColumnWidth", imgui_GetColumnWidth, METH_VARARGS, "ImGui::GetColumnWidth"},
        {"SetColumnWidth", imgui_SetColumnWidth, METH_VARARGS, "ImGui::SetColumnWidth"},
        {"GetColumnOffset", imgui_GetColumnOffset, METH_VARARGS, "ImGui::GetColumnOffset"},
        {"SetColumnOffset", imgui_SetColumnOffset, METH_VARARGS, "ImGui::SetColumnOffset"},
        {"GetColumnsCount", imgui_GetColumnsCount, METH_VARARGS, "ImGui::GetColumnsCount"},
        {"BeginTabBar", imgui_BeginTabBar, METH_VARARGS, "ImGui::BeginTabBar"},
        {"EndTabBar", imgui_EndTabBar, METH_VARARGS, "ImGui::EndTabBar"},
        {"BeginTabItem", imgui_BeginTabItem, METH_VARARGS, "ImGui::BeginTabItem"},
        {"EndTabItem", imgui_EndTabItem, METH_VARARGS, "ImGui::EndTabItem"},
        {"TabItemButton", imgui_TabItemButton, METH_VARARGS, "ImGui::TabItemButton"},
        {"SetTabItemClosed", imgui_SetTabItemClosed, METH_VARARGS, "ImGui::SetTabItemClosed"},
        {"DockSpace", imgui_DockSpace, METH_VARARGS, "ImGui::DockSpace"},
        {"DockSpaceOverViewport", imgui_DockSpaceOverViewport, METH_VARARGS, "ImGui::DockSpaceOverViewport"},
        {"SetNextWindowDockID", imgui_SetNextWindowDockID, METH_VARARGS, "ImGui::SetNextWindowDockID"},
        {"SetNextWindowClass", imgui_SetNextWindowClass, METH_VARARGS, "ImGui::SetNextWindowClass"},
        {"GetWindowDockID", imgui_GetWindowDockID, METH_VARARGS, "ImGui::GetWindowDockID"},
        {"IsWindowDocked", imgui_IsWindowDocked, METH_VARARGS, "ImGui::IsWindowDocked"},
        {"LogToTTY", imgui_LogToTTY, METH_VARARGS, "ImGui::LogToTTY"},
        {"LogToFile", imgui_LogToFile, METH_VARARGS, "ImGui::LogToFile"},
        {"LogToClipboard", imgui_LogToClipboard, METH_VARARGS, "ImGui::LogToClipboard"},
        {"LogFinish", imgui_LogFinish, METH_VARARGS, "ImGui::LogFinish"},
        {"LogButtons", imgui_LogButtons, METH_VARARGS, "ImGui::LogButtons"},
        {"LogText", imgui_LogText, METH_VARARGS, "ImGui::LogText"},
        {"BeginDragDropSource", imgui_BeginDragDropSource, METH_VARARGS, "ImGui::BeginDragDropSource"},
        {"SetDragDropPayload", imgui_SetDragDropPayload, METH_VARARGS, "ImGui::SetDragDropPayload"},
        {"EndDragDropSource", imgui_EndDragDropSource, METH_VARARGS, "ImGui::EndDragDropSource"},
        {"BeginDragDropTarget", imgui_BeginDragDropTarget, METH_VARARGS, "ImGui::BeginDragDropTarget"},
        {"AcceptDragDropPayload", imgui_AcceptDragDropPayload, METH_VARARGS, "ImGui::AcceptDragDropPayload"},
        {"EndDragDropTarget", imgui_EndDragDropTarget, METH_VARARGS, "ImGui::EndDragDropTarget"},
        {"GetDragDropPayload", imgui_GetDragDropPayload, METH_VARARGS, "ImGui::GetDragDropPayload"},
        {"BeginDisabled", imgui_BeginDisabled, METH_VARARGS, "ImGui::BeginDisabled"},
        {"EndDisabled", imgui_EndDisabled, METH_VARARGS, "ImGui::EndDisabled"},
        {"PushClipRect", imgui_PushClipRect, METH_VARARGS, "ImGui::PushClipRect"},
        {"PopClipRect", imgui_PopClipRect, METH_VARARGS, "ImGui::PopClipRect"},
        {"SetItemDefaultFocus", imgui_SetItemDefaultFocus, METH_VARARGS, "ImGui::SetItemDefaultFocus"},
        {"SetKeyboardFocusHere", imgui_SetKeyboardFocusHere, METH_VARARGS, "ImGui::SetKeyboardFocusHere"},
        {"IsItemHovered", imgui_IsItemHovered, METH_VARARGS, "ImGui::IsItemHovered"},
        {"IsItemActive", imgui_IsItemActive, METH_VARARGS, "ImGui::IsItemActive"},
        {"IsItemFocused", imgui_IsItemFocused, METH_VARARGS, "ImGui::IsItemFocused"},
        {"IsItemClicked", imgui_IsItemClicked, METH_VARARGS, "ImGui::IsItemClicked"},
        {"IsItemVisible", imgui_IsItemVisible, METH_VARARGS, "ImGui::IsItemVisible"},
        {"IsItemEdited", imgui_IsItemEdited, METH_VARARGS, "ImGui::IsItemEdited"},
        {"IsItemActivated", imgui_IsItemActivated, METH_VARARGS, "ImGui::IsItemActivated"},
        {"IsItemDeactivated", imgui_IsItemDeactivated, METH_VARARGS, "ImGui::IsItemDeactivated"},
        {"IsItemDeactivatedAfterEdit", imgui_IsItemDeactivatedAfterEdit, METH_VARARGS, "ImGui::IsItemDeactivatedAfterEdit"},
        {"IsItemToggledOpen", imgui_IsItemToggledOpen, METH_VARARGS, "ImGui::IsItemToggledOpen"},
        {"IsAnyItemHovered", imgui_IsAnyItemHovered, METH_VARARGS, "ImGui::IsAnyItemHovered"},
        {"IsAnyItemActive", imgui_IsAnyItemActive, METH_VARARGS, "ImGui::IsAnyItemActive"},
        {"IsAnyItemFocused", imgui_IsAnyItemFocused, METH_VARARGS, "ImGui::IsAnyItemFocused"},
        {"GetItemRectMin", imgui_GetItemRectMin, METH_VARARGS, "ImGui::GetItemRectMin"},
        {"GetItemRectMax", imgui_GetItemRectMax, METH_VARARGS, "ImGui::GetItemRectMax"},
        {"GetItemRectSize", imgui_GetItemRectSize, METH_VARARGS, "ImGui::GetItemRectSize"},
        {"SetItemAllowOverlap", imgui_SetItemAllowOverlap, METH_VARARGS, "ImGui::SetItemAllowOverlap"},
        {"GetMainViewport", imgui_GetMainViewport, METH_VARARGS, "ImGui::GetMainViewport"},
        {"IsRectVisible", imgui_IsRectVisible, METH_VARARGS, "ImGui::IsRectVisible"},
        {"IsRectVisible_2", imgui_IsRectVisible_2, METH_VARARGS, "ImGui::IsRectVisible"},
        {"GetTime", imgui_GetTime, METH_VARARGS, "ImGui::GetTime"},
        {"GetFrameCount", imgui_GetFrameCount, METH_VARARGS, "ImGui::GetFrameCount"},
        {"GetBackgroundDrawList", imgui_GetBackgroundDrawList, METH_VARARGS, "ImGui::GetBackgroundDrawList"},
        {"GetForegroundDrawList", imgui_GetForegroundDrawList, METH_VARARGS, "ImGui::GetForegroundDrawList"},
        {"GetBackgroundDrawList_2", imgui_GetBackgroundDrawList_2, METH_VARARGS, "ImGui::GetBackgroundDrawList"},
        {"GetForegroundDrawList_2", imgui_GetForegroundDrawList_2, METH_VARARGS, "ImGui::GetForegroundDrawList"},
        {"GetDrawListSharedData", imgui_GetDrawListSharedData, METH_VARARGS, "ImGui::GetDrawListSharedData"},
        {"GetStyleColorName", imgui_GetStyleColorName, METH_VARARGS, "ImGui::GetStyleColorName"},
        {"BeginChildFrame", imgui_BeginChildFrame, METH_VARARGS, "ImGui::BeginChildFrame"},
        {"EndChildFrame", imgui_EndChildFrame, METH_VARARGS, "ImGui::EndChildFrame"},
        {"CalcTextSize", imgui_CalcTextSize, METH_VARARGS, "ImGui::CalcTextSize"},
        {"ColorConvertU32ToFloat4", imgui_ColorConvertU32ToFloat4, METH_VARARGS, "ImGui::ColorConvertU32ToFloat4"},
        {"ColorConvertFloat4ToU32", imgui_ColorConvertFloat4ToU32, METH_VARARGS, "ImGui::ColorConvertFloat4ToU32"},
        {"ColorConvertRGBtoHSV", imgui_ColorConvertRGBtoHSV, METH_VARARGS, "ImGui::ColorConvertRGBtoHSV"},
        {"ColorConvertHSVtoRGB", imgui_ColorConvertHSVtoRGB, METH_VARARGS, "ImGui::ColorConvertHSVtoRGB"},
        {"GetKeyIndex", imgui_GetKeyIndex, METH_VARARGS, "ImGui::GetKeyIndex"},
        {"IsKeyDown", imgui_IsKeyDown, METH_VARARGS, "ImGui::IsKeyDown"},
        {"IsKeyPressed", imgui_IsKeyPressed, METH_VARARGS, "ImGui::IsKeyPressed"},
        {"IsKeyReleased", imgui_IsKeyReleased, METH_VARARGS, "ImGui::IsKeyReleased"},
        {"GetKeyPressedAmount", imgui_GetKeyPressedAmount, METH_VARARGS, "ImGui::GetKeyPressedAmount"},
        {"CaptureKeyboardFromApp", imgui_CaptureKeyboardFromApp, METH_VARARGS, "ImGui::CaptureKeyboardFromApp"},
        {"IsMouseDown", imgui_IsMouseDown, METH_VARARGS, "ImGui::IsMouseDown"},
        {"IsMouseClicked", imgui_IsMouseClicked, METH_VARARGS, "ImGui::IsMouseClicked"},
        {"IsMouseReleased", imgui_IsMouseReleased, METH_VARARGS, "ImGui::IsMouseReleased"},
        {"IsMouseDoubleClicked", imgui_IsMouseDoubleClicked, METH_VARARGS, "ImGui::IsMouseDoubleClicked"},
        {"GetMouseClickedCount", imgui_GetMouseClickedCount, METH_VARARGS, "ImGui::GetMouseClickedCount"},
        {"IsMouseHoveringRect", imgui_IsMouseHoveringRect, METH_VARARGS, "ImGui::IsMouseHoveringRect"},
        {"IsMousePosValid", imgui_IsMousePosValid, METH_VARARGS, "ImGui::IsMousePosValid"},
        {"IsAnyMouseDown", imgui_IsAnyMouseDown, METH_VARARGS, "ImGui::IsAnyMouseDown"},
        {"GetMousePos", imgui_GetMousePos, METH_VARARGS, "ImGui::GetMousePos"},
        {"GetMousePosOnOpeningCurrentPopup", imgui_GetMousePosOnOpeningCurrentPopup, METH_VARARGS, "ImGui::GetMousePosOnOpeningCurrentPopup"},
        {"IsMouseDragging", imgui_IsMouseDragging, METH_VARARGS, "ImGui::IsMouseDragging"},
        {"GetMouseDragDelta", imgui_GetMouseDragDelta, METH_VARARGS, "ImGui::GetMouseDragDelta"},
        {"ResetMouseDragDelta", imgui_ResetMouseDragDelta, METH_VARARGS, "ImGui::ResetMouseDragDelta"},
        {"GetMouseCursor", imgui_GetMouseCursor, METH_VARARGS, "ImGui::GetMouseCursor"},
        {"SetMouseCursor", imgui_SetMouseCursor, METH_VARARGS, "ImGui::SetMouseCursor"},
        {"CaptureMouseFromApp", imgui_CaptureMouseFromApp, METH_VARARGS, "ImGui::CaptureMouseFromApp"},
        {"GetClipboardText", imgui_GetClipboardText, METH_VARARGS, "ImGui::GetClipboardText"},
        {"SetClipboardText", imgui_SetClipboardText, METH_VARARGS, "ImGui::SetClipboardText"},
        {"LoadIniSettingsFromDisk", imgui_LoadIniSettingsFromDisk, METH_VARARGS, "ImGui::LoadIniSettingsFromDisk"},
        {"LoadIniSettingsFromMemory", imgui_LoadIniSettingsFromMemory, METH_VARARGS, "ImGui::LoadIniSettingsFromMemory"},
        {"SaveIniSettingsToDisk", imgui_SaveIniSettingsToDisk, METH_VARARGS, "ImGui::SaveIniSettingsToDisk"},
        {"SaveIniSettingsToMemory", imgui_SaveIniSettingsToMemory, METH_VARARGS, "ImGui::SaveIniSettingsToMemory"},
        {"DebugCheckVersionAndDataLayout", imgui_DebugCheckVersionAndDataLayout, METH_VARARGS, "ImGui::DebugCheckVersionAndDataLayout"},
        {"MemAlloc", imgui_MemAlloc, METH_VARARGS, "ImGui::MemAlloc"},
        {"MemFree", imgui_MemFree, METH_VARARGS, "ImGui::MemFree"},
        {"GetPlatformIO", imgui_GetPlatformIO, METH_VARARGS, "ImGui::GetPlatformIO"},
        {"UpdatePlatformWindows", imgui_UpdatePlatformWindows, METH_VARARGS, "ImGui::UpdatePlatformWindows"},
        {"RenderPlatformWindowsDefault", imgui_RenderPlatformWindowsDefault, METH_VARARGS, "ImGui::RenderPlatformWindowsDefault"},
        {"DestroyPlatformWindows", imgui_DestroyPlatformWindows, METH_VARARGS, "ImGui::DestroyPlatformWindows"},
        {"FindViewportByID", imgui_FindViewportByID, METH_VARARGS, "ImGui::FindViewportByID"},
        {"FindViewportByPlatformHandle", imgui_FindViewportByPlatformHandle, METH_VARARGS, "ImGui::FindViewportByPlatformHandle"},
        {"CalcListClipping", imgui_CalcListClipping, METH_VARARGS, "ImGui::CalcListClipping"},
        {"GetWindowContentRegionWidth", imgui_GetWindowContentRegionWidth, METH_VARARGS, "ImGui::GetWindowContentRegionWidth"},
        {"ListBoxHeader", imgui_ListBoxHeader, METH_VARARGS, "ImGui::ListBoxHeader"},
        {"ListBoxHeader_2", imgui_ListBoxHeader_2, METH_VARARGS, "ImGui::ListBoxHeader"},
        {"ListBoxFooter", imgui_ListBoxFooter, METH_VARARGS, "ImGui::ListBoxFooter"},
        {"OpenPopupContextItem", imgui_OpenPopupContextItem, METH_VARARGS, "ImGui::OpenPopupContextItem"},
        {"DragScalar_2", imgui_DragScalar_2, METH_VARARGS, "ImGui::DragScalar"},
        {"DragScalarN_2", imgui_DragScalarN_2, METH_VARARGS, "ImGui::DragScalarN"},
        {"DragFloat_2", imgui_DragFloat_2, METH_VARARGS, "ImGui::DragFloat"},
        {"DragFloat2_2", imgui_DragFloat2_2, METH_VARARGS, "ImGui::DragFloat2"},
        {"DragFloat3_2", imgui_DragFloat3_2, METH_VARARGS, "ImGui::DragFloat3"},
        {"DragFloat4_2", imgui_DragFloat4_2, METH_VARARGS, "ImGui::DragFloat4"},
        {"SliderScalar_2", imgui_SliderScalar_2, METH_VARARGS, "ImGui::SliderScalar"},
        {"SliderScalarN_2", imgui_SliderScalarN_2, METH_VARARGS, "ImGui::SliderScalarN"},
        {"SliderFloat_2", imgui_SliderFloat_2, METH_VARARGS, "ImGui::SliderFloat"},
        {"SliderFloat2_2", imgui_SliderFloat2_2, METH_VARARGS, "ImGui::SliderFloat2"},
        {"SliderFloat3_2", imgui_SliderFloat3_2, METH_VARARGS, "ImGui::SliderFloat3"},
        {"SliderFloat4_2", imgui_SliderFloat4_2, METH_VARARGS, "ImGui::SliderFloat4"},
        {"BeginPopupContextWindow_2", imgui_BeginPopupContextWindow_2, METH_VARARGS, "ImGui::BeginPopupContextWindow"},
        {"TreeAdvanceToLabelPos", imgui_TreeAdvanceToLabelPos, METH_VARARGS, "ImGui::TreeAdvanceToLabelPos"},
        {"SetNextTreeNodeOpen", imgui_SetNextTreeNodeOpen, METH_VARARGS, "ImGui::SetNextTreeNodeOpen"},
        {"GetContentRegionAvailWidth", imgui_GetContentRegionAvailWidth, METH_VARARGS, "ImGui::GetContentRegionAvailWidth"},
        {"ImFontAtlas_AddFont", ImFontAtlas_AddFont, METH_VARARGS, "ImFontAtlas::AddFont"},
        {"ImFontAtlas_AddFontDefault", ImFontAtlas_AddFontDefault, METH_VARARGS, "ImFontAtlas::AddFontDefault"},
        {"ImFontAtlas_AddFontFromFileTTF", ImFontAtlas_AddFontFromFileTTF, METH_VARARGS, "ImFontAtlas::AddFontFromFileTTF"},
        {"ImFontAtlas_AddFontFromMemoryTTF", ImFontAtlas_AddFontFromMemoryTTF, METH_VARARGS, "ImFontAtlas::AddFontFromMemoryTTF"},
        {"ImFontAtlas_AddFontFromMemoryCompressedTTF", ImFontAtlas_AddFontFromMemoryCompressedTTF, METH_VARARGS, "ImFontAtlas::AddFontFromMemoryCompressedTTF"},
        {"ImFontAtlas_AddFontFromMemoryCompressedBase85TTF", ImFontAtlas_AddFontFromMemoryCompressedBase85TTF, METH_VARARGS, "ImFontAtlas::AddFontFromMemoryCompressedBase85TTF"},
        {"ImFontAtlas_ClearInputData", ImFontAtlas_ClearInputData, METH_VARARGS, "ImFontAtlas::ClearInputData"},
        {"ImFontAtlas_ClearTexData", ImFontAtlas_ClearTexData, METH_VARARGS, "ImFontAtlas::ClearTexData"},
        {"ImFontAtlas_ClearFonts", ImFontAtlas_ClearFonts, METH_VARARGS, "ImFontAtlas::ClearFonts"},
        {"ImFontAtlas_Clear", ImFontAtlas_Clear, METH_VARARGS, "ImFontAtlas::Clear"},
        {"ImFontAtlas_Build", ImFontAtlas_Build, METH_VARARGS, "ImFontAtlas::Build"},
        {"ImFontAtlas_GetTexDataAsAlpha8", ImFontAtlas_GetTexDataAsAlpha8, METH_VARARGS, "ImFontAtlas::GetTexDataAsAlpha8"},
        {"ImFontAtlas_GetTexDataAsRGBA32", ImFontAtlas_GetTexDataAsRGBA32, METH_VARARGS, "ImFontAtlas::GetTexDataAsRGBA32"},
        {"ImFontAtlas_IsBuilt", ImFontAtlas_IsBuilt, METH_VARARGS, "ImFontAtlas::IsBuilt"},
        {"ImFontAtlas_SetTexID", ImFontAtlas_SetTexID, METH_VARARGS, "ImFontAtlas::SetTexID"},
        {"ImFontAtlas_GetGlyphRangesDefault", ImFontAtlas_GetGlyphRangesDefault, METH_VARARGS, "ImFontAtlas::GetGlyphRangesDefault"},
        {"ImFontAtlas_GetGlyphRangesKorean", ImFontAtlas_GetGlyphRangesKorean, METH_VARARGS, "ImFontAtlas::GetGlyphRangesKorean"},
        {"ImFontAtlas_GetGlyphRangesJapanese", ImFontAtlas_GetGlyphRangesJapanese, METH_VARARGS, "ImFontAtlas::GetGlyphRangesJapanese"},
        {"ImFontAtlas_GetGlyphRangesChineseFull", ImFontAtlas_GetGlyphRangesChineseFull, METH_VARARGS, "ImFontAtlas::GetGlyphRangesChineseFull"},
        {"ImFontAtlas_GetGlyphRangesChineseSimplifiedCommon", ImFontAtlas_GetGlyphRangesChineseSimplifiedCommon, METH_VARARGS, "ImFontAtlas::GetGlyphRangesChineseSimplifiedCommon"},
        {"ImFontAtlas_GetGlyphRangesCyrillic", ImFontAtlas_GetGlyphRangesCyrillic, METH_VARARGS, "ImFontAtlas::GetGlyphRangesCyrillic"},
        {"ImFontAtlas_GetGlyphRangesThai", ImFontAtlas_GetGlyphRangesThai, METH_VARARGS, "ImFontAtlas::GetGlyphRangesThai"},
        {"ImFontAtlas_GetGlyphRangesVietnamese", ImFontAtlas_GetGlyphRangesVietnamese, METH_VARARGS, "ImFontAtlas::GetGlyphRangesVietnamese"},
        {"ImFontAtlas_AddCustomRectRegular", ImFontAtlas_AddCustomRectRegular, METH_VARARGS, "ImFontAtlas::AddCustomRectRegular"},
        {"ImFontAtlas_AddCustomRectFontGlyph", ImFontAtlas_AddCustomRectFontGlyph, METH_VARARGS, "ImFontAtlas::AddCustomRectFontGlyph"},
        {"ImFontAtlas_GetCustomRectByIndex", ImFontAtlas_GetCustomRectByIndex, METH_VARARGS, "ImFontAtlas::GetCustomRectByIndex"},
        {"ImFontAtlas_CalcCustomRectUV", ImFontAtlas_CalcCustomRectUV, METH_VARARGS, "ImFontAtlas::CalcCustomRectUV"},
        {"ImFontAtlas_GetMouseCursorTexData", ImFontAtlas_GetMouseCursorTexData, METH_VARARGS, "ImFontAtlas::GetMouseCursorTexData"},
        {"ImGuiViewport_GetCenter", ImGuiViewport_GetCenter, METH_VARARGS, "ImGuiViewport::GetCenter"},
        {"ImGuiViewport_GetWorkCenter", ImGuiViewport_GetWorkCenter, METH_VARARGS, "ImGuiViewport::GetWorkCenter"},
        // clang-format on
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "imgui", /* name of module */
        nullptr, /* module documentation, may be NULL */
        -1,      /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
        Methods};

    auto m = PyModule_Create(&module);
    assert(m);
    // if (!m){
    //     return NULL;
    // }

    // add submodule
    PyDict_SetItemString(__dict__, "pydear.impl.imgui", m);
}
  { // imnodes
    static PyMethodDef Methods[] = {
        // clang-format off
        {"SetImGuiContext", imnodes_SetImGuiContext, METH_VARARGS, "ImNodes::SetImGuiContext"},
        {"CreateContext", imnodes_CreateContext, METH_VARARGS, "ImNodes::CreateContext"},
        {"DestroyContext", imnodes_DestroyContext, METH_VARARGS, "ImNodes::DestroyContext"},
        {"GetCurrentContext", imnodes_GetCurrentContext, METH_VARARGS, "ImNodes::GetCurrentContext"},
        {"SetCurrentContext", imnodes_SetCurrentContext, METH_VARARGS, "ImNodes::SetCurrentContext"},
        {"EditorContextCreate", imnodes_EditorContextCreate, METH_VARARGS, "ImNodes::EditorContextCreate"},
        {"EditorContextFree", imnodes_EditorContextFree, METH_VARARGS, "ImNodes::EditorContextFree"},
        {"EditorContextSet", imnodes_EditorContextSet, METH_VARARGS, "ImNodes::EditorContextSet"},
        {"EditorContextGetPanning", imnodes_EditorContextGetPanning, METH_VARARGS, "ImNodes::EditorContextGetPanning"},
        {"EditorContextResetPanning", imnodes_EditorContextResetPanning, METH_VARARGS, "ImNodes::EditorContextResetPanning"},
        {"EditorContextMoveToNode", imnodes_EditorContextMoveToNode, METH_VARARGS, "ImNodes::EditorContextMoveToNode"},
        {"GetIO", imnodes_GetIO, METH_VARARGS, "ImNodes::GetIO"},
        {"GetStyle", imnodes_GetStyle, METH_VARARGS, "ImNodes::GetStyle"},
        {"StyleColorsDark", imnodes_StyleColorsDark, METH_VARARGS, "ImNodes::StyleColorsDark"},
        {"StyleColorsClassic", imnodes_StyleColorsClassic, METH_VARARGS, "ImNodes::StyleColorsClassic"},
        {"StyleColorsLight", imnodes_StyleColorsLight, METH_VARARGS, "ImNodes::StyleColorsLight"},
        {"BeginNodeEditor", imnodes_BeginNodeEditor, METH_VARARGS, "ImNodes::BeginNodeEditor"},
        {"EndNodeEditor", imnodes_EndNodeEditor, METH_VARARGS, "ImNodes::EndNodeEditor"},
        {"PushColorStyle", imnodes_PushColorStyle, METH_VARARGS, "ImNodes::PushColorStyle"},
        {"PopColorStyle", imnodes_PopColorStyle, METH_VARARGS, "ImNodes::PopColorStyle"},
        {"PushStyleVar", imnodes_PushStyleVar, METH_VARARGS, "ImNodes::PushStyleVar"},
        {"PushStyleVar_2", imnodes_PushStyleVar_2, METH_VARARGS, "ImNodes::PushStyleVar"},
        {"PopStyleVar", imnodes_PopStyleVar, METH_VARARGS, "ImNodes::PopStyleVar"},
        {"BeginNode", imnodes_BeginNode, METH_VARARGS, "ImNodes::BeginNode"},
        {"EndNode", imnodes_EndNode, METH_VARARGS, "ImNodes::EndNode"},
        {"GetNodeDimensions", imnodes_GetNodeDimensions, METH_VARARGS, "ImNodes::GetNodeDimensions"},
        {"BeginNodeTitleBar", imnodes_BeginNodeTitleBar, METH_VARARGS, "ImNodes::BeginNodeTitleBar"},
        {"EndNodeTitleBar", imnodes_EndNodeTitleBar, METH_VARARGS, "ImNodes::EndNodeTitleBar"},
        {"BeginInputAttribute", imnodes_BeginInputAttribute, METH_VARARGS, "ImNodes::BeginInputAttribute"},
        {"EndInputAttribute", imnodes_EndInputAttribute, METH_VARARGS, "ImNodes::EndInputAttribute"},
        {"BeginOutputAttribute", imnodes_BeginOutputAttribute, METH_VARARGS, "ImNodes::BeginOutputAttribute"},
        {"EndOutputAttribute", imnodes_EndOutputAttribute, METH_VARARGS, "ImNodes::EndOutputAttribute"},
        {"BeginStaticAttribute", imnodes_BeginStaticAttribute, METH_VARARGS, "ImNodes::BeginStaticAttribute"},
        {"EndStaticAttribute", imnodes_EndStaticAttribute, METH_VARARGS, "ImNodes::EndStaticAttribute"},
        {"PushAttributeFlag", imnodes_PushAttributeFlag, METH_VARARGS, "ImNodes::PushAttributeFlag"},
        {"PopAttributeFlag", imnodes_PopAttributeFlag, METH_VARARGS, "ImNodes::PopAttributeFlag"},
        {"Link", imnodes_Link, METH_VARARGS, "ImNodes::Link"},
        {"SetNodeDraggable", imnodes_SetNodeDraggable, METH_VARARGS, "ImNodes::SetNodeDraggable"},
        {"SetNodeScreenSpacePos", imnodes_SetNodeScreenSpacePos, METH_VARARGS, "ImNodes::SetNodeScreenSpacePos"},
        {"SetNodeEditorSpacePos", imnodes_SetNodeEditorSpacePos, METH_VARARGS, "ImNodes::SetNodeEditorSpacePos"},
        {"SetNodeGridSpacePos", imnodes_SetNodeGridSpacePos, METH_VARARGS, "ImNodes::SetNodeGridSpacePos"},
        {"GetNodeScreenSpacePos", imnodes_GetNodeScreenSpacePos, METH_VARARGS, "ImNodes::GetNodeScreenSpacePos"},
        {"GetNodeEditorSpacePos", imnodes_GetNodeEditorSpacePos, METH_VARARGS, "ImNodes::GetNodeEditorSpacePos"},
        {"GetNodeGridSpacePos", imnodes_GetNodeGridSpacePos, METH_VARARGS, "ImNodes::GetNodeGridSpacePos"},
        {"IsEditorHovered", imnodes_IsEditorHovered, METH_VARARGS, "ImNodes::IsEditorHovered"},
        {"IsNodeHovered", imnodes_IsNodeHovered, METH_VARARGS, "ImNodes::IsNodeHovered"},
        {"IsLinkHovered", imnodes_IsLinkHovered, METH_VARARGS, "ImNodes::IsLinkHovered"},
        {"IsPinHovered", imnodes_IsPinHovered, METH_VARARGS, "ImNodes::IsPinHovered"},
        {"NumSelectedNodes", imnodes_NumSelectedNodes, METH_VARARGS, "ImNodes::NumSelectedNodes"},
        {"NumSelectedLinks", imnodes_NumSelectedLinks, METH_VARARGS, "ImNodes::NumSelectedLinks"},
        {"GetSelectedNodes", imnodes_GetSelectedNodes, METH_VARARGS, "ImNodes::GetSelectedNodes"},
        {"GetSelectedLinks", imnodes_GetSelectedLinks, METH_VARARGS, "ImNodes::GetSelectedLinks"},
        {"ClearNodeSelection", imnodes_ClearNodeSelection, METH_VARARGS, "ImNodes::ClearNodeSelection"},
        {"ClearLinkSelection", imnodes_ClearLinkSelection, METH_VARARGS, "ImNodes::ClearLinkSelection"},
        {"SelectNode", imnodes_SelectNode, METH_VARARGS, "ImNodes::SelectNode"},
        {"ClearNodeSelection_2", imnodes_ClearNodeSelection_2, METH_VARARGS, "ImNodes::ClearNodeSelection"},
        {"IsNodeSelected", imnodes_IsNodeSelected, METH_VARARGS, "ImNodes::IsNodeSelected"},
        {"SelectLink", imnodes_SelectLink, METH_VARARGS, "ImNodes::SelectLink"},
        {"ClearLinkSelection_2", imnodes_ClearLinkSelection_2, METH_VARARGS, "ImNodes::ClearLinkSelection"},
        {"IsLinkSelected", imnodes_IsLinkSelected, METH_VARARGS, "ImNodes::IsLinkSelected"},
        {"IsAttributeActive", imnodes_IsAttributeActive, METH_VARARGS, "ImNodes::IsAttributeActive"},
        {"IsAnyAttributeActive", imnodes_IsAnyAttributeActive, METH_VARARGS, "ImNodes::IsAnyAttributeActive"},
        {"IsLinkStarted", imnodes_IsLinkStarted, METH_VARARGS, "ImNodes::IsLinkStarted"},
        {"IsLinkDropped", imnodes_IsLinkDropped, METH_VARARGS, "ImNodes::IsLinkDropped"},
        {"IsLinkCreated", imnodes_IsLinkCreated, METH_VARARGS, "ImNodes::IsLinkCreated"},
        {"IsLinkCreated_2", imnodes_IsLinkCreated_2, METH_VARARGS, "ImNodes::IsLinkCreated"},
        {"IsLinkDestroyed", imnodes_IsLinkDestroyed, METH_VARARGS, "ImNodes::IsLinkDestroyed"},
        {"SaveCurrentEditorStateToIniString", imnodes_SaveCurrentEditorStateToIniString, METH_VARARGS, "ImNodes::SaveCurrentEditorStateToIniString"},
        {"SaveEditorStateToIniString", imnodes_SaveEditorStateToIniString, METH_VARARGS, "ImNodes::SaveEditorStateToIniString"},
        {"LoadCurrentEditorStateFromIniString", imnodes_LoadCurrentEditorStateFromIniString, METH_VARARGS, "ImNodes::LoadCurrentEditorStateFromIniString"},
        {"LoadEditorStateFromIniString", imnodes_LoadEditorStateFromIniString, METH_VARARGS, "ImNodes::LoadEditorStateFromIniString"},
        {"SaveCurrentEditorStateToIniFile", imnodes_SaveCurrentEditorStateToIniFile, METH_VARARGS, "ImNodes::SaveCurrentEditorStateToIniFile"},
        {"SaveEditorStateToIniFile", imnodes_SaveEditorStateToIniFile, METH_VARARGS, "ImNodes::SaveEditorStateToIniFile"},
        {"LoadCurrentEditorStateFromIniFile", imnodes_LoadCurrentEditorStateFromIniFile, METH_VARARGS, "ImNodes::LoadCurrentEditorStateFromIniFile"},
        {"LoadEditorStateFromIniFile", imnodes_LoadEditorStateFromIniFile, METH_VARARGS, "ImNodes::LoadEditorStateFromIniFile"},
        // clang-format on
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "imnodes", /* name of module */
        nullptr, /* module documentation, may be NULL */
        -1,      /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
        Methods};

    auto m = PyModule_Create(&module);
    assert(m);
    // if (!m){
    //     return NULL;
    // }

    // add submodule
    PyDict_SetItemString(__dict__, "pydear.impl.imnodes", m);
}
  { // nanovg
    static PyMethodDef Methods[] = {
        // clang-format off
        {"nvgBeginFrame", nanovg_nvgBeginFrame, METH_VARARGS, "nvgBeginFrame"},
        {"nvgCancelFrame", nanovg_nvgCancelFrame, METH_VARARGS, "nvgCancelFrame"},
        {"nvgEndFrame", nanovg_nvgEndFrame, METH_VARARGS, "nvgEndFrame"},
        {"nvgGlobalCompositeOperation", nanovg_nvgGlobalCompositeOperation, METH_VARARGS, "nvgGlobalCompositeOperation"},
        {"nvgGlobalCompositeBlendFunc", nanovg_nvgGlobalCompositeBlendFunc, METH_VARARGS, "nvgGlobalCompositeBlendFunc"},
        {"nvgGlobalCompositeBlendFuncSeparate", nanovg_nvgGlobalCompositeBlendFuncSeparate, METH_VARARGS, "nvgGlobalCompositeBlendFuncSeparate"},
        {"nvgRGB", nanovg_nvgRGB, METH_VARARGS, "nvgRGB"},
        {"nvgRGBf", nanovg_nvgRGBf, METH_VARARGS, "nvgRGBf"},
        {"nvgRGBA", nanovg_nvgRGBA, METH_VARARGS, "nvgRGBA"},
        {"nvgRGBAf", nanovg_nvgRGBAf, METH_VARARGS, "nvgRGBAf"},
        {"nvgLerpRGBA", nanovg_nvgLerpRGBA, METH_VARARGS, "nvgLerpRGBA"},
        {"nvgTransRGBA", nanovg_nvgTransRGBA, METH_VARARGS, "nvgTransRGBA"},
        {"nvgTransRGBAf", nanovg_nvgTransRGBAf, METH_VARARGS, "nvgTransRGBAf"},
        {"nvgHSL", nanovg_nvgHSL, METH_VARARGS, "nvgHSL"},
        {"nvgHSLA", nanovg_nvgHSLA, METH_VARARGS, "nvgHSLA"},
        {"nvgSave", nanovg_nvgSave, METH_VARARGS, "nvgSave"},
        {"nvgRestore", nanovg_nvgRestore, METH_VARARGS, "nvgRestore"},
        {"nvgReset", nanovg_nvgReset, METH_VARARGS, "nvgReset"},
        {"nvgShapeAntiAlias", nanovg_nvgShapeAntiAlias, METH_VARARGS, "nvgShapeAntiAlias"},
        {"nvgStrokeColor", nanovg_nvgStrokeColor, METH_VARARGS, "nvgStrokeColor"},
        {"nvgStrokePaint", nanovg_nvgStrokePaint, METH_VARARGS, "nvgStrokePaint"},
        {"nvgFillColor", nanovg_nvgFillColor, METH_VARARGS, "nvgFillColor"},
        {"nvgFillPaint", nanovg_nvgFillPaint, METH_VARARGS, "nvgFillPaint"},
        {"nvgMiterLimit", nanovg_nvgMiterLimit, METH_VARARGS, "nvgMiterLimit"},
        {"nvgStrokeWidth", nanovg_nvgStrokeWidth, METH_VARARGS, "nvgStrokeWidth"},
        {"nvgLineCap", nanovg_nvgLineCap, METH_VARARGS, "nvgLineCap"},
        {"nvgLineJoin", nanovg_nvgLineJoin, METH_VARARGS, "nvgLineJoin"},
        {"nvgGlobalAlpha", nanovg_nvgGlobalAlpha, METH_VARARGS, "nvgGlobalAlpha"},
        {"nvgResetTransform", nanovg_nvgResetTransform, METH_VARARGS, "nvgResetTransform"},
        {"nvgTransform", nanovg_nvgTransform, METH_VARARGS, "nvgTransform"},
        {"nvgTranslate", nanovg_nvgTranslate, METH_VARARGS, "nvgTranslate"},
        {"nvgRotate", nanovg_nvgRotate, METH_VARARGS, "nvgRotate"},
        {"nvgSkewX", nanovg_nvgSkewX, METH_VARARGS, "nvgSkewX"},
        {"nvgSkewY", nanovg_nvgSkewY, METH_VARARGS, "nvgSkewY"},
        {"nvgScale", nanovg_nvgScale, METH_VARARGS, "nvgScale"},
        {"nvgCurrentTransform", nanovg_nvgCurrentTransform, METH_VARARGS, "nvgCurrentTransform"},
        {"nvgTransformIdentity", nanovg_nvgTransformIdentity, METH_VARARGS, "nvgTransformIdentity"},
        {"nvgTransformTranslate", nanovg_nvgTransformTranslate, METH_VARARGS, "nvgTransformTranslate"},
        {"nvgTransformScale", nanovg_nvgTransformScale, METH_VARARGS, "nvgTransformScale"},
        {"nvgTransformRotate", nanovg_nvgTransformRotate, METH_VARARGS, "nvgTransformRotate"},
        {"nvgTransformSkewX", nanovg_nvgTransformSkewX, METH_VARARGS, "nvgTransformSkewX"},
        {"nvgTransformSkewY", nanovg_nvgTransformSkewY, METH_VARARGS, "nvgTransformSkewY"},
        {"nvgTransformMultiply", nanovg_nvgTransformMultiply, METH_VARARGS, "nvgTransformMultiply"},
        {"nvgTransformPremultiply", nanovg_nvgTransformPremultiply, METH_VARARGS, "nvgTransformPremultiply"},
        {"nvgTransformInverse", nanovg_nvgTransformInverse, METH_VARARGS, "nvgTransformInverse"},
        {"nvgTransformPoint", nanovg_nvgTransformPoint, METH_VARARGS, "nvgTransformPoint"},
        {"nvgDegToRad", nanovg_nvgDegToRad, METH_VARARGS, "nvgDegToRad"},
        {"nvgRadToDeg", nanovg_nvgRadToDeg, METH_VARARGS, "nvgRadToDeg"},
        {"nvgCreateImage", nanovg_nvgCreateImage, METH_VARARGS, "nvgCreateImage"},
        {"nvgCreateImageMem", nanovg_nvgCreateImageMem, METH_VARARGS, "nvgCreateImageMem"},
        {"nvgCreateImageRGBA", nanovg_nvgCreateImageRGBA, METH_VARARGS, "nvgCreateImageRGBA"},
        {"nvgUpdateImage", nanovg_nvgUpdateImage, METH_VARARGS, "nvgUpdateImage"},
        {"nvgImageSize", nanovg_nvgImageSize, METH_VARARGS, "nvgImageSize"},
        {"nvgDeleteImage", nanovg_nvgDeleteImage, METH_VARARGS, "nvgDeleteImage"},
        {"nvgLinearGradient", nanovg_nvgLinearGradient, METH_VARARGS, "nvgLinearGradient"},
        {"nvgBoxGradient", nanovg_nvgBoxGradient, METH_VARARGS, "nvgBoxGradient"},
        {"nvgRadialGradient", nanovg_nvgRadialGradient, METH_VARARGS, "nvgRadialGradient"},
        {"nvgImagePattern", nanovg_nvgImagePattern, METH_VARARGS, "nvgImagePattern"},
        {"nvgScissor", nanovg_nvgScissor, METH_VARARGS, "nvgScissor"},
        {"nvgIntersectScissor", nanovg_nvgIntersectScissor, METH_VARARGS, "nvgIntersectScissor"},
        {"nvgResetScissor", nanovg_nvgResetScissor, METH_VARARGS, "nvgResetScissor"},
        {"nvgBeginPath", nanovg_nvgBeginPath, METH_VARARGS, "nvgBeginPath"},
        {"nvgMoveTo", nanovg_nvgMoveTo, METH_VARARGS, "nvgMoveTo"},
        {"nvgLineTo", nanovg_nvgLineTo, METH_VARARGS, "nvgLineTo"},
        {"nvgBezierTo", nanovg_nvgBezierTo, METH_VARARGS, "nvgBezierTo"},
        {"nvgQuadTo", nanovg_nvgQuadTo, METH_VARARGS, "nvgQuadTo"},
        {"nvgArcTo", nanovg_nvgArcTo, METH_VARARGS, "nvgArcTo"},
        {"nvgClosePath", nanovg_nvgClosePath, METH_VARARGS, "nvgClosePath"},
        {"nvgPathWinding", nanovg_nvgPathWinding, METH_VARARGS, "nvgPathWinding"},
        {"nvgArc", nanovg_nvgArc, METH_VARARGS, "nvgArc"},
        {"nvgRect", nanovg_nvgRect, METH_VARARGS, "nvgRect"},
        {"nvgRoundedRect", nanovg_nvgRoundedRect, METH_VARARGS, "nvgRoundedRect"},
        {"nvgRoundedRectVarying", nanovg_nvgRoundedRectVarying, METH_VARARGS, "nvgRoundedRectVarying"},
        {"nvgEllipse", nanovg_nvgEllipse, METH_VARARGS, "nvgEllipse"},
        {"nvgCircle", nanovg_nvgCircle, METH_VARARGS, "nvgCircle"},
        {"nvgFill", nanovg_nvgFill, METH_VARARGS, "nvgFill"},
        {"nvgStroke", nanovg_nvgStroke, METH_VARARGS, "nvgStroke"},
        {"nvgCreateFont", nanovg_nvgCreateFont, METH_VARARGS, "nvgCreateFont"},
        {"nvgCreateFontAtIndex", nanovg_nvgCreateFontAtIndex, METH_VARARGS, "nvgCreateFontAtIndex"},
        {"nvgCreateFontMem", nanovg_nvgCreateFontMem, METH_VARARGS, "nvgCreateFontMem"},
        {"nvgCreateFontMemAtIndex", nanovg_nvgCreateFontMemAtIndex, METH_VARARGS, "nvgCreateFontMemAtIndex"},
        {"nvgFindFont", nanovg_nvgFindFont, METH_VARARGS, "nvgFindFont"},
        {"nvgAddFallbackFontId", nanovg_nvgAddFallbackFontId, METH_VARARGS, "nvgAddFallbackFontId"},
        {"nvgAddFallbackFont", nanovg_nvgAddFallbackFont, METH_VARARGS, "nvgAddFallbackFont"},
        {"nvgResetFallbackFontsId", nanovg_nvgResetFallbackFontsId, METH_VARARGS, "nvgResetFallbackFontsId"},
        {"nvgResetFallbackFonts", nanovg_nvgResetFallbackFonts, METH_VARARGS, "nvgResetFallbackFonts"},
        {"nvgFontSize", nanovg_nvgFontSize, METH_VARARGS, "nvgFontSize"},
        {"nvgFontBlur", nanovg_nvgFontBlur, METH_VARARGS, "nvgFontBlur"},
        {"nvgTextLetterSpacing", nanovg_nvgTextLetterSpacing, METH_VARARGS, "nvgTextLetterSpacing"},
        {"nvgTextLineHeight", nanovg_nvgTextLineHeight, METH_VARARGS, "nvgTextLineHeight"},
        {"nvgTextAlign", nanovg_nvgTextAlign, METH_VARARGS, "nvgTextAlign"},
        {"nvgFontFaceId", nanovg_nvgFontFaceId, METH_VARARGS, "nvgFontFaceId"},
        {"nvgFontFace", nanovg_nvgFontFace, METH_VARARGS, "nvgFontFace"},
        {"nvgText", nanovg_nvgText, METH_VARARGS, "nvgText"},
        {"nvgTextBox", nanovg_nvgTextBox, METH_VARARGS, "nvgTextBox"},
        {"nvgTextBounds", nanovg_nvgTextBounds, METH_VARARGS, "nvgTextBounds"},
        {"nvgTextBoxBounds", nanovg_nvgTextBoxBounds, METH_VARARGS, "nvgTextBoxBounds"},
        {"nvgTextGlyphPositions", nanovg_nvgTextGlyphPositions, METH_VARARGS, "nvgTextGlyphPositions"},
        {"nvgTextMetrics", nanovg_nvgTextMetrics, METH_VARARGS, "nvgTextMetrics"},
        {"nvgTextBreakLines", nanovg_nvgTextBreakLines, METH_VARARGS, "nvgTextBreakLines"},
        {"nvgCreateInternal", nanovg_nvgCreateInternal, METH_VARARGS, "nvgCreateInternal"},
        {"nvgDeleteInternal", nanovg_nvgDeleteInternal, METH_VARARGS, "nvgDeleteInternal"},
        {"nvgInternalParams", nanovg_nvgInternalParams, METH_VARARGS, "nvgInternalParams"},
        {"nvgDebugDumpPathCache", nanovg_nvgDebugDumpPathCache, METH_VARARGS, "nvgDebugDumpPathCache"},
        // clang-format on
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "nanovg", /* name of module */
        nullptr, /* module documentation, may be NULL */
        -1,      /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
        Methods};

    auto m = PyModule_Create(&module);
    assert(m);
    // if (!m){
    //     return NULL;
    // }

    // add submodule
    PyDict_SetItemString(__dict__, "pydear.impl.nanovg", m);
}
  { // glew
    static PyMethodDef Methods[] = {
        // clang-format off
        {"glewInit", glew_glewInit, METH_VARARGS, "glewInit"},
        // clang-format on
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "glew", /* name of module */
        nullptr, /* module documentation, may be NULL */
        -1,      /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
        Methods};

    auto m = PyModule_Create(&module);
    assert(m);
    // if (!m){
    //     return NULL;
    // }

    // add submodule
    PyDict_SetItemString(__dict__, "pydear.impl.glew", m);
}
  { // nanovg_gl
    static PyMethodDef Methods[] = {
        // clang-format off
        {"nvgCreateGL3", nanovg_gl_nvgCreateGL3, METH_VARARGS, "nvgCreateGL3"},
        {"nvgDeleteGL3", nanovg_gl_nvgDeleteGL3, METH_VARARGS, "nvgDeleteGL3"},
        {"nvglCreateImageFromHandleGL3", nanovg_gl_nvglCreateImageFromHandleGL3, METH_VARARGS, "nvglCreateImageFromHandleGL3"},
        {"nvglImageHandleGL3", nanovg_gl_nvglImageHandleGL3, METH_VARARGS, "nvglImageHandleGL3"},
        {"glnvg__maxi", nanovg_gl_glnvg__maxi, METH_VARARGS, "glnvg__maxi"},
        {"glnvg__bindTexture", nanovg_gl_glnvg__bindTexture, METH_VARARGS, "glnvg__bindTexture"},
        {"glnvg__stencilMask", nanovg_gl_glnvg__stencilMask, METH_VARARGS, "glnvg__stencilMask"},
        {"glnvg__blendFuncSeparate", nanovg_gl_glnvg__blendFuncSeparate, METH_VARARGS, "glnvg__blendFuncSeparate"},
        {"glnvg__allocTexture", nanovg_gl_glnvg__allocTexture, METH_VARARGS, "glnvg__allocTexture"},
        {"glnvg__findTexture", nanovg_gl_glnvg__findTexture, METH_VARARGS, "glnvg__findTexture"},
        {"glnvg__deleteTexture", nanovg_gl_glnvg__deleteTexture, METH_VARARGS, "glnvg__deleteTexture"},
        {"glnvg__dumpShaderError", nanovg_gl_glnvg__dumpShaderError, METH_VARARGS, "glnvg__dumpShaderError"},
        {"glnvg__dumpProgramError", nanovg_gl_glnvg__dumpProgramError, METH_VARARGS, "glnvg__dumpProgramError"},
        {"glnvg__checkError", nanovg_gl_glnvg__checkError, METH_VARARGS, "glnvg__checkError"},
        {"glnvg__createShader", nanovg_gl_glnvg__createShader, METH_VARARGS, "glnvg__createShader"},
        {"glnvg__deleteShader", nanovg_gl_glnvg__deleteShader, METH_VARARGS, "glnvg__deleteShader"},
        {"glnvg__getUniforms", nanovg_gl_glnvg__getUniforms, METH_VARARGS, "glnvg__getUniforms"},
        {"glnvg__renderCreateTexture", nanovg_gl_glnvg__renderCreateTexture, METH_VARARGS, "glnvg__renderCreateTexture"},
        {"glnvg__renderCreate", nanovg_gl_glnvg__renderCreate, METH_VARARGS, "glnvg__renderCreate"},
        {"glnvg__renderCreateTexture_2", nanovg_gl_glnvg__renderCreateTexture_2, METH_VARARGS, "glnvg__renderCreateTexture"},
        {"glnvg__renderDeleteTexture", nanovg_gl_glnvg__renderDeleteTexture, METH_VARARGS, "glnvg__renderDeleteTexture"},
        {"glnvg__renderUpdateTexture", nanovg_gl_glnvg__renderUpdateTexture, METH_VARARGS, "glnvg__renderUpdateTexture"},
        {"glnvg__renderGetTextureSize", nanovg_gl_glnvg__renderGetTextureSize, METH_VARARGS, "glnvg__renderGetTextureSize"},
        {"glnvg__xformToMat3x4", nanovg_gl_glnvg__xformToMat3x4, METH_VARARGS, "glnvg__xformToMat3x4"},
        {"glnvg__premulColor", nanovg_gl_glnvg__premulColor, METH_VARARGS, "glnvg__premulColor"},
        {"glnvg__convertPaint", nanovg_gl_glnvg__convertPaint, METH_VARARGS, "glnvg__convertPaint"},
        {"nvg__fragUniformPtr", nanovg_gl_nvg__fragUniformPtr, METH_VARARGS, "nvg__fragUniformPtr"},
        {"glnvg__setUniforms", nanovg_gl_glnvg__setUniforms, METH_VARARGS, "glnvg__setUniforms"},
        {"glnvg__renderViewport", nanovg_gl_glnvg__renderViewport, METH_VARARGS, "glnvg__renderViewport"},
        {"glnvg__fill", nanovg_gl_glnvg__fill, METH_VARARGS, "glnvg__fill"},
        {"glnvg__convexFill", nanovg_gl_glnvg__convexFill, METH_VARARGS, "glnvg__convexFill"},
        {"glnvg__stroke", nanovg_gl_glnvg__stroke, METH_VARARGS, "glnvg__stroke"},
        {"glnvg__triangles", nanovg_gl_glnvg__triangles, METH_VARARGS, "glnvg__triangles"},
        {"glnvg__renderCancel", nanovg_gl_glnvg__renderCancel, METH_VARARGS, "glnvg__renderCancel"},
        {"glnvg_convertBlendFuncFactor", nanovg_gl_glnvg_convertBlendFuncFactor, METH_VARARGS, "glnvg_convertBlendFuncFactor"},
        {"glnvg__blendCompositeOperation", nanovg_gl_glnvg__blendCompositeOperation, METH_VARARGS, "glnvg__blendCompositeOperation"},
        {"glnvg__renderFlush", nanovg_gl_glnvg__renderFlush, METH_VARARGS, "glnvg__renderFlush"},
        {"glnvg__maxVertCount", nanovg_gl_glnvg__maxVertCount, METH_VARARGS, "glnvg__maxVertCount"},
        {"glnvg__allocCall", nanovg_gl_glnvg__allocCall, METH_VARARGS, "glnvg__allocCall"},
        {"glnvg__allocPaths", nanovg_gl_glnvg__allocPaths, METH_VARARGS, "glnvg__allocPaths"},
        {"glnvg__allocVerts", nanovg_gl_glnvg__allocVerts, METH_VARARGS, "glnvg__allocVerts"},
        {"glnvg__allocFragUniforms", nanovg_gl_glnvg__allocFragUniforms, METH_VARARGS, "glnvg__allocFragUniforms"},
        {"nvg__fragUniformPtr_2", nanovg_gl_nvg__fragUniformPtr_2, METH_VARARGS, "nvg__fragUniformPtr"},
        {"glnvg__vset", nanovg_gl_glnvg__vset, METH_VARARGS, "glnvg__vset"},
        {"glnvg__renderFill", nanovg_gl_glnvg__renderFill, METH_VARARGS, "glnvg__renderFill"},
        {"glnvg__renderStroke", nanovg_gl_glnvg__renderStroke, METH_VARARGS, "glnvg__renderStroke"},
        {"glnvg__renderTriangles", nanovg_gl_glnvg__renderTriangles, METH_VARARGS, "glnvg__renderTriangles"},
        {"glnvg__renderDelete", nanovg_gl_glnvg__renderDelete, METH_VARARGS, "glnvg__renderDelete"},
        {"nvgCreateGL3_2", nanovg_gl_nvgCreateGL3_2, METH_VARARGS, "nvgCreateGL3"},
        {"nvgDeleteGL3_2", nanovg_gl_nvgDeleteGL3_2, METH_VARARGS, "nvgDeleteGL3"},
        {"nvglCreateImageFromHandleGL3_2", nanovg_gl_nvglCreateImageFromHandleGL3_2, METH_VARARGS, "nvglCreateImageFromHandleGL3"},
        {"nvglImageHandleGL3_2", nanovg_gl_nvglImageHandleGL3_2, METH_VARARGS, "nvglImageHandleGL3"},
        // clang-format on
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "nanovg_gl", /* name of module */
        nullptr, /* module documentation, may be NULL */
        -1,      /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
        Methods};

    auto m = PyModule_Create(&module);
    assert(m);
    // if (!m){
    //     return NULL;
    // }

    // add submodule
    PyDict_SetItemString(__dict__, "pydear.impl.nanovg_gl", m);
}
  // clang-format on

  static auto ImplError = PyErr_NewException("impl.error", NULL, NULL);
  Py_XINCREF(ImplError);
  if (PyModule_AddObject(__root__, "error", ImplError) < 0) {
    Py_XDECREF(ImplError);
    Py_CLEAR(ImplError);
    Py_DECREF(__root__);
    return NULL;
  }

  s_initialize();

  return __root__;
}
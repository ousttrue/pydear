from typing import List, Tuple
import io
import pathlib
from clang import cindex
from .parser import Parser
from .header import Header
from .declarations.typewrap import TypeWrap
from . import interpreted_types

CTYPS_CAST = '''
template<typename T>
T ctypes_cast(PyObject *src)
{
    if(!src){
        return (T)nullptr;
    }

    static auto ctypes = PyImport_ImportModule("ctypes");
    static auto addressof = PyObject_GetAttrString(ctypes, "addressof");
    static auto ctypes_Array = PyObject_GetAttrString(ctypes, "Array");
    static auto ctypes_Structure = PyObject_GetAttrString(ctypes, "Structure");
    static auto c_void_p = PyObject_GetAttrString(ctypes, "c_void_p");
    static auto value = PyUnicode_FromString("value");

    // ctypes.c_void_p
    if(PyObject_IsInstance(src, c_void_p)){
        if(PyObject *p = PyObject_GetAttr(src, value))
        {
            return (T)PyLong_AsVoidPtr(p);
        }
    }

    // ctypes.Array   
    // ctypes.Structure
    if(PyObject_IsInstance(src, ctypes_Array) || PyObject_IsInstance(src, ctypes_Structure)){
        if(PyObject *p = PyObject_CallFunction(addressof, "O", src))
        {
            return (T)PyLong_AsVoidPtr(p);
        }
    }

    return (T)nullptr;
}

'''

C_VOID_P = '''
static PyObject* c_void_p(void* address)
{
    static auto ctypes = PyImport_ImportModule("ctypes");
    static auto c_void_p = PyObject_GetAttrString(ctypes, "c_void_p");
    
    return PyObject_CallFunction(c_void_p, "K", (uintptr_t)address);
}
'''


def get_namespace(cursors: Tuple[cindex.Cursor, ...]) -> str:
    sio = io.StringIO()
    for cursor in cursors:
        if cursor.kind == cindex.CursorKind.NAMESPACE:
            sio.write(f'{cursor.spelling}::')
    return sio.getvalue()


def get_params(indent: str, cursor: cindex.Cursor) -> Tuple[List[interpreted_types.basetype.BaseType], List[str], str, str]:
    sio_extract = io.StringIO()
    sio_cpp_from_py = io.StringIO()
    types = []
    defaults = []
    for i, param in enumerate(TypeWrap.get_function_params(cursor)):
        t = interpreted_types.from_cursor(param.type, param.cursor)
        sio_extract.write(t.cpp_param_declare(indent, i, param.name))
        types.append(t)
        defaults.append(param.default_value(use_filter=False))
        sio_cpp_from_py.write(t.cpp_from_py(indent, i))
    return types, defaults, sio_extract.getvalue(), sio_cpp_from_py.getvalue()


def write_header(w: io.IOBase, parser: Parser, header: Header):
    w.write(f'''
# include <{header.path.name}>

''')
    for f in parser.functions:
        if header.path != f.path:
            continue

        # signature
        namespace = get_namespace(f.cursors)
        result = TypeWrap.from_function_result(f.cursor)
        func_name = f'{header.path.stem}_{f.spelling}'
        indent = '  '
        w.write(
            f'static PyObject *{func_name}(PyObject *self, PyObject *args){{\n')

        # prams
        types, defaults, extract, cpp_from_py = get_params(indent, f.cursor)
        w.write(extract)

        format = ''
        last_d = None
        set_defaults = ''
        for t, d in zip(types, defaults):
            if not last_d and d:
                format += '|'
            last_d = d
            format += t.format
            set_defaults += f'{indent}if(!t0) t0{d};\n'

        extract_params = ''.join(', &' + t.cpp_extract_name(i)
                                 for i, t in enumerate(types))
        w.write(
            f'{indent}if(!PyArg_ParseTuple(args, "{format}"{extract_params})) return NULL;\n')

        w.write(set_defaults)

        w.write(cpp_from_py)

        # call & result
        call_params = ''.join(t.cpp_call_name(i) for i, t in enumerate(types))
        call = f'{namespace}{f.spelling}({call_params})'
        w.write(interpreted_types.from_cursor(
            result.type, result.cursor).cpp_result(indent, call))

        w.write(f'''}}

''')

        yield f'{{"{f.spelling}", {func_name}, METH_VARARGS, "{namespace}{f.spelling}"}},\n'
        break


def write(package_dir: pathlib.Path, parser: Parser, headers: List[Header]):

    cpp_path = package_dir / 'rawtypes/implmodule.cpp'
    cpp_path.parent.mkdir(parents=True, exist_ok=True)

    with cpp_path.open('w') as w:
        w.write('''// generated
# define PY_SSIZE_T_CLEAN
# include <Python.h>

''')

        w.write(CTYPS_CAST)
        w.write(C_VOID_P)

        sio = io.StringIO()
        for header in headers:
            for method in write_header(w, parser, header):
                sio.write(method)

        w.write(f'''
static PyMethodDef Methods[] = {{
    {sio.getvalue()}
    {{NULL, NULL, 0, NULL}}        /* Sentinel */
}};

static struct PyModuleDef module = {{
    PyModuleDef_HEAD_INIT,
    "impl",   /* name of module */
    nullptr, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    Methods
}};

PyMODINIT_FUNC
PyInit_impl(void)
{{
    auto m = PyModule_Create(&module);
    if (!m){{
        return NULL;
    }}

    static auto ImplError = PyErr_NewException("impl.error", NULL, NULL);
    Py_XINCREF(ImplError);
    if (PyModule_AddObject(m, "error", ImplError) < 0) {{
        Py_XDECREF(ImplError);
        Py_CLEAR(ImplError);
        Py_DECREF(m);
        return NULL;
    }}

    return m;
}}
''')

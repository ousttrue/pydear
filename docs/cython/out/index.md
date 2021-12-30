# out

関数返り値。

* python での表現(def 返り値)をどうするか
* C 表現(cdef) から python 表現に如何に変換するか

| c              | py                             | cdef                      | c_to_py                                    |
|----------------|--------------------------------|---------------------------|--------------------------------------------|
| struct Struct& | class Struct(ctypes.Structure) | cdef Struct r0* = &call() | ctypes.cast(r0, ctypes.POINTER(Struct))[0] |

## Struct &

```c++
Sturct& call();
```

```cython
class Struct(ctypes.Structure):
    pass

def call()->Struct:
    cdef Struct r0* = &call()
    return ctypes.cast(r0, ctypes.POINTER(Struct))[0]
```

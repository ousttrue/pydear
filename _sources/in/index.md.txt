# in

関数引き数。

* python での表現(def 引き数)をどうするか
* python 表現から、 C 表現(cdef)に如何に変換するか

| c     | py                | py_to_c                                                 |
|-------|-------------------|---------------------------------------------------------|
| int   | int               | cdef int c0 = p0                                        |
| bool* | ctypes.c_bool * 1 | cdef int* c0 = <bool*><uintptr_t>(ctypes.addressof(p0)) |

## primitive

```c++
void call(int a);
```

```cython
def call(a: int):
    cdef int p0 = a
    c_module.call(p0)
```

## pointer

```c++
void call(int *a);
```

ctypes

```cython
def call(a: ctypes.Array):
    cdef int *p0 = <int*><uintptr_t>(ctypes.addressof(a))
    c_module.call(p0)
```

view

```cython
def call(int[::1] a):
    cdef int *p0 = &a[0]
    c_module.call(p0)
```

## const char *

```c++
void call(const char *a);
```

```cython
def call(a: bytes):
    cdef const char*p0 = <const char*>a
    c_module.call(p0)
```

## const ImVec2&

```c++
void call(const ImVec2 &a);
```

?

```cython
def call(a: Tuple[float, float]):
    cdef ImVec2 p0(a[0], a[1])
    c_module.call(p0)
```

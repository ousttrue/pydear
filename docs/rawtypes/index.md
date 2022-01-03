# rawtypes

自前でコード生成する。

<https://docs.python.org/3/extending/extending.html>

## 関数

登録する関数のシグネチャーは以下の通り。

```c++
static PyObject *EXPORT_FUNC(PyObject *self, PyObject *args);
```

## 引数の取り出し

<https://docs.python.org/3/c-api/arg.html>

`PyObject *args` から値を取り出す。

-   <https://docs.python.org/3/extending/extending.html#extracting-parameters-in-extension-functions>
-   <https://docs.python.org/3/c-api/index.html>

### int, float, bool

* <https://docs.python.org/3/c-api/number.html>
* <https://docs.python.org/3/c-api/long.html>

### object

<https://docs.python.org/3/c-api/object.html>

### ctypes.c_void_p

-   <https://github.com/python/cpython/blob/main/Modules/_ctypes/ctypes.h>
-   <https://github.com/python/cpython/blob/main/Modules/_ctypes/_ctypes.c>

### ctypes.Array

## 返り値

`PyObject*` を返す。

### int, float, bool

### ctypes.c_void_p

### ctypes.Array

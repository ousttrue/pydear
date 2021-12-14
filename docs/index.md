# cydeer 🦌

実装メモ。

```{toctree}
:maxdepth: 2
:caption: Contents
```

## cython + ctypes

型の `wrap` を cython の `cdef class` ではなく、 `ctypes.Structure` で実装してみた。

* cython: imgui の statlic library からの関数呼び出し
* ctypes: ImGuiIO などの型の wrap。`c++` から得たポインタを `ctypes.Structure` にキャストしてる。

```python
def GetIO()->ImGuiIO:
    cdef cpp_imgui.ImGuiIO * value = &cpp_imgui.GetIO()
    # pointer を ctypes.Structure にキャストする
    return ctypes.cast(ctypes.c_void_p(<long long>value), ctypes.POINTER(ImGuiIO))[0]
```

* cython: class method の呼び出し

```python
class ImFontAtlas(ctypes.Structure):
    def ClearTexData(self, ):
        # self を pointer にキャスト  
        cdef cpp_imgui.ImFontAtlas *ptr = <cpp_imgui.ImFontAtlas*><uintptr_t>ctypes.addressof(self)
        # ptr からメソッド呼び出し
        ptr.ClearTexData()
```

ちと変則的だが、いい感じになった。

## 個別の型変換

### 引数

#### bytes

```python
def some(src: bytes):
    # cast で pointer を得る
    cdef const char *p = <const char *>src
```

### ImVec2, ImVec4

* NamedTuple にしたい

## Indices and tables

-   {ref}`genindex`
-   {ref}`modindex`
-   {ref}`search`

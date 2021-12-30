# cython

cython による imgui ラッパーの先人。 <https://github.com/pyimgui/pyimgui>

## cython + ctypes

型の `wrap` を cython の `cdef class` ではなく、 `ctypes.Structure` で実装してみた。

* cython: imgui の statlic library からの関数呼び出し
* ctypes: ImGuiIO などの型の wrap。`c++` から得たポインタを `ctypes.Structure` にキャストしてる。

```python
def GetIO()->ImGuiIO:
    cdef impl.ImGuiIO * value = &impl.GetIO()
    # pointer を ctypes.Structure にキャストする
    return ctypes.cast(ctypes.c_void_p(<long long>value), ctypes.POINTER(ImGuiIO))[0]
```

* cython: class method の呼び出し

```python
class ImFontAtlas(ctypes.Structure):
    def ClearTexData(self, ):
        # self を pointer にキャスト  
        cdef impl.ImFontAtlas *ptr = <impl.ImFontAtlas*><uintptr_t>ctypes.addressof(self)
        # ptr からメソッド呼び出し
        ptr.ClearTexData()
```

ちと変則的だが、いい感じになった。

## 個別の型変換

```{toctree}
:maxdepth: 2
in/index
out/index
```

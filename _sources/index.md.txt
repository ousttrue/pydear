# pydeer 🦌

`clang.cindex` で読み取ったヘッダ情報から `c++` コードを生成して作った `imgui` バインディング。

はじめ `clang.cindex` を使った `cython` のコード生成である程度動くところまで作ったのだけど、
`namespace` に入った型の取り扱いなど `c++` 要素が手に負えなくなってきたのを機に、 
`cython` じゃなくて `c++` を生成する方向に路線を変更した。

```{toctree}
rawtypes/index
```

`pybind11` の利用を検討したのだけど見送った。
不完全型のポインタを `ctypes.c_void_p` で返したかったのだけど方法がわからず。
`template` が手に負えなかったのである。

## 参考

* <https://github.com/pyimgui/pyimgui>

`cython` による `imgui` バインディング。
このライブラリを改造して使っていて、自作してみようと思った。

## Indices and tables

-   {ref}`genindex`
-   {ref}`modindex`
-   {ref}`search`

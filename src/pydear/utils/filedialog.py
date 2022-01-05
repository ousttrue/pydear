
from typing import Optional
import logging
import ctypes
import pathlib
from OpenGL import GL
import pydear as ImGui
logger = logging.getLogger(__name__)

# FileDialog
FILE_DIALOG = b'open file'


def create_texture(data: ctypes.c_void_p, w: int, h: int, fmt: int):
    tex = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(
        GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(
        GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(
        GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
    GL.glTexParameteri(
        GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, w, h, 0, GL.GL_BGRA if(
        fmt == 0) else GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, ctypes.c_void_p(data))
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
    logger.debug(f'filedialog: create texture: {tex}')
    return int(tex)


# delay texture deletion
DELETE_QUEUE = []


def delete_texture(tex):
    logger.debug(f'filedialog: delete texture: {tex}')
    DELETE_QUEUE.append(tex)


P_CREATE_TEXTURE = ctypes.CFUNCTYPE(
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char)(create_texture)
P_DELETE_TEXTURE = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(delete_texture)


# 違う !
# print(
#     ctypes.addressof(P_CREATE_TEXTURE), 
#     ctypes.cast(P_CREATE_TEXTURE, ctypes.c_void_p).value)


def initialize():
    ImGui.ImFileDialog_SetTextureCallback(
        ctypes.cast(P_CREATE_TEXTURE, ctypes.c_void_p),
        ctypes.cast(P_DELETE_TEXTURE, ctypes.c_void_p))


def open_menu(label: bytes):
    if ImGui.MenuItem(label, None, False, True):
        ImGui.ImFileDialog_Open(FILE_DIALOG, b'open file', b'*.txt')


def get_result() -> Optional[pathlib.Path]:
    if DELETE_QUEUE:
        logger.debug(f'file dialog delete: {DELETE_QUEUE}')
        GL.glDeleteTextures(DELETE_QUEUE)
        DELETE_QUEUE.clear()

    result = ImGui.ImFileDialog_GetResult(FILE_DIALOG)
    if result:
        return pathlib.Path(result.decode('utf-8'))

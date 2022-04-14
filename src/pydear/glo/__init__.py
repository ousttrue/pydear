'''
OpenGL Object Library
'''
from .vbo import Vbo, Ibo
from .shader import Shader, UniformLocation, UniformBlockIndex
from .texture import Texture
from .vertex_layout import AttributeLocation, VertexLayout
from .vao import Vao
from .fbo import Fbo, FboRenderer
from .drawable import Drawable, Submesh

__all__ = [
    'Vbo',
    'Ibo',
    'Shader',
    'UniformLocation',
    'ShaderProp',
    'UniformBlockIndex',
    'Texture',
    'AttributeLocation',
    'VertexLayout',
    'Vao',
    'Fbo',
    'FboRenderer',
    'Drawable',
    'Submesh',
]


def get_info():
    from OpenGL.GL import (glGetString, glGetIntegerv, GL_VENDOR, GL_VERSION,
                           GL_SHADING_LANGUAGE_VERSION, GL_RENDERER,
                           GL_MAJOR_VERSION, GL_MINOR_VERSION)
    return {
        'major': glGetIntegerv(GL_MAJOR_VERSION),
        'minor': glGetIntegerv(GL_MINOR_VERSION),
        'vendor': glGetString(GL_VENDOR),
        'version': glGetString(GL_VERSION),
        'shader_language_version': glGetString(GL_SHADING_LANGUAGE_VERSION),
        'renderer': glGetString(GL_RENDERER),
    }

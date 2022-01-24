from typing import NamedTuple
from OpenGL import GL
import logging
logger = logging.getLogger(__name__)


class Shader:
    def __init__(self, vs, fs) -> None:
        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)

    @staticmethod
    def load(vs, fs) -> 'Shader':
        vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(vertex_shader, vs, None)
        GL.glCompileShader(vertex_shader)

        fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(fragment_shader, fs, None)
        GL.glCompileShader(fragment_shader)

        return Shader(vertex_shader, fragment_shader)


class UniformLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program,  name: str) -> 'UniformLocation':
        return UniformLocation(name, GL.glGetUniformLocation(program, name))

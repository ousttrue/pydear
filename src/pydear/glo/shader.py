from typing import NamedTuple, Optional
from OpenGL import GL
import logging
logger = logging.getLogger(__name__)


class ShaderCompile:
    def __init__(self, shader_type):
        '''
        GL.GL_VERTEX_SHADER
        GL.GL_FRAGMENT_SHADER
        '''
        self.shader = GL.glCreateShader(shader_type)

    def compile(self, src: str) -> bool:
        GL.glShaderSource(self.shader, src, None)
        GL.glCompileShader(self.shader)
        result = GL.glGetShaderiv(self.shader, GL.GL_COMPILE_STATUS)
        if result == GL.GL_TRUE:
            return True
        # error message
        info = GL.glGetShaderInfoLog(self.shader)
        logging.error(info)
        return False

    def __del__(self):
        GL.glDeleteShader(self.shader)


class Shader:
    def __init__(self) -> None:
        self.program = GL.glCreateProgram()

    def __del__(self):
        GL.glDeleteProgram(self.program)

    def __enter__(self):
        self.use()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unuse()
        if exc_type:
            logger.warning(f'{exc_type}: {exc_value}: {traceback}')

    def link(self, vs, fs) -> bool:
        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)
        error = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
        if error == GL.GL_TRUE:
            return True
        # error message
        info = GL.glGetShaderInfoLog(self.program)
        logger.error(info)
        return False

    @staticmethod
    def load(vs_src: str, fs_src: str) -> Optional['Shader']:
        vs = ShaderCompile(GL.GL_VERTEX_SHADER)
        if not vs.compile(vs_src):
            return
        fs = ShaderCompile(GL.GL_FRAGMENT_SHADER)
        if not fs.compile(fs_src):
            return
        shader = Shader()
        if not shader.link(vs.shader, fs.shader):
            return
        return shader

    def use(self):
        GL.glUseProgram(self.program)

    def unuse(self):
        GL.glUseProgram(0)


class UniformLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program,  name: str) -> 'UniformLocation':
        return UniformLocation(name, GL.glGetUniformLocation(program, name))

    def set_mat4(self, value, transpose: bool = False):
        GL.glUniformMatrix4fv(
            self.location, 1, GL.GL_TRUE if transpose else GL.GL_FALSE, value)


class ShaderProp:
    def __init__(self, setter, getter) -> None:
        self.setter = setter
        self.getter = getter

    def update(self):
        self.setter(self.getter())

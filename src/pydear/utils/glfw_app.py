from typing import Tuple, NamedTuple, Optional
import asyncio
import json
import logging
import glfw
from OpenGL import GL
import ctypes
from .setting import BinSetting
logger = logging.getLogger(__name__)


class GlfwAppState(NamedTuple):
    width: int = 1024
    height: int = 768
    is_maximized: bool = False

    def to_json(self) -> str:
        return json.dumps(self._asdict())

    @staticmethod
    def load(data: bytes) -> 'GlfwAppState':
        try:
            state = GlfwAppState(**json.loads(data))
            logger.debug(f'load: ini')
            return state
        except:
            pass
        return GlfwAppState()


SETTING_KEY = 'glfw'


class GlfwApp:
    def __init__(self, title: str, *,
                 width=1024, height=768,
                 gl_major=4, gl_minor=3, use_core_profile=True,
                 use_vsync=True, setting: Optional[BinSetting] = None) -> None:

        self.setting = setting
        self.loop = asyncio.get_event_loop()

        def glfw_error_callback(error: int, description: str):
            logger.error(f"{error}: {description}")
        glfw.set_error_callback(glfw_error_callback)

        if not glfw.init():
            raise RuntimeError('glfw.init')

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, gl_major)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, gl_minor)
        if use_core_profile:
            # Context profiles are only defined for OpenGL version 3.2 and above
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)

        data = self.setting[SETTING_KEY] if self.setting else None
        state = GlfwAppState.load(
            data) if data else GlfwAppState(width, height)

        self.window: glfw._GLFWwindow = glfw.create_window(
            state.width, state.height, title, None, None)
        if not self.window:
            raise RuntimeError('glfw.create_window')

        w, h = glfw.get_window_size(self.window)
        self.width = w
        self.height = h
        self.is_maximized = False

        # glfw.set_window_size_callback(self.window, self.on_size)
        glfw.set_window_maximize_callback(self.window, self.on_maximized)
        if state.is_maximized:
            glfw.maximize_window(self.window)

        glfw.make_context_current(self.window)
        if use_vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        glfw.set_time(0)
        logging.debug(GL.glGetString(GL.GL_VERSION))
        self.clear_color = (ctypes.c_float * 4)(0.5, 0.5, 0.8, 1)

    def save(self):
        if self.setting:
            # save state
            state = GlfwAppState(self.width, self.height,
                                 self.is_maximized)
            logging.debug(f'save state: {state}')
            self.setting[SETTING_KEY] = state.to_json().encode('utf-8')

    def on_maximized(self, window, maximized):
        self.is_maximized = maximized

    def clear(self) -> bool:

        glfw.swap_buffers(self.window)

        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

        glfw.poll_events()
        if glfw.window_should_close(self.window):
            return False

        self.width, self.height = glfw.get_window_size(self.window)
        width, height = glfw.get_framebuffer_size(self.window)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glViewport(0, 0, width, height)
        GL.glScissor(0, 0, width, height)
        GL.glClearColor(self.clear_color[0] * self.clear_color[3],
                        self.clear_color[1] * self.clear_color[3],
                        self.clear_color[2] * self.clear_color[3],
                        self.clear_color[3])

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        return True

    def get_rect(self) -> Tuple[float, float, float, float]:
        x, y = glfw.get_cursor_pos(self.window)
        w, h = glfw.get_framebuffer_size(self.window)
        return x, y, w, h

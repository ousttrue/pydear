from typing import Tuple
import logging
from OpenGL import GL
import glfw
import nanovg_demo
from pydear import glo


class GlfwApp:
    def __init__(self, w, h, title) -> None:
        glfw.init()
        # Context profiles are only defined for OpenGL version 3.2 and above
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        self.window = glfw.create_window(w, h, title, None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)
        glfw.set_time(0)
        print(glo.get_info())

    def __del__(self):
        glfw.destroy_window(self.window)
        glfw.terminate()

    def begin_frame(self) -> bool:
        if glfw.window_should_close(self.window):
            return False
        return True

    def end_frame(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def get_rect(self) -> Tuple[float, float, float, float]:
        x, y = glfw.get_cursor_pos(self.window)
        w, h = glfw.get_framebuffer_size(self.window)
        return x, y, w, h


def run(app):
    demo = nanovg_demo.Demo()
    prevt = glfw.get_time()
    while app.begin_frame():
        x, y, w, h = app.get_rect()
        ratio = w / float(h)

        t = glfw.get_time()
        dt = t - prevt
        prevt = t

        GL.glViewport(0, 0, w, h)
        GL.glClearColor(0.3, 0.3, 0.32, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        demo.render(x, y, w, h, t)

        app.end_frame()


def main():
    logging.basicConfig(
        level=logging.DEBUG, format='[%(levelname)s]%(name)s %(funcName)s: %(message)s')
    app = GlfwApp(1000, 600, "nanovg: example_gl3.c")
    run(app)


if __name__ == '__main__':
    main()

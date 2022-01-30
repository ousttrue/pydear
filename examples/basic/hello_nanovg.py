from typing import Tuple
from OpenGL import GL
import glfw
import nanovg_demo


class GlfwApp:
    def __init__(self, w, h, title) -> None:
        glfw.init()
        self.window = glfw.create_window(w, h, title, None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)
        glfw.set_time(0)

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


def main():
    app = GlfwApp(1000, 600, "nanovg: example_gl3.c")
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


if __name__ == '__main__':
    main()

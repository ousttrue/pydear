# For local/library development:
# import sys, os
# sys.path.append(os.pardir)
# sys.path.append('../../python-glfw_private')

import ctypes
from OpenGL import GL
import glfw
from pydear import nanovg
from pydear import nanovg_gl
from pydear import glew


def key_callback_fn(window_handle, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window_handle, 1)


def render(vg, x, y, w, h):
    w = float(w)
    h = float(h)
    cornerRadius = 4.0
    s = nanovg.nvgRGBA(255, 255, 255, 16)
    e = nanovg.nvgRGBA(0, 0, 0, 16)
    bg = nanovg.nvgLinearGradient(vg, x, y, x, y+h, s, e)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+1, w-2, h-2, cornerRadius-1)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)


def main():
    glfw.init()

    win = glfw.create_window(1000, 600, "Python NanoVG/GLFW", None, None)
    glfw.make_context_current(win)

    glew.glewInit()
    vg = nanovg_gl.nvgCreateGL3(nanovg_gl.NVGcreateFlags.NVG_ANTIALIAS)
    # nanovg_gl.NVGcreateFlags.NVG_ANTIALIAS)
    # | NVG_STENCIL_STROKES | NVG_DEBUG)
    if not vg:
        raise RuntimeError("Could not init nanovg")

    glfw.set_key_callback(win, key_callback_fn)
    glfw.swap_interval(0)
    glfw.set_time(0)
    prevt = glfw.get_time()

    try:
        while glfw.window_should_close(win) == 0:
            t = glfw.get_time()
            dt = t - prevt
            prevt = t
            # fps.update(dt)

            x, y = glfw.get_cursor_pos(win)
            w, h = glfw.get_framebuffer_size(win)
            ratio = w / float(h)

            GL.glViewport(0, 0, w, h)
            GL.glClearColor(0.3, 0.3, 0.32, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            nanovg.nvgBeginFrame(vg, float(w),
                                 float(h), ratio)
            # data.render(vg, mx.value, my.value, fb_width.value,
            #             fb_height.value, t, False)
            # fps.render(vg, 5, 5)

            render(vg, x, y, w, h)

            nanovg.nvgEndFrame(vg)

            glfw.swap_buffers(win)
            glfw.poll_events()
    finally:
        # data.free(vg)
        nanovg_gl.nvgDeleteGL3_2(vg)
        glfw.destroy_window(win)
        glfw.terminate()


if __name__ == '__main__':
    main()

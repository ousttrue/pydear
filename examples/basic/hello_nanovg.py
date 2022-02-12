import logging
from OpenGL import GL
import glfw
import nanovg_demo
from pydear import nanovg
from pydear.nanovg_backends import nanovg_impl_opengl3
from pydear.utils import glfw_app


def run(app: glfw_app.GlfwApp):
    vg = nanovg.nvgCreate(nanovg.NVGcreateFlags.NVG_ANTIALIAS
                          | nanovg.NVGcreateFlags.NVG_STENCIL_STROKES
                          | nanovg.NVGcreateFlags.NVG_DEBUG)
    if not vg:
        raise RuntimeError("Could not init nanovg")

    nanovg_impl_opengl3.init(vg)

    demo = nanovg_demo.Demo(vg)
    prevt = glfw.get_time()
    while app.clear():
        x, y, w, h = app.get_rect()

        t = glfw.get_time()
        dt = t - prevt
        prevt = t

        GL.glViewport(0, 0, w, h)
        GL.glClearColor(0.3, 0.3, 0.32, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        demo.render(x, y, w, h, t)
        nanovg_impl_opengl3.render(nanovg.nvgGetDrawData(vg))

        # app.end_frame()
    nanovg_impl_opengl3.delete()


def main():
    logging.basicConfig(
        level=logging.DEBUG, format='[%(levelname)s]%(name)s %(funcName)s: %(message)s')

    app = glfw_app.GlfwApp("nanovg: pydear", width=1000, height=600)
    run(app)


if __name__ == '__main__':
    main()

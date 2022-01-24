import logging
import ctypes
from OpenGL import GL
from pydear import glo

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('fbo')

    from pydear import imgui as ImGui
    from pydear.utils import dockspace
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    def show_hello(p_open):
        if ImGui.Begin('hello', p_open):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', clear_color, 0, 1)
            ImGui.ColorPicker4('color', clear_color)
        ImGui.End()

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                ImGui.BeginChild("_image_")
                ImGui.Image(texture, (w, h))
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()

    views = [
        dockspace.Dock('demo', (ctypes.c_bool * 1)
                       (True), ImGui.ShowDemoWindow),
        dockspace.Dock('metrics', (ctypes.c_bool * 1)
                       (True), ImGui.ShowMetricsWindow),
        dockspace.Dock('hello', (ctypes.c_bool * 1)(True), show_hello),
        dockspace.Dock('view', (ctypes.c_bool * 1)(True), show_view),
    ]

    gui = dockspace.DockingGui(app.window, views)

    class Vertex(ctypes.Structure):
        _fields_ = [
            ('x', ctypes.c_float),
            ('y', ctypes.c_float),
            ('r', ctypes.c_float),
            ('g', ctypes.c_float),
            ('b', ctypes.c_float),
        ]
    vertices = (Vertex * 3)(
        Vertex(-0.6, -0.4, 1., 0., 0.),
        Vertex(0.6, -0.4, 0., 1., 0.),
        Vertex(0.,  0.6, 0., 0., 1.)
    )

    vs = '''
#version 110
uniform mat4 MVP;
attribute vec3 vCol;
attribute vec2 vPos;
varying vec3 color;
void main()
{
    gl_Position = MVP * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
'''

    fs = '''
#version 110
varying vec3 color;
void main()
{
    gl_FragColor = vec4(color, 1.0);
}
'''

    shader = glo.Shader.load(vs, fs)

    class Pipeline:
        def __init__(self, shader: glo.Shader) -> None:
            self.shader = shader
            self.MVP = glo.UniformVariable(shader.program, "MVP")
            self.vPos = glo.VertexAttribute(shader.program, "vPos")
            self.vCol = glo.VertexAttribute(shader.program, "vCol")
    pipeline = Pipeline(shader)

    vbo = glo.Vbo()
    vbo.set_vertices(vertices)

    GL.glEnableVertexAttribArray(pipeline.vPos.locatin)
    GL.glVertexAttribPointer(pipeline.vPos.locatin, 2, GL.GL_FLOAT, GL.GL_FALSE,
                             ctypes.sizeof(Vertex), 0)
    GL.glEnableVertexAttribArray(pipeline.vCol.locatin)
    GL.glVertexAttribPointer(pipeline.vCol.locatin, 3, GL.GL_FLOAT, GL.GL_FALSE,
                             ctypes.sizeof(Vertex), ctypes.c_void_p(8))

    while app.clear():
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        gui.render()
    del gui


if __name__ == '__main__':
    main()

import logging
from pydear import imgui as ImGui
from pydear.impl import imnodes as ImNodes
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello')

    def hello():
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin("simple node editor"):

            ImNodes.BeginNodeEditor()
            ImNodes.BeginNode(1)

            ImNodes.BeginNodeTitleBar()
            ImGui.TextUnformatted("simple node :)")
            ImNodes.EndNodeTitleBar()

            ImNodes.BeginInputAttribute(2)
            ImGui.Text("input")
            ImNodes.EndInputAttribute()

            ImNodes.BeginOutputAttribute(3)
            ImGui.Indent(40)
            ImGui.Text("output")
            ImNodes.EndOutputAttribute()

            ImNodes.EndNode()
            ImNodes.EndNodeEditor()

        ImGui.End()

    ImNodes.CreateContext()

    from pydear.utils import gui_app
    gui = gui_app.Gui(app.window, hello)
    while app.clear():
        gui.render()
    ImNodes.DestroyContext()
    del gui


if __name__ == '__main__':
    main()
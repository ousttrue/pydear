from typing import Optional
import logging
import pathlib
import argparse
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.node_editor import NodeEditor, Node, InputPin, OutputPin
from pydear.utils.setting import SettingInterface
logger = logging.getLogger(__name__)


class SampleNodeEditor(NodeEditor):
    def __init__(self, setting: Optional[SettingInterface] = None) -> None:
        super().__init__('sample_node_editor', setting=setting)

    def before_node_editor(self):
        ImGui.TextUnformatted("Right click -- add node")
        ImGui.TextUnformatted("X -- delete selected node")

    def on_node_editor(self):
        open_popup = False
        if (ImGui.IsWindowFocused(ImGui.ImGuiFocusedFlags_.RootAndChildWindows) and
                ImNodes.IsEditorHovered()):
            if ImGui.IsMouseClicked(1):
                open_popup = True

        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (8, 8))
        if not ImGui.IsAnyItemHovered() and open_popup:
            ImGui.OpenPopup("add node")

        if ImGui.BeginPopup("add node"):
            click_pos = ImGui.GetMousePosOnOpeningCurrentPopup()
            if ImGui.MenuItem("add"):
                node = Node('add',
                            [InputPin('a'), InputPin('b')],
                            [OutputPin('value')])
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("multiply"):
                node = Node('mult',
                            [InputPin('a'), InputPin('b')],
                            [OutputPin('value')])
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("output"):
                node = Node('output', [InputPin('value')], [])
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("sine"):
                node = Node('sine', [], [OutputPin('value')])
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("time"):
                node = Node('time', [], [OutputPin('value')])
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.EndPopup()
        ImGui.PopStyleVar()


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', type=pathlib.Path)
    args = parser.parse_args()

    setting = None
    if args.ini:
        from pydear.utils.setting import TomlSetting
        setting = TomlSetting(args.ini)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp(
        'imnodes_util', setting=setting if setting else None)

    node_editor = SampleNodeEditor(setting=setting if setting else None)
    from pydear.utils import dockspace
    docks = [
        dockspace.Dock('', node_editor.show, (ctypes.c_bool * 1)(True))
    ]

    gui = dockspace.DockingGui(
        app.loop, docks=docks, setting=setting if setting else None)
    from pydear.backends import impl_glfw
    impl_glfw = impl_glfw.ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()

    if setting:
        node_editor.save()
        gui.save()
        app.save()
        setting.write()


if __name__ == '__main__':
    main()

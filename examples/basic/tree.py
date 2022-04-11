from typing import Optional
import logging
import asyncio
import pathlib
from pydear import imgui as ImGui
LOGGER = logging.getLogger(__name__)


class State:
    def __init__(self) -> None:
        self.selected: Optional[pathlib.Path] = None


def main():
    logging.basicConfig(level=logging.DEBUG)

    #
    # glfw app
    #
    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello')

    state = State()

    def hello():
        '''
        imgui widgets
        '''

        ImGui.SetNextWindowSize((200, 200), ImGui.ImGuiCond_.Once)
        if ImGui.Begin('hello'):
            flags = (
                ImGui.ImGuiTableFlags_.BordersV
                | ImGui.ImGuiTableFlags_.BordersOuterH
                | ImGui.ImGuiTableFlags_.Resizable
                | ImGui.ImGuiTableFlags_.RowBg
                | ImGui.ImGuiTableFlags_.NoBordersInBody
            )
            header_lablels = ("name", "type", "size")
            if ImGui.BeginTable("jsontree_table", len(header_lablels), flags):
                # header
                for label in header_lablels:
                    ImGui.TableSetupColumn(label)
                ImGui.TableHeadersRow()

                # body
                def traverse(path: pathlib.Path):
                    flag = 0
                    size = '---'
                    file_type = 'file'
                    if path.is_dir():
                        # dir
                        file_type = 'dir'
                    else:
                        # leaf
                        flag |= ImGui.ImGuiTreeNodeFlags_.Leaf
                        flag |= ImGui.ImGuiTreeNodeFlags_.Bullet
                        # flag |= ImGui.TREE_NODE_NO_TREE_PUSH_ON_OPEN
                        size = path.stat().st_size

                    ImGui.TableNextRow()
                    # col 0
                    ImGui.TableNextColumn()
                    open = ImGui.TreeNodeEx(f'{path.name}##{path}', flag)
                    # col 1
                    ImGui.SetItemAllowOverlap()
                    ImGui.TableNextColumn()
                    selected = ImGui.Selectable(
                        f'{file_type}##{path}', path == state.selected, ImGui.ImGuiSelectableFlags_.SpanAllColumns)
                    # if selected:
                    if ImGui.IsItemClicked():
                        state.selected = path
                    # col 2
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{size}')

                    if open:
                        if path.is_dir():
                            for f in path.iterdir():
                                traverse(f)
                        ImGui.TreePop()

                traverse(pathlib.Path(__file__).parent.parent)

                ImGui.EndTable()
        ImGui.End()

    #
    # async coroutine
    #
    async def async_task():
        count = 1
        while True:
            await asyncio.sleep(1)
            LOGGER.debug(f'count: {count}')
            count += 1
    app.loop.create_task(async_task())

    #
    # imgui
    #
    from pydear.utils import gui_app
    gui = gui_app.Gui(app.loop, widgets=hello)

    #
    # glfw_app => ImplGlfwInput => imgui
    #
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)

    #
    # main loop
    #
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()


if __name__ == '__main__':
    main()

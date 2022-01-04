from typing import Callable, List, Iterable
import ctypes
import dataclasses
import pydeer as ImGui
'''
https://gist.github.com/rmitton/f80cbb028fca4495ab1859a155db4cd8
'''


def _dockspace(name: str, toolbar_size=0):
    io = ImGui.GetIO()
    io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable

    flags = (ImGui.ImGuiWindowFlags_.MenuBar
             | ImGui.ImGuiWindowFlags_.NoDocking
             | ImGui.ImGuiWindowFlags_.NoBackground
             | ImGui.ImGuiWindowFlags_.NoTitleBar
             | ImGui.ImGuiWindowFlags_.NoCollapse
             | ImGui.ImGuiWindowFlags_.NoResize
             | ImGui.ImGuiWindowFlags_.NoMove
             | ImGui.ImGuiWindowFlags_.NoBringToFrontOnFocus
             | ImGui.ImGuiWindowFlags_.NoNavFocus
             )

    viewport = ImGui.GetMainViewport()
    x, y = viewport.Pos
    w, h = viewport.Size
    if toolbar_size:
        y += toolbar_size
        h -= toolbar_size

    ImGui.SetNextWindowPos((x, y))
    ImGui.SetNextWindowSize((w, h))
    # imgui.set_next_window_viewport(viewport.id)
    ImGui.PushStyleVar(ImGui.ImGuiStyleVar_.WindowBorderSize, 0.0)
    ImGui.PushStyleVar(ImGui.ImGuiStyleVar_.WindowRounding, 0.0)

    # When using ImGuiDockNodeFlags_PassthruCentralNode, DockSpace() will render our background and handle the pass-thru hole, so we ask Begin() to not render a background.
    # local window_flags = self.window_flags
    # if bit.band(self.dockspace_flags, ) ~= 0 then
    #     window_flags = bit.bor(window_flags, const.ImGuiWindowFlags_.NoBackground)
    # end

    # Important: note that we proceed even if Begin() returns false (aka window is collapsed).
    # This is because we want to keep our DockSpace() active. If a DockSpace() is inactive,
    # all active windows docked into it will lose their parent and become undocked.
    # We cannot preserve the docking relationship between an active window and an inactive docking, otherwise
    # any change of dockspace/settings would lead to windows being stuck in limbo and never being visible.
    ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
    ImGui.Begin(name, None, flags)
    ImGui.PopStyleVar()
    ImGui.PopStyleVar(2)

    # TODO:
    # Save off menu bar height for later.
    # menubar_height = imgui.internal.get_current_window().menu_bar_height()
    menubar_height = 26

    # DockSpace
    dockspace_id = ImGui.GetID(name)
    ImGui.DockSpace(dockspace_id, (0, 0),
                    ImGui.ImGuiDockNodeFlags_.PassthruCentralNode)

    ImGui.End()

    return menubar_height


@dataclasses.dataclass
class DockView:
    name: str
    p_open: ctypes.Array
    drawable: Callable[[ctypes.Array], None]

    def draw(self):
        self.drawable(self.p_open)


TOOLBAR_SIZE = 50


def dockspace(views: Iterable[DockView],
              menu: Callable[[], None] = None,
              toolbar: Callable[[], None] = None,
              ):
    menubar_height = _dockspace(
        '__DOCKING_SPACE__', TOOLBAR_SIZE if toolbar else 0)

    # toolbar
    if toolbar:
        viewport: ImGui.ImGuiViewport = ImGui.GetMainViewport()
        ImGui.SetNextWindowPos(
            (viewport.Pos.x, viewport.Pos.y + menubar_height))
        ImGui.SetNextWindowSize((viewport.Size.x, TOOLBAR_SIZE))
        # imgui.SetNextWindowViewport(viewport -> ID);

        window_flags = (0
                        | ImGui.ImGuiWindowFlags_.NoDocking
                        | ImGui.ImGuiWindowFlags_.NoTitleBar
                        | ImGui.ImGuiWindowFlags_.NoResize
                        | ImGui.ImGuiWindowFlags_.NoMove
                        | ImGui.ImGuiWindowFlags_.NoScrollbar
                        | ImGui.ImGuiWindowFlags_.NoSavedSettings
                        )
        ImGui.PushStyleVar(ImGui.ImGuiStyleVar_.WindowBorderSize, 0)
        ImGui.Begin("TOOLBAR", None, window_flags)
        ImGui.PopStyleVar()

        toolbar()

        ImGui.End()

    if ImGui.BeginMainMenuBar():
        if menu:
            menu()

        if views:
            if ImGui.BeginMenu(b"Views", True):
                for v in views:
                    ImGui.MenuItem_2(v.name, b'', v.p_open)
                ImGui.EndMenu()

        ImGui.EndMainMenuBar()

    if views:
        for v in views:
            if v.p_open[0]:
                v.draw()

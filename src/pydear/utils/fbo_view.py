from typing import Callable, Optional, TypeAlias
import ctypes
from pydear import imgui as ImGui
from .mouse_event import MouseEvent, MouseInput


RenderCallback: TypeAlias = Callable[[MouseInput], None]


class FboView:
    def __init__(self, render: Optional[RenderCallback] = None) -> None:
        self.clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
        from pydear import glo
        self.fbo_manager = glo.FboRenderer()
        self.bg = ImGui.ImVec4(1, 1, 1, 1)
        self.tint = ImGui.ImVec4(1, 1, 1, 1)
        self.mouse_event = MouseEvent()
        self.render = render

    def show_fbo(self, x: int, y: int, w: int, h: int):
        assert w
        assert h
        texture = self.fbo_manager.clear(
            int(w), int(h), self.clear_color)
        if texture:
            ImGui.ImageButton(texture, (w, h), (0, 1),
                              (1, 0), 0, self.bg, self.tint)
            from pydear import imgui_internal
            imgui_internal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,  # type: ignore
                                          ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)

            io = ImGui.GetIO()

            mouse_input = MouseInput(
                (int(io.MousePos.x) - x), (int(io.MousePos.y) - y),
                w, h,
                io.MouseDown[0], io.MouseDown[1], io.MouseDown[2],
                ImGui.IsItemActive(), ImGui.IsItemHovered(), int(io.MouseWheel))
            self.mouse_event.process(mouse_input)

            if self.render:
                self.render(mouse_input)
            else:
                self.mouse_event.debug_draw()

    def show(self, p_open=None):
        if p_open and not p_open[0]:
            return

        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar
                       | ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            x, y = ImGui.GetWindowPos()
            y += ImGui.GetFrameHeight()
            w, h = ImGui.GetContentRegionAvail()
            self.show_fbo(x, y, w, h)

        ImGui.End()
        ImGui.PopStyleVar()

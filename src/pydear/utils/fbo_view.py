from typing import Callable, Optional
import ctypes
from pydear import imgui as ImGui
from .mouseevent import MouseEvent, MouseInput


class FboView:
    def __init__(self, render=Optional[Callable[[], None]]) -> None:
        self.clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
        from pydear import glo
        self.fbo_manager = glo.FboRenderer()
        self.bg = ImGui.ImVec4(1, 1, 1, 1)
        self.tint = ImGui.ImVec4(1, 1, 1, 1)
        self.mouse_event = MouseEvent()
        self.render = render

    def show(self, p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = self.fbo_manager.clear(
                int(w), int(h), self.clear_color)
            if texture:
                ImGui.ImageButton(texture, (w, h), (0, 1),
                                  (1, 0), 0, self.bg, self.tint)
                from pydear import imgui_internal
                imgui_internal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,  # type: ignore
                                              ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)
                io = ImGui.GetIO()
                x, y = ImGui.GetWindowPos()
                y += ImGui.GetFrameHeight()

                self.mouse_event.process(MouseInput(
                    (io.MousePos.x-x), (io.MousePos.y-y),
                    w, h,
                    io.MouseDown[0], io.MouseDown[1], io.MouseDown[2],
                    ImGui.IsItemActive(), ImGui.IsItemHovered(), int(io.MouseWheel)))

                if self.render:
                    self.render()

        ImGui.End()
        ImGui.PopStyleVar()

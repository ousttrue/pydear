from typing import Callable, Optional, TypeAlias
import ctypes
from pydear import imgui as ImGui
from glglue.camera.mouse_event import MouseEvent
from glglue.frame_input import FrameInput


RenderCallback: TypeAlias = Callable[[FrameInput], None]


class FboView:
    def __init__(self, render: Optional[RenderCallback] = None) -> None:
        self.clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
        from glglue import glo

        self.fbo_manager = glo.FboRenderer()
        self.bg = ImGui.ImVec4(1, 1, 1, 1)
        self.tint = ImGui.ImVec4(1, 1, 1, 1)
        self.mouse_event = MouseEvent()
        self.render = render

    def show_fbo(self, x: int, y: int, w: int, h: int):
        assert w
        assert h
        texture = self.fbo_manager.clear(int(w), int(h), self.clear_color)
        if texture:
            ImGui.ImageButton(texture, (w, h), (0, 1), (1, 0), 0, self.bg, self.tint)
            from pydear import imgui_internal

            imgui_internal.ButtonBehavior(
                ImGui.Custom_GetLastItemRect(),
                ImGui.Custom_GetLastItemId(),
                None,
                None,  # type: ignore
                ImGui.ImGuiButtonFlags_.MouseButtonMiddle
                | ImGui.ImGuiButtonFlags_.MouseButtonRight,
            )

            io = ImGui.GetIO()

            mouse_input = FrameInput(
                width=w,
                height=h,
                mouse_x=(int(io.MousePos.x) - x),
                mouse_y=(int(io.MousePos.y) - y),
                mouse_left=io.MouseDown[0],
                mouse_right=io.MouseDown[1],
                mouse_middle=io.MouseDown[2],
                mouse_wheel=int(io.MouseWheel),
                is_active=ImGui.IsItemActive(),
                is_hover=ImGui.IsItemHovered(),
            )
            self.mouse_event.process(mouse_input)

            if self.render:
                self.render(mouse_input)
            else:
                self.mouse_event.debug_draw()

    def show(self, p_open=None):
        if p_open and not p_open[0]:
            return

        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin(
            "render target",
            p_open,
            ImGui.ImGuiWindowFlags_.NoScrollbar
            | ImGui.ImGuiWindowFlags_.NoScrollWithMouse,
        ):
            x, y = ImGui.GetWindowPos()
            y += ImGui.GetFrameHeight()
            w, h = ImGui.GetContentRegionAvail()
            self.show_fbo(x, y, w, h)

        ImGui.End()
        ImGui.PopStyleVar()

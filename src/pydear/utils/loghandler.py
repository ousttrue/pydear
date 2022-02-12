from typing import NamedTuple, List
import logging
import ctypes
from pydear import imgui as ImGui

LOGLEVEL_COLORS = {
    'WARNING': ImGui.ImVec4(1, 1, 0, 1),
    'ERROR': ImGui.ImVec4(1, 0, 0, 1),
    'EXCEPTION': ImGui.ImVec4(1, 0, 1, 1),
    'DEBUG': ImGui.ImVec4(0.5, 0.5, 0.5, 1),
}
DEFAULT_COLOR = ImGui.ImVec4(1, 1, 1, 1)


class Message(NamedTuple):
    level: str
    message: str


class ImGuiLogHandler(logging.Handler):
    '''
    Logger
    '''

    def __init__(self):
        super().__init__()
        self.logs: List[Message] = []
        self.auto_scroll = (ctypes.c_bool * 1)(True)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        self.logs.append(Message(record.levelname, msg))

    def write(self, m):
        pass

    def draw(self, p_open: ctypes.Array):
        if ImGui.Begin('log', p_open):
            # Options menu
            if ImGui.BeginPopup("Options"):
                ImGui.Checkbox("Auto-scroll", self.auto_scroll)
                ImGui.EndPopup()

            # Main window
            if ImGui.Button("Options"):
                ImGui.OpenPopup("Options")
            ImGui.SameLine()
            clear = ImGui.Button("Clear")
            ImGui.SameLine()
            copy = ImGui.Button("Copy")
            # ImGui.SameLine()
            # Filter.Draw("Filter", -100.0f)

            ImGui.Separator()
            ImGui.BeginChild("scrolling", (0, 0), False,
                             ImGui.ImGuiWindowFlags_.HorizontalScrollbar)

            if clear:
                self.logs.clear()
            if copy:
                ImGui.LogToClipboard()

            ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.ItemSpacing, (0, 0))
            # ImGuiListClipper clipper
            # clipper.Begin(LineOffsets.Size)
            # while (clipper.Step())
            for log in self.logs:
                ImGui.TextColored(LOGLEVEL_COLORS.get(
                    log.level, DEFAULT_COLOR), log.message)
            # clipper.End()
            ImGui.PopStyleVar()

            if self.auto_scroll[0] and ImGui.GetScrollY() >= ImGui.GetScrollMaxY():
                ImGui.SetScrollHereY(1.0)

            ImGui.EndChild()
        ImGui.End()

    def register_root(self):
        logging.getLogger().handlers = [self]

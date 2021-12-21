import glfw
import cydeer as ImGui


def compute_fb_scale(window_size: ImGui.ImVec2, frame_buffer_size: ImGui.ImVec2) -> ImGui.ImVec2:
    if window_size.x == 0 or window_size.y == 0:
        return ImGui.ImVec2(1, 1)

    return ImGui.ImVec2(
        frame_buffer_size.x / window_size.x,
        frame_buffer_size.y / window_size.y
    )


class GlfwRenderer:
    def __init__(self, window, attach_callbacks=True):
        if not ImGui.GetCurrentContext():
            raise RuntimeError(
                "No valid ImGui context. Use imgui.create_context() first and/or "
                "imgui.set_current_context()."
            )
        self.io = ImGui.GetIO()
        self.io.DeltaTime = 1.0 / 60.0

        self.window = window

        if attach_callbacks:
            glfw.set_key_callback(self.window, self.keyboard_callback)
            glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
            glfw.set_window_size_callback(self.window, self.resize_callback)
            glfw.set_char_callback(self.window, self.char_callback)
            glfw.set_scroll_callback(self.window, self.scroll_callback)

        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self.io.get_clipboard_text_fn = self._get_clipboard_text
        self.io.set_clipboard_text_fn = self._set_clipboard_text

        self._map_keys()
        self._gui_time = None

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def _map_keys(self):
        key_map = self.io.KeyMap
        key_map[ImGui.ImGuiKey_.Tab] = glfw.KEY_TAB
        key_map[ImGui.ImGuiKey_.LeftArrow] = glfw.KEY_LEFT
        key_map[ImGui.ImGuiKey_.RightArrow] = glfw.KEY_RIGHT
        key_map[ImGui.ImGuiKey_.UpArrow] = glfw.KEY_UP
        key_map[ImGui.ImGuiKey_.DownArrow] = glfw.KEY_DOWN
        key_map[ImGui.ImGuiKey_.PageUp] = glfw.KEY_PAGE_UP
        key_map[ImGui.ImGuiKey_.PageDown] = glfw.KEY_PAGE_DOWN
        key_map[ImGui.ImGuiKey_.Home] = glfw.KEY_HOME
        key_map[ImGui.ImGuiKey_.End] = glfw.KEY_END
        key_map[ImGui.ImGuiKey_.Insert] = glfw.KEY_INSERT
        key_map[ImGui.ImGuiKey_.Delete] = glfw.KEY_DELETE
        key_map[ImGui.ImGuiKey_.Backspace] = glfw.KEY_BACKSPACE
        key_map[ImGui.ImGuiKey_.Space] = glfw.KEY_SPACE
        key_map[ImGui.ImGuiKey_.Enter] = glfw.KEY_ENTER
        key_map[ImGui.ImGuiKey_.Escape] = glfw.KEY_ESCAPE
        key_map[ImGui.ImGuiKey_.KeyPadEnter] = glfw.KEY_KP_ENTER
        key_map[ImGui.ImGuiKey_.A] = glfw.KEY_A
        key_map[ImGui.ImGuiKey_.C] = glfw.KEY_C
        key_map[ImGui.ImGuiKey_.V] = glfw.KEY_V
        key_map[ImGui.ImGuiKey_.X] = glfw.KEY_X
        key_map[ImGui.ImGuiKey_.Y] = glfw.KEY_Y
        key_map[ImGui.ImGuiKey_.Z] = glfw.KEY_Z

    def keyboard_callback(self, window, key, scancode, action, mods):
        io = self.io

        if action == glfw.PRESS:
            io.KeysDown[key] = True
        elif action == glfw.RELEASE:
            io.KeysDown[key] = False

        io.KeyCtrl = (
            io.KeysDown[glfw.KEY_LEFT_CONTROL] or
            io.KeysDown[glfw.KEY_RIGHT_CONTROL]
        )

        io.KeyAlt = (
            io.KeysDown[glfw.KEY_LEFT_ALT] or
            io.KeysDown[glfw.KEY_RIGHT_ALT]
        )

        io.KeyShift = (
            io.KeysDown[glfw.KEY_LEFT_SHIFT] or
            io.KeysDown[glfw.KEY_RIGHT_SHIFT]
        )

        io.KeySuper = (
            io.KeysDown[glfw.KEY_LEFT_SUPER] or
            io.KeysDown[glfw.KEY_RIGHT_SUPER]
        )

    def char_callback(self, window, char):
        pass
        # if 0 < char < 0x10000:
        #     self.io.add_input_character(char)

    def resize_callback(self, window, width, height):
        self.io.DisplaySize = ImGui.ImVec2(width, height)

    def mouse_callback(self, *args, **kwargs):
        pass

    def scroll_callback(self, window, x_offset, y_offset):
        self.io.MouseWheelH = x_offset
        self.io.MouseWheel = y_offset

    def process_inputs(self):
        window_size = ImGui.ImVec2(*glfw.get_window_size(self.window))
        fb_size = ImGui.ImVec2(*glfw.get_framebuffer_size(self.window))

        io = self.io
        io.DisplaySize = window_size
        io.DisplayFramebufferScale = compute_fb_scale(window_size, fb_size)
        io.DeltaTime = 1.0/60

        x = -1
        y = -1
        if glfw.get_window_attrib(self.window, glfw.FOCUSED):
            x, y = glfw.get_cursor_pos(self.window)
        io.MousePos.x = x
        io.MousePos.y = y
        io.MouseDown[0] = glfw.get_mouse_button(self.window, 0)
        io.MouseDown[1] = glfw.get_mouse_button(self.window, 1)
        io.MouseDown[2] = glfw.get_mouse_button(self.window, 2)

        current_time = glfw.get_time()

        if self._gui_time:
            self.io.DeltaTime = current_time - self._gui_time
        else:
            self.io.DeltaTime = 1. / 60.
        if(io.DeltaTime <= 0.0):
            io.DeltaTime = 1. / 1000.

        self._gui_time = current_time

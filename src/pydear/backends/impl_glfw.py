import glfw
from pydear import imgui as ImGui


def compute_fb_scale(window_size: ImGui.ImVec2, frame_buffer_size: ImGui.ImVec2) -> ImGui.ImVec2:
    if window_size.x == 0 or window_size.y == 0:
        return ImGui.ImVec2(1, 1)

    return ImGui.ImVec2(
        frame_buffer_size.x / window_size.x,
        frame_buffer_size.y / window_size.y
    )


GLFW_TO_IMGUI = {
    glfw.KEY_TAB: ImGui.ImGuiKey_.Tab,
    glfw.KEY_LEFT: ImGui.ImGuiKey_.LeftArrow,
    glfw.KEY_RIGHT: ImGui.ImGuiKey_.RightArrow,
    glfw.KEY_UP: ImGui.ImGuiKey_.UpArrow,
    glfw.KEY_DOWN: ImGui.ImGuiKey_.DownArrow,
    glfw.KEY_PAGE_UP: ImGui.ImGuiKey_.PageUp,
    glfw.KEY_PAGE_DOWN: ImGui.ImGuiKey_.PageDown,
    glfw.KEY_HOME: ImGui.ImGuiKey_.Home,
    glfw.KEY_END: ImGui.ImGuiKey_.End,
    glfw.KEY_INSERT: ImGui.ImGuiKey_.Insert,
    glfw.KEY_DELETE: ImGui.ImGuiKey_.Delete,
    glfw.KEY_BACKSPACE: ImGui.ImGuiKey_.Backspace,
    glfw.KEY_SPACE: ImGui.ImGuiKey_.Space,
    glfw.KEY_ENTER: ImGui.ImGuiKey_.Enter,
    glfw.KEY_ESCAPE: ImGui.ImGuiKey_.Escape,
    glfw.KEY_APOSTROPHE: ImGui.ImGuiKey_.Apostrophe,
    glfw.KEY_COMMA: ImGui.ImGuiKey_.Comma,
    glfw.KEY_MINUS: ImGui.ImGuiKey_.Minus,
    glfw.KEY_PERIOD: ImGui.ImGuiKey_.Period,
    glfw.KEY_SLASH: ImGui.ImGuiKey_.Slash,
    glfw.KEY_SEMICOLON: ImGui.ImGuiKey_.Semicolon,
    glfw.KEY_EQUAL: ImGui.ImGuiKey_.Equal,
    glfw.KEY_LEFT_BRACKET: ImGui.ImGuiKey_.LeftBracket,
    glfw.KEY_BACKSLASH: ImGui.ImGuiKey_.Backslash,
    glfw.KEY_RIGHT_BRACKET: ImGui.ImGuiKey_.RightBracket,
    glfw.KEY_GRAVE_ACCENT: ImGui.ImGuiKey_.GraveAccent,
    glfw.KEY_CAPS_LOCK: ImGui.ImGuiKey_.CapsLock,
    glfw.KEY_SCROLL_LOCK: ImGui.ImGuiKey_.ScrollLock,
    glfw.KEY_NUM_LOCK: ImGui.ImGuiKey_.NumLock,
    glfw.KEY_PRINT_SCREEN: ImGui.ImGuiKey_.PrintScreen,
    glfw.KEY_PAUSE: ImGui.ImGuiKey_.Pause,
    glfw.KEY_KP_0: ImGui.ImGuiKey_.Keypad0,
    glfw.KEY_KP_1: ImGui.ImGuiKey_.Keypad1,
    glfw.KEY_KP_2: ImGui.ImGuiKey_.Keypad2,
    glfw.KEY_KP_3: ImGui.ImGuiKey_.Keypad3,
    glfw.KEY_KP_4: ImGui.ImGuiKey_.Keypad4,
    glfw.KEY_KP_5: ImGui.ImGuiKey_.Keypad5,
    glfw.KEY_KP_6: ImGui.ImGuiKey_.Keypad6,
    glfw.KEY_KP_7: ImGui.ImGuiKey_.Keypad7,
    glfw.KEY_KP_8: ImGui.ImGuiKey_.Keypad8,
    glfw.KEY_KP_9: ImGui.ImGuiKey_.Keypad9,
    glfw.KEY_KP_DECIMAL: ImGui.ImGuiKey_.KeypadDecimal,
    glfw.KEY_KP_DIVIDE: ImGui.ImGuiKey_.KeypadDivide,
    glfw.KEY_KP_MULTIPLY: ImGui.ImGuiKey_.KeypadMultiply,
    glfw.KEY_KP_SUBTRACT: ImGui.ImGuiKey_.KeypadSubtract,
    glfw.KEY_KP_ADD: ImGui.ImGuiKey_.KeypadAdd,
    glfw.KEY_KP_ENTER: ImGui.ImGuiKey_.KeypadEnter,
    glfw.KEY_KP_EQUAL: ImGui.ImGuiKey_.KeypadEqual,
    glfw.KEY_LEFT_SHIFT: ImGui.ImGuiKey_.LeftShift,
    glfw.KEY_LEFT_CONTROL: ImGui.ImGuiKey_.LeftCtrl,
    glfw.KEY_LEFT_ALT: ImGui.ImGuiKey_.LeftAlt,
    glfw.KEY_LEFT_SUPER: ImGui.ImGuiKey_.LeftSuper,
    glfw.KEY_RIGHT_SHIFT: ImGui.ImGuiKey_.RightShift,
    glfw.KEY_RIGHT_CONTROL: ImGui.ImGuiKey_.RightCtrl,
    glfw.KEY_RIGHT_ALT: ImGui.ImGuiKey_.RightAlt,
    glfw.KEY_RIGHT_SUPER: ImGui.ImGuiKey_.RightSuper,
    glfw.KEY_MENU: ImGui.ImGuiKey_.Menu,
    glfw.KEY_0: ImGui.ImGuiKey_._0,
    glfw.KEY_1: ImGui.ImGuiKey_._1,
    glfw.KEY_2: ImGui.ImGuiKey_._2,
    glfw.KEY_3: ImGui.ImGuiKey_._3,
    glfw.KEY_4: ImGui.ImGuiKey_._4,
    glfw.KEY_5: ImGui.ImGuiKey_._5,
    glfw.KEY_6: ImGui.ImGuiKey_._6,
    glfw.KEY_7: ImGui.ImGuiKey_._7,
    glfw.KEY_8: ImGui.ImGuiKey_._8,
    glfw.KEY_9: ImGui.ImGuiKey_._9,
    glfw.KEY_A: ImGui.ImGuiKey_.A,
    glfw.KEY_B: ImGui.ImGuiKey_.B,
    glfw.KEY_C: ImGui.ImGuiKey_.C,
    glfw.KEY_D: ImGui.ImGuiKey_.D,
    glfw.KEY_E: ImGui.ImGuiKey_.E,
    glfw.KEY_F: ImGui.ImGuiKey_.F,
    glfw.KEY_G: ImGui.ImGuiKey_.G,
    glfw.KEY_H: ImGui.ImGuiKey_.H,
    glfw.KEY_I: ImGui.ImGuiKey_.I,
    glfw.KEY_J: ImGui.ImGuiKey_.J,
    glfw.KEY_K: ImGui.ImGuiKey_.K,
    glfw.KEY_L: ImGui.ImGuiKey_.L,
    glfw.KEY_M: ImGui.ImGuiKey_.M,
    glfw.KEY_N: ImGui.ImGuiKey_.N,
    glfw.KEY_O: ImGui.ImGuiKey_.O,
    glfw.KEY_P: ImGui.ImGuiKey_.P,
    glfw.KEY_Q: ImGui.ImGuiKey_.Q,
    glfw.KEY_R: ImGui.ImGuiKey_.R,
    glfw.KEY_S: ImGui.ImGuiKey_.S,
    glfw.KEY_T: ImGui.ImGuiKey_.T,
    glfw.KEY_U: ImGui.ImGuiKey_.U,
    glfw.KEY_V: ImGui.ImGuiKey_.V,
    glfw.KEY_W: ImGui.ImGuiKey_.W,
    glfw.KEY_X: ImGui.ImGuiKey_.X,
    glfw.KEY_Y: ImGui.ImGuiKey_.Y,
    glfw.KEY_Z: ImGui.ImGuiKey_.Z,
    glfw.KEY_F1: ImGui.ImGuiKey_.F1,
    glfw.KEY_F2: ImGui.ImGuiKey_.F2,
    glfw.KEY_F3: ImGui.ImGuiKey_.F3,
    glfw.KEY_F4: ImGui.ImGuiKey_.F4,
    glfw.KEY_F5: ImGui.ImGuiKey_.F5,
    glfw.KEY_F6: ImGui.ImGuiKey_.F6,
    glfw.KEY_F7: ImGui.ImGuiKey_.F7,
    glfw.KEY_F8: ImGui.ImGuiKey_.F8,
    glfw.KEY_F9: ImGui.ImGuiKey_.F9,
    glfw.KEY_F10: ImGui.ImGuiKey_.F10,
    glfw.KEY_F11: ImGui.ImGuiKey_.F11,
    glfw.KEY_F12: ImGui.ImGuiKey_.F12,
}


class ImplGlfwInput:
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
            glfw.set_key_callback(self.window, self._keyboard_callback)
            glfw.set_mouse_button_callback(
                self.window, self._mouse_button_callback)
            glfw.set_cursor_pos_callback(
                self.window, self._mouse_position_callback)
            glfw.set_window_size_callback(self.window, self._resize_callback)
            glfw.set_char_callback(self.window, self._char_callback)
            glfw.set_scroll_callback(self.window, self._scroll_callback)

        self.io.display_size = glfw.get_framebuffer_size(self.window)
        self.io.get_clipboard_text_fn = self._get_clipboard_text
        self.io.set_clipboard_text_fn = self._set_clipboard_text

        self._gui_time = None

    def _get_clipboard_text(self):
        return glfw.get_clipboard_string(self.window)

    def _set_clipboard_text(self, text):
        glfw.set_clipboard_string(self.window, text)

    def _keyboard_callback(self, window, key, scancode, action, mods):
        imgui_key = GLFW_TO_IMGUI.get(key)
        if imgui_key is not None:
            self.io.AddKeyEvent(imgui_key.value, action == glfw.PRESS)

    def _char_callback(self, window, char):
        if 0 < char < 0x10000:
            self.io.AddInputCharacter(char)

    def _resize_callback(self, window, width, height):
        self.io.DisplaySize = ImGui.ImVec2(width, height)

    def _mouse_button_callback(self, window, button, action, mods):
        self.io.AddMouseButtonEvent(button, action == glfw.PRESS)

    def _mouse_position_callback(self,  window, x, y):
        self.io.AddMousePosEvent(x, y)

    def _scroll_callback(self, window, x_offset, y_offset):
        self.io.AddMouseWheelEvent(x_offset, y_offset)

    def process_inputs(self):
        window_size = ImGui.ImVec2(*glfw.get_window_size(self.window))
        fb_size = ImGui.ImVec2(*glfw.get_framebuffer_size(self.window))

        io = self.io
        io.DisplaySize = window_size
        io.DisplayFramebufferScale = compute_fb_scale(window_size, fb_size)
        io.DeltaTime = 1.0/60

        current_time = glfw.get_time()

        if self._gui_time:
            self.io.DeltaTime = current_time - self._gui_time
        else:
            self.io.DeltaTime = 1. / 60.
        if(io.DeltaTime <= 0.0):
            io.DeltaTime = 1. / 1000.

        self._gui_time = current_time

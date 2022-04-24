import logging
import pathlib
import ctypes
import glfw
from OpenGL import GL
from pydear import imgui as ImGui
from pydear.utils import filedialog


logger = logging.getLogger(__name__)
print(ctypes.sizeof(ImGui.ImGuiIO))

# Dear ImGui: standalone example application for GLFW + OpenGL 3, using programmable pipeline
# (GLFW is a cross-platform general purpose library for handling windows, inputs, OpenGL/Vulkan/Metal graphics context creation, etc.)
# If you are new to Dear ImGui, read documentation from the docs/ folder + read the top of ImGui.cpp.
# Read online: https://github.com/ocornut/imgui/tree/master/docs


def color_32(r, g, b, a):
    return r + (g << 8) + (b << 16) + (a << 24)


def glfw_error_callback(error: int, description: str):
    logger.error(f"Glfw Error {error}: {description}")


def main():
    logging.basicConfig(level=logging.DEBUG)
    # Setup window
    glfw.set_error_callback(glfw_error_callback)
    if not glfw.init():
        logger.error('fail to glfw.init')
        return

    # GL 3.0 + GLSL 130
    # glsl_version = "#version 130"
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE,
                     glfw.OPENGL_CORE_PROFILE)  # 3.2+ only

    # Create window with graphics context
    window = glfw.create_window(
        1280, 720, "pydear GLFW+OpenGL3 example", None, None)
    if not window:
        logger.error('fail to glfw.create_window')
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)  # Enable vsync

    # Setup Dear ImGui context
    # IMGUI_CHECKVERSION()
    ImGui.CreateContext()
    io = ImGui.GetIO()
    # create texture before: ImGui.NewFrame()
    # io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;     // Enable Keyboard Controls
    # io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls
    io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable  # before load ini

    # Setup Dear ImGui style
    # ImGui.StyleColorsDark()
    # ImGui.StyleColorsClassic();

    font_size = 20.0

    from pydear.utils import fontloader
    fontloader.load(pathlib.Path("C:/Windows/Fonts/MSGothic.ttc"), font_size,
                    io.Fonts.GetGlyphRangesJapanese())

    import fontawesome47
    icons_ranges = (ctypes.c_ushort * 3)(0xf000, 0xf3ff, 0)
    fontloader.load(fontawesome47.get_path(), font_size, icons_ranges,
                    merge=True, monospace=True)

    io.Fonts.Build()

    # Setup Platform/Renderer backends
    # ImGui_ImplGlfw_InitForOpenGL(window, True)
    # ImGui_ImplOpenGL3_Init(glsl_version)
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(window)
    from pydear.backends.impl_opengl3 import Renderer
    impl_opengl = Renderer()

    # Our state
    clear_color = (ctypes.c_float * 4)(0.45, 0.55, 0.60, 1.00)

    # Main loop
    counter = [0]
    f = (ctypes.c_float * 1)(0.0)

    from pydear.utils.dockspace import show_docks, Dock
    show_another_window = (ctypes.c_bool * 1)(True)
    show_demo_window = (ctypes.c_bool * 1)(True)

    # 1. Show the big demo window (Most of the sample code is in ImGui.ShowDemoWindow()! You can browse its code to learn more about Dear ImGui!).
    demo = Dock('demo', ImGui.ShowDemoWindow, show_demo_window)

    # 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
    def draw_hello(p_open: ctypes.Array):
        if ImGui.Begin(b"Hello, world!", p_open):
            # Create a window called "Hello, world!" and append into it.

            ImGui.TextUnformatted(b"This is some useful text.")
            # Display some text(you can use a format strings too)
            # Edit bools storing our window open/close state
            ImGui.Checkbox(b"Demo Window", show_demo_window)
            ImGui.Checkbox(b"Another Window", show_another_window)

            # Edit 1 float using a slider from 0.0f to 1.0f
            ImGui.SliderFloat(b"float", f, 0.0, 1.0)
            # Edit 3 floats representing a color
            ImGui.ColorEdit3(b"clear color", clear_color)

            # Buttons return true when clicked (most widgets return true when edited/activated)
            if ImGui.Button(b"Button"):
                counter[0] += 1
            ImGui.SameLine()
            ImGui.PushStyleColor(
                ImGui.ImGuiCol_.Text, color_32(255, 0, 0, 255))
            ImGui.Text(f"counter = {counter[0]}".encode('utf-8'))
            ImGui.PopStyleColor()

            ImGui.Text(
                f"Application average {1000.0 / ImGui.GetIO().Framerate:.3f} ms/frame ({ImGui.GetIO().Framerate:.1f} FPS)".encode('utf-8'))

        ImGui.End()
    window2 = Dock('hello', draw_hello, (ctypes.c_bool * 1)(True))

    # 3. Show another simple window.
    def draw_another_window(p_open: ctypes.Array):
        if ImGui.Begin("Another Window", p_open):
            # Pass a pointer to our bool variable(the window will have a closing button that will clear the bool when clicked)
            ImGui.Text("Hello from another window!")
            if ImGui.Button("Close Me"):
                p_open[0] = False

            if ImGui.Button("debug"):
                logger.debug("DEBUG")
            ImGui.SameLine()
            if ImGui.Button("info"):
                logger.info("INFO")
            ImGui.SameLine()
            if ImGui.Button("warning"):
                logger.warning("WARNING")
            ImGui.SameLine()
            if ImGui.Button("error"):
                logger.error("error")
            ImGui.SameLine()
            if ImGui.Button("exception"):
                logger.exception("exception")

        ImGui.End()
    another_window = Dock(
        'another_window', draw_another_window, show_another_window)

    # 4.
    metrics = Dock('metrics', ImGui.ShowMetricsWindow,
                   (ctypes.c_bool * 1)(True))

    # 5.
    from pydear.utils.loghandler import ImGuiLogHandler
    log_handler = ImGuiLogHandler()
    log_handler.setFormatter(logging.Formatter(
        '%(name)s:%(lineno)s[%(levelname)s]%(message)s'))
    log_handler.register_root()
    log = Dock('log', log_handler.show, (ctypes.c_bool * 1)(True))

    views = [
        demo, another_window, window2, metrics, log
    ]

    FILEDIALOG = 'FileOpen'

    def menu():
        if ImGui.BeginMenu(b"File", True):
            filedialog.open(FILEDIALOG)

            if ImGui.MenuItem(b"Quit", None, False, True):
                glfw.set_window_should_close(window, True)
            ImGui.EndMenu()

    def toolbar():
        import fontawesome47.icons_str as ICON_FA
        if ImGui.Button(ICON_FA.SERVER):
            print('0')

        ImGui.SameLine()
        if ImGui.Button(ICON_FA.SLIDERS):
            print('1')

        ImGui.SameLine()
        if ImGui.Button(ICON_FA.YELP):
            print('2')

        ImGui.SameLine()
        if ImGui.Button(ICON_FA.AMBULANCE):
            print('3')

        ImGui.SameLine()
        if ImGui.Button(ICON_FA.BUILDING_O):
            print('4')

    while not glfw.window_should_close(window):
        # Poll and handle events (inputs, window resize, etc.)
        # You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
        # - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application.
        # - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main application.
        # Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
        glfw.poll_events()
        impl_glfw.process_inputs()

        # update ImGui
        ImGui.NewFrame()
        show_docks(views, menu=menu, toolbar=toolbar)

        # file = filedialog.fileopendialog()
        # if file:
        #     logger.info(f'open {file}')
        # file dialogs
        result = filedialog.modal(FILEDIALOG)
        if result:
            logger.info(f'file open: {result}')

        ImGui.Render()

        # clear OpenGL
        display_w, display_h = glfw.get_framebuffer_size(window)
        GL.glViewport(0, 0, display_w, display_h)
        GL.glScissor(0, 0, display_w, display_h)
        GL.glClearColor(clear_color[0] * clear_color[3],
                        clear_color[1] * clear_color[3],
                        clear_color[2] * clear_color[3],
                        clear_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # render ImGui
        impl_opengl.render(ImGui.GetDrawData())
        glfw.swap_buffers(window)

    # Cleanup

    del impl_opengl
    del impl_glfw
    ImGui.DestroyContext()

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main()

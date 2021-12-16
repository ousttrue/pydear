import logging
import glfw
from OpenGL import GL
import cydeer as ImGui
import ctypes

logger = logging.getLogger(__name__)

# Dear ImGui: standalone example application for GLFW + OpenGL 3, using programmable pipeline
# (GLFW is a cross-platform general purpose library for handling windows, inputs, OpenGL/Vulkan/Metal graphics context creation, etc.)
# If you are new to Dear ImGui, read documentation from the docs/ folder + read the top of imgui.cpp.
# Read online: https://github.com/ocornut/imgui/tree/master/docs


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
    glsl_version = "#version 130"
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE,
                     glfw.OPENGL_CORE_PROFILE)  # 3.2+ only

    # Create window with graphics context
    window = glfw.create_window(
        1280, 720, "CyDeer GLFW+OpenGL3 example", None, None)
    if not window:
        logger.error('fail to glfw.create_window')
        return

    glfw.make_context_current(window)
    glfw.swap_interval(1)  # Enable vsync

    # Setup Dear ImGui context
    # IMGUI_CHECKVERSION()
    ImGui.CreateContext()
    io = ImGui.GetIO()
    # io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;     // Enable Keyboard Controls
    # io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls
    io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable

    # Setup Dear ImGui style
    ImGui.StyleColorsDark()
    # ImGui.StyleColorsClassic();

    # Setup Platform/Renderer backends
    # ImGui_ImplGlfw_InitForOpenGL(window, True)
    # ImGui_ImplOpenGL3_Init(glsl_version)
    from pyimgui_backend.glfw import GlfwRenderer
    impl_glfw = GlfwRenderer(window)
    from pyimgui_backend.opengl import Renderer
    impl_opengl = Renderer()

#     // Load Fonts
#     // - If no fonts are loaded, dear imgui will use the default font. You can also load multiple fonts and use ImGui.PushFont()/PopFont() to select them.
#     // - AddFontFromFileTTF() will return the ImFont* so you can store it if you need to select the font among multiple.
#     // - If the file cannot be loaded, the function will return NULL. Please handle those errors in your application (e.g. use an assertion, or display an error and quit).
#     // - The fonts will be rasterized at a given size (w/ oversampling) and stored into a texture when calling ImFontAtlas::Build()/GetTexDataAsXXXX(), which ImGui_ImplXXXX_NewFrame below will call.
#     // - Read 'docs/FONTS.md' for more instructions and details.
#     // - Remember that in C/C++ if you want to include a backslash \ in a string literal you need to write a double backslash \\ !
#     //io.Fonts->AddFontDefault();
#     //io.Fonts->AddFontFromFileTTF("../../misc/fonts/Roboto-Medium.ttf", 16.0f);
#     //io.Fonts->AddFontFromFileTTF("../../misc/fonts/Cousine-Regular.ttf", 15.0f);
#     //io.Fonts->AddFontFromFileTTF("../../misc/fonts/DroidSans.ttf", 16.0f);
#     //io.Fonts->AddFontFromFileTTF("../../misc/fonts/ProggyTiny.ttf", 10.0f);
#     //ImFont* font = io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\ArialUni.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesJapanese());
#     //IM_ASSERT(font != NULL);

    # Our state
    show_demo_window = (ctypes.c_bool * 1)(True)
    show_another_window = (ctypes.c_bool * 1)(True)
    clear_color = (ctypes.c_float * 4)(0.45, 0.55, 0.60, 1.00)

    # Main loop
    counter = [0]
    f = (ctypes.c_float * 1)(0.0)
    while not glfw.window_should_close(window):
        # Poll and handle events (inputs, window resize, etc.)
        # You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
        # - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application.
        # - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main application.
        # Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
        glfw.poll_events()
        impl_glfw.process_inputs()

        # Start the Dear ImGui frame
        ImGui.NewFrame()

        # 1. Show the big demo window (Most of the sample code is in ImGui.ShowDemoWindow()! You can browse its code to learn more about Dear ImGui!).
        if show_demo_window[0]:
            ImGui.ShowDemoWindow(show_demo_window)

        # 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
        def window2():
            ImGui.Begin(b"Hello, world!")
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
            ImGui.Text(f"counter = {counter[0]}".encode('utf-8'))

            ImGui.Text(
                f"Application average {1000.0 / ImGui.GetIO().Framerate:.3f} ms/frame ({ImGui.GetIO().Framerate:.1f} FPS)".encode('utf-8'))
            ImGui.End()
        window2()

        # 3. Show another simple window.
        if show_another_window[0]:
            ImGui.Begin("Another Window", show_another_window)
            # Pass a pointer to our bool variable(the window will have a closing button that will clear the bool when clicked)
            ImGui.Text("Hello from another window!")
            if ImGui.Button("Close Me"):
                show_another_window[0] = False
            ImGui.End()

        ImGui.ShowMetricsWindow()

        # Rendering
        ImGui.Render()

        display_w, display_h = glfw.get_framebuffer_size(window)
        GL.glViewport(0, 0, display_w, display_h)
        GL.glScissor(0, 0, display_w, display_h)

        GL.glClearColor(clear_color[0] * clear_color[3],
                        clear_color[1] * clear_color[3],
                        clear_color[2] * clear_color[3],
                        clear_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

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

import logging
import glfw
from OpenGL import GL
import cydeer.imgui as ImGui

logger = logging.getLogger(__name__)

# // Dear ImGui: standalone example application for GLFW + OpenGL 3, using programmable pipeline
# // (GLFW is a cross-platform general purpose library for handling windows, inputs, OpenGL/Vulkan/Metal graphics context creation, etc.)
# // If you are new to Dear ImGui, read documentation from the docs/ folder + read the top of imgui.cpp.
# // Read online: https://github.com/ocornut/imgui/tree/master/docs

# #include "imgui.h"
# #include "imgui_impl_glfw.h"
# #include "imgui_impl_opengl3.h"
# #include <stdio.h>
# #if defined(IMGUI_IMPL_OPENGL_ES2)
# #include <GLES2/gl2.h>
# #endif
# #include <GLFW/glfw3.h> // Will drag system OpenGL headers

# // [Win32] Our example includes a copy of glfw3.lib pre-compiled with VS2010 to maximize ease of testing and compatibility with old VS compilers.
# // To link with VS2010-era libraries, VS2015+ requires linking with legacy_stdio_definitions.lib, which we do using this pragma.
# // Your own project should not be affected, as you are likely to link with a newer binary of GLFW that is adequate for your version of Visual Studio.
# #if defined(_MSC_VER) && (_MSC_VER >= 1900) && !defined(IMGUI_DISABLE_WIN32_FUNCTIONS)
# #pragma comment(lib, "legacy_stdio_definitions")
# #endif


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
    ImGui.CreateContext(None)
    io = ImGui.GetIO()
    #io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;     // Enable Keyboard Controls
    #io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls

    # Setup Dear ImGui style
    ImGui.StyleColorsDark(None)
    #ImGui.StyleColorsClassic();

    # Setup Platform/Renderer backends
    # ImGui_ImplGlfw_InitForOpenGL(window, True)
    # ImGui_ImplOpenGL3_Init(glsl_version)
    from pyimgui_backend.glfw import GlfwRenderer
    impl = GlfwRenderer(window)

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

#     // Our state
#     bool show_demo_window = true;
#     bool show_another_window = false;
    clear_color = (0.45, 0.55, 0.60, 1.00)

    # Main loop
    while not glfw.window_should_close(window):
        # Poll and handle events (inputs, window resize, etc.)
        # You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
        # - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application.
        # - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main application.
        # Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
        glfw.poll_events()
        impl.process_inputs()

#         // Start the Dear ImGui frame
#         ImGui_ImplOpenGL3_NewFrame();
#         ImGui_ImplGlfw_NewFrame();
#         ImGui.NewFrame();

#         // 1. Show the big demo window (Most of the sample code is in ImGui.ShowDemoWindow()! You can browse its code to learn more about Dear ImGui!).
#         if (show_demo_window)
#             ImGui.ShowDemoWindow(&show_demo_window);

#         // 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
#         {
#             static float f = 0.0f;
#             static int counter = 0;

#             ImGui.Begin("Hello, world!");                          // Create a window called "Hello, world!" and append into it.

#             ImGui.Text("This is some useful text.");               // Display some text (you can use a format strings too)
#             ImGui.Checkbox("Demo Window", &show_demo_window);      // Edit bools storing our window open/close state
#             ImGui.Checkbox("Another Window", &show_another_window);

#             ImGui.SliderFloat("float", &f, 0.0f, 1.0f);            // Edit 1 float using a slider from 0.0f to 1.0f
#             ImGui.ColorEdit3("clear color", (float*)&clear_color); // Edit 3 floats representing a color

#             if (ImGui.Button("Button"))                            // Buttons return true when clicked (most widgets return true when edited/activated)
#                 counter++;
#             ImGui.SameLine();
#             ImGui.Text("counter = %d", counter);

#             ImGui.Text("Application average %.3f ms/frame (%.1f FPS)", 1000.0f / ImGui.GetIO().Framerate, ImGui.GetIO().Framerate);
#             ImGui.End();
#         }

#         // 3. Show another simple window.
#         if (show_another_window)
#         {
#             ImGui.Begin("Another Window", &show_another_window);   // Pass a pointer to our bool variable (the window will have a closing button that will clear the bool when clicked)
#             ImGui.Text("Hello from another window!");
#             if (ImGui.Button("Close Me"))
#                 show_another_window = false;
#             ImGui.End();
#         }

#         // Rendering
#         ImGui.Render();
#         int display_w, display_h;
        display_w, display_h = glfw.get_framebuffer_size(window)
        GL.glViewport(0, 0, display_w, display_h)
        GL.glClearColor(clear_color[0] * clear_color[3],
                        clear_color[1] * clear_color[3],
                        clear_color[2] * clear_color[3],
                        clear_color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
#         ImGui_ImplOpenGL3_RenderDrawData(ImGui.GetDrawData());

        glfw.swap_buffers(window)
#     }

#     // Cleanup
#     ImGui_ImplOpenGL3_Shutdown();
#     ImGui_ImplGlfw_Shutdown();
#     ImGui.DestroyContext();

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main()

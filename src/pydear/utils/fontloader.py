import ctypes
import pathlib
import pydear as ImGui


def load(font: pathlib.Path, size: float, range: ctypes.Array, *, merge=False, monospace=False):
    '''
    https://github.com/ocornut/imgui/blob/master/docs/FONTS.md#font-loading-instructions
    '''
    # Load Fonts
    # - If no fonts are loaded, dear imgui will use the default font. You can also load multiple fonts and use ImGui.PushFont()/PopFont() to select them.
    # - AddFontFromFileTTF() will return the ImFont* so you can store it if you need to select the font among multiple.
    # - If the file cannot be loaded, the function will return NULL. Please handle those errors in your application (e.g. use an assertion, or display an error and quit).
    # - The fonts will be rasterized at a given size (w/ oversampling) and stored into a texture when calling ImFontAtlas::Build()/GetTexDataAsXXXX(), which ImGui_ImplXXXX_NewFrame below will call.
    # - Read 'docs/FONTS.md' for more instructions and details.
    # - Remember that in C/C++ if you want to include a backslash \ in a string literal you need to write a double backslash \\ !
    # io.Fonts->AddFontDefault();
    # io.Fonts->AddFontFromFileTTF("../../misc/fonts/Roboto-Medium.ttf", 16.0f);
    # io.Fonts->AddFontFromFileTTF("../../misc/fonts/Cousine-Regular.ttf", 15.0f);
    # io.Fonts->AddFontFromFileTTF("../../misc/fonts/DroidSans.ttf", 16.0f);
    # io.Fonts->AddFontFromFileTTF("../../misc/fonts/ProggyTiny.ttf", 10.0f);
    # ImFont* font = io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\ArialUni.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesJapanese());
    #IM_ASSERT(font != NULL);

    io = ImGui.GetIO()
    fonts = io.Fonts

    config = ImGui.ImFontConfig()
    # memset(this, 0, sizeof(*this));
    config.FontDataOwnedByAtlas = True
    config.OversampleH = 3 # FIXME: 2 may be a better default?
    config.OversampleV = 1
    config.GlyphMaxAdvanceX = 9999 #FLT_MAX;
    config.RasterizerMultiply = 1.0
    config.EllipsisChar = 65535 # (ImWchar)-1;    
    if merge:
        config.MergeMode = True
    if monospace:
        config.GlyphMinAdvanceX = size

    fonts.AddFontFromFileTTF(
        str(font), size, config, range
    )

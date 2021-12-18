import ctypes
import cydeer as ImGui


def load_font(size: float):
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
    # Load a first font
    fonts = io.Fonts
    # fonts.AddFontDefault()
    range = fonts.GetGlyphRangesJapanese()
    # Add character ranges and merge into the previous font
    # The ranges array is not copied by the AddFont* functions and is used lazily
    # so ensure it is available at the time of building or calling GetTexDataAsRGBA32().
    # Will not be copied by AddFont* so keep in scope.

    # fonts->AddFontFromFileTTF("DroidSans.ttf", 18.0f, &config, io.Fonts->GetGlyphRangesJapanese()); // Merge into first font
    fonts.ClearFonts()

    fonts.AddFontFromFileTTF(
        "C:/Windows/Fonts/MSGothic.ttc", size, None, range
    )

    import fontawesome47
    icons_ranges = (ctypes.c_ushort * 3)(0xf000, 0xf3ff, 0)
    config = ImGui.ImFontConfig()
    config.MergeMode = True
    config.GlyphMinAdvanceX = size
    fonts.AddFontFromFileTTF(
        str(fontawesome47.get_path()), size,
        config,
        icons_ranges)
    # Merge into first font
    fonts.Build()

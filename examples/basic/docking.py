import logging
import pathlib
import argparse
logger = logging.getLogger(__name__)

FILE_DIALOG = 'ModalFileDialog'


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', type=pathlib.Path)
    args = parser.parse_args()

    setting = None
    if args.ini:
        from pydear.utils.setting import TomlSetting
        setting = TomlSetting(args.ini)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp(
        'hello_docking', setting=setting['glfw'] if setting else None)

    from pydear.utils import dockspace
    from pydear import imgui as ImGui
    import ctypes

    def show_hello(p_open):
        if ImGui.Begin('hello', p_open):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', app.clear_color, 0, 1)
            ImGui.ColorPicker4('color', app.clear_color)
        ImGui.End()
    views = [
        dockspace.Dock('demo', ImGui.ShowDemoWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('hello', show_hello,
                       (ctypes.c_bool * 1)(True)),
    ]

    from pydear.utils import filedialog

    def menu():
        if ImGui.BeginMenu(b"File", True):
            if ImGui.MenuItem('open'):
                filedialog.open(FILE_DIALOG)
            ImGui.EndMenu()

    def modal():
        selected = filedialog.modal(FILE_DIALOG)
        if selected:
            print(f'select: {selected}')

    gui = dockspace.DockingGui(
        app.loop, docks=views, menu=menu, modal=modal, setting=setting['imgui'] if setting else None)

    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)

    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    if setting:
        gui.save()
        app.save()
        setting.save()


if __name__ == '__main__':
    main()

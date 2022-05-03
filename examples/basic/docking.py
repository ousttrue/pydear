import logging
import pathlib
import argparse
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', type=pathlib.Path)
    args = parser.parse_args()

    setting = None
    if args.ini:
        from pydear.utils.setting import BinSetting
        setting = BinSetting(args.ini)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp(
        'hello_docking', setting=setting if setting else None)

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

    def menu():
        if ImGui.BeginMenu(b"File", True):
            if ImGui.MenuItem('open'):
                async def open_task():
                    from pydear.utils import filedialog
                    selected = await filedialog.open_async(app.loop)
                    print(f'select: {selected}')
                app.loop.create_task(open_task())
            ImGui.EndMenu()

    gui = dockspace.DockingGui(
        app.loop, docks=views, menu=menu, setting=setting if setting else None)

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

import logging
import pathlib
import argparse
import ctypes
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
        'imnodes_util', setting=setting if setting else None)

    from pydear.utils.node_editor.editor import NodeEditor
    node_editor = NodeEditor('imnodes_util_editor',
                             setting=setting if setting else None)

    #
    # customize node editor
    #
    from simple_nodes import TYPES, PIN_STYLE_MAP
    for t in TYPES:
        node_editor.graph.register_type(t)
    for t, pin_style in PIN_STYLE_MAP.items():
        node_editor.graph.add_pin_style(t, pin_style)

    from pydear.utils import dockspace
    docks = [
        dockspace.Dock('node_editor', node_editor.show, (ctypes.c_bool * 1)(True))
    ]

    gui = dockspace.DockingGui(
        app.loop, docks=docks, setting=setting if setting else None)
    from pydear.backends import impl_glfw
    impl_glfw = impl_glfw.ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()

    if setting:
        node_editor.save()
        gui.save()
        app.save()
        setting.save()


if __name__ == '__main__':
    main()

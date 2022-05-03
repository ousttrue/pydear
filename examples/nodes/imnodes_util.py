import logging
import ctypes
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('imnodes_util')

    from node_editor import NodeEditor
    node_editor = NodeEditor('nodes')
    from pydear.utils import dockspace
    docks = [
        dockspace.Dock('', node_editor.show, (ctypes.c_bool * 1)(True))
    ]

    gui = dockspace.DockingGui(app.loop, docks=docks)
    from pydear.backends import impl_glfw
    impl_glfw = impl_glfw.ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    del gui


if __name__ == '__main__':
    main()

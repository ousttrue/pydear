'''
Triangle with Orthogonal Matrix
'''
from typing import Optional, Callable, List
import logging
import ctypes
from glglue import glo
from pydear import imgui as ImGui
from pydear.utils.selector import Item
from pydear.utils.mouse_event import MouseEvent, MouseInput
import glm

LOGGER = logging.getLogger(__name__)

vs = '''#version 330
in vec2 vPos;
in vec3 vCol;
out vec3 color;
uniform mat4 V;
uniform mat4 M;
void main()
{
    gl_Position = V * M * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
'''

fs = '''#version 330
in vec3 color;
out vec4 FragColor;
void main()
{
    FragColor = vec4(color, 1.0);
}
'''


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('r', ctypes.c_float),
        ('g', ctypes.c_float),
        ('b', ctypes.c_float),
    ]


SIZE = 100

vertices = (Vertex * 3)(
    Vertex(-SIZE, -SIZE, 1., 0., 0.),
    Vertex(SIZE, -SIZE, 0., 1., 0.),
    Vertex(0.,  SIZE, 0., 0., 1.)
)


class ButtonInfo:
    def __init__(self, name: str) -> None:
        self.name = name
        self.start: Optional[MouseInput] = None
        self.status = ''

    def on_pressed(self, mouse_input: MouseInput):
        self.start = mouse_input

    def on_drag(self, mouse_input: MouseInput, dx, dy):
        self.status = f'{self.name}: drag: {self.start} => ({mouse_input.x}, {mouse_input.y})'

    def on_released(self, mouse_input: MouseInput):
        self.start = None
        self.status = f'{self.name}: release'

    def show(self):
        ImGui.TextUnformatted(self.status)


class View(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('mouse event')
        self.vao: Optional[glo.Vao] = None
        self.shader: Optional[glo.Shader] = None
        self.props: List[Callable[[], None]] = []
        self.x = 0
        self.y = 0
        self.zoom = 1
        self.width = 1
        self.height = 1
        self.model = glm.mat4()
        self.view = glm.mat4()
        self.p_open = (ctypes.c_bool * 1)(True)

        self.left = ButtonInfo('left')
        mouse_event.left_pressed += [self.left.on_pressed]
        mouse_event.left_drag += [self.left.on_drag]
        mouse_event.left_released += [self.left.on_released]
        self.right = ButtonInfo('right')
        mouse_event.right_pressed += [self.right.on_pressed]
        mouse_event.right_drag += [self.right.on_drag]
        mouse_event.right_released += [self.right.on_released]

        self.middle = ButtonInfo('middle')
        mouse_event.middle_pressed += [self.middle.on_pressed]

        def on_drag(mouse_input: MouseInput, dx, dy):
            self.x -= dx * self.zoom
            self.y += dy * self.zoom

        mouse_event.middle_drag += [self.middle.on_drag, on_drag]
        mouse_event.middle_released += [self.middle.on_released]

        def on_wheel(d: int):
            if d < 0:
                self.zoom *= 1.1
            elif d > 0:
                self.zoom *= 0.9

        mouse_event.wheel += [on_wheel]

    def _update_matrix(self):
        w = self.width/2 * self.zoom
        h = self.height/2 * self.zoom

        self.view = glm.ortho(
            self.x-w, self.x+w,
            self.y-h, self.y+h,
            0, 1)

    def show(self):
        if not self.p_open[0]:
            return

        if ImGui.Begin('mouse event info', self.p_open):
            ImGui.TextUnformatted(f'{self.x}: {self.y}')
            ImGui.TextUnformatted(f'{self.width}: {self.height}')
            ImGui.TextUnformatted(f'{self.zoom}')

            ImGui.Separator()

            self.left.show()
            self.right.show()
            self.middle.show()

        ImGui.End()

    def render(self, mouse_input: MouseInput):
        self.width = mouse_input.width
        self.height = mouse_input.height
        self._update_matrix()

        if not self.shader:
            shader_or_error = glo.Shader.load(vs, fs)
            if not isinstance(shader_or_error, glo.Shader):
                LOGGER.error(shader_or_error)
                return
            self.shader = shader_or_error

            vbo = glo.Vbo()
            vbo.set_vertices(vertices)
            self.vao = glo.Vao(
                vbo, glo.VertexLayout.create_list(self.shader.program))

            #
            model = glo.UniformLocation.create(self.shader.program, "M")

            def set_M():
                model.set_mat4(glm.value_ptr(self.model))
            self.props.append(set_M)

            #
            view = glo.UniformLocation.create(self.shader.program, "V")

            def set_V():
                view.set_mat4(glm.value_ptr(self.view))
            self.props.append(set_V)

        assert self.vao
        with self.shader:
            for prop in self.props:
                prop()
            self.vao.draw(3)

from typing import NamedTuple, Dict, List, Tuple, Optional
import logging
import ctypes
import string
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from pydear.utils.selector import Item
from pydear.utils.mouse_event import MouseInput, MouseEvent
from pydear import glo
from OpenGL import GL
import glm


class Letter(NamedTuple):
    letter: str
    x: int
    y: int
    ox: int
    oy: int
    w: int
    h: int
    size: int
    uv: Tuple[float, float, float, float]

    @property
    def width(self):
        return self.ox+self.w

    def get_uv(self):
        return self.uv


class AsciiLetters:
    def __init__(self, fontfile: str, fontsize: int, w: int, h: int, padding: int) -> None:
        self.padding = padding
        self.fontsize = fontsize
        self.img = PIL.Image.new("RGBA", (w, h))
        self.draw = PIL.ImageDraw.Draw(self.img)
        self.font = PIL.ImageFont.truetype(fontfile, fontsize)
        self.x = 0
        self.y = 0
        self.letters: List[Letter] = []

    @staticmethod
    def create(fontfile: str, fontsize: int, w: int, h: int, padding: int, box=False):
        image = AsciiLetters(fontfile, fontsize, w, h, padding)
        for letter in string.digits:
            image.write_letter(letter, box)
        for letter in string.ascii_letters:
            image.write_letter(letter, box)
        for letter in string.punctuation:
            image.write_letter(letter, box)
        return image

    def write_letter(self, l, write_box: bool = False):
        bbox = self.draw.textbbox((self.x, self.y), l, font=self.font)

        letter = Letter(
            l, self.x, self.y, bbox[0]-self.x, bbox[1]-self.y, bbox[2]-bbox[0], bbox[3]-bbox[1], self.fontsize, (
                float(self.x)/self.img.width,
                float(bbox[2])/self.img.width,
                float(self.y)/self.img.height,
                float(bbox[3])/self.img.height
            ))

        assert(letter.oy + letter.h <= self.fontsize + self.padding)

        if bbox[2] > self.img.width:
            self.x = 0
            self.y += self.fontsize + self.padding

        self.letters.append(letter)

        self.draw.text((self.x, self.y), l, font=self.font)

        if write_box:
            self.draw.rectangle(bbox, fill=None, outline=(255, 0, 0))

        # advance
        self.x += letter.width + self.padding

    def save(self, name):
        self.img.save(name)

    def get_bytes(self):
        image = self.img
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        return image.tobytes('raw')


LOGGER = logging.getLogger(__name__)

vs = '''#version 330
layout (location=0) in vec2 aPos;
layout (location=1) in vec2 aUv;
out vec2 fUv;
uniform mat4 V;
void main()
{
    gl_Position = V * vec4(aPos, 0.0, 1.0);
    fUv = aUv;
}
'''

fs = '''#version 330
in vec2 fUv;
out vec4 FragColor;
uniform sampler2D ColorTexture;
void main()
{
    FragColor = texture(ColorTexture, fUv);    
}
'''


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('u', ctypes.c_float),
        ('v', ctypes.c_float),
    ]


'''
3+-+2
 |/|
0+-+1
'''
vertices = (Vertex * 65536)(
)

indices = (ctypes.c_ushort * 65536)()


def add_indices(i, x):
    indices[i] = x
    indices[i+1] = x+1
    indices[i+2] = x+2
    indices[i+3] = x+2
    indices[i+4] = x+3
    indices[i+5] = x
    return i+6, x+4


i = 0
x = 0
while i+6 < 65536:
    i, x = add_indices(i, x)


class TextRenderer(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('text')
        self.left = False
        self.index = 0
        self.letters = []
        self.size = 10
        self.shader: Optional[glo.Shader] = None
        self.props = []
        self.vao: Optional[glo.Vao] = None
        self.width = 1
        self.height = 1
        self.view = glm.mat4()
        mouse_event.left_pressed.append(self.put_letter)

    def _update_vertices(self, x, y, w, h):
        if not self.vao:
            return
        letter = self.letters[self.index]
        LOGGER.debug(f'{letter}')
        pos = self.index * 4
        l, r, b, t = letter.get_uv()
        vertices[pos] = Vertex(float(x-w), float(y-h), l, b)
        vertices[pos+1] = Vertex(float(x+w), float(y-h), r, b)
        vertices[pos+2] = Vertex(float(x+w), float(y+h), r, t)
        vertices[pos+3] = Vertex(float(x-w), float(y+h), l, t)
        self.vao.vbo.update(vertices)
        self.index += 1

    def resize(self, w: int, h: int):
        self.width = w
        self.height = h

    def wheel(self, d):
        if d < 0:
            self.size -= 1
        elif d > 0:
            self.size += 1

    def put_letter(self, x, y):
        self._update_vertices(x, y, self.size, self.size)

    def mouse_drag(self, x, y, dx, dy, left, right, middle):
        pass

    def mouse_release(self, x, y):
        pass

    def show(self):
        pass

    def render(self):
        self.view = glm.ortho(
            0, self.width,
            self.height, 0,
            0, 1)

        if not self.shader:
            image = AsciiLetters.create("verdana.ttf", 10, 256, 64, 3)
            bytes = image.get_bytes()
            self.letters = image.letters

            shader_or_error = glo.Shader.load(vs, fs)
            if not isinstance(shader_or_error, glo.Shader):
                LOGGER.error(shader_or_error)
                return
            self.shader = shader_or_error

            self.view = glm.mat4()
            view = glo.UniformLocation.create(self.shader.program, "V")

            def set_V():
                view.set_mat4(glm.value_ptr(self.view))
            self.props = [set_V]

            self.texture = glo.Texture(
                image.img.width, image.img.height, bytes)

            vbo = glo.Vbo()
            vbo.set_vertices(vertices, is_dynamic=True)
            ibo = glo.Ibo()
            ibo.set_indices(indices)
            layout = glo.VertexLayout.create_list(self.shader.program)
            LOGGER.debug(layout)
            self.vao = glo.Vao(
                vbo, layout, ibo)

        assert self.vao
        with self.shader:
            GL.glEnable(GL.GL_BLEND)
            # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)
            for prop in self.props:
                prop()
            self.texture.bind()
            self.vao.draw(self.index * 6)
            self.texture.unbind()
            GL.glDisable(GL.GL_BLEND)


if __name__ == '__main__':
    image = AsciiLetters.create("DejaVuSans.ttf", 10, 256, 64, 2)
    image.save('tmp.png')
    print(image.letters)

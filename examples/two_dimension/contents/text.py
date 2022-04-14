from typing import NamedTuple, Dict, List, Tuple
import logging
import ctypes
import string
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from pydear.utils.item import Item, Input
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


logger = logging.getLogger(__name__)

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
    def __init__(self) -> None:
        super().__init__('text')
        self._input = None
        self.index = 0
        self.letters = []
        self.size = 10

    def initialize(self):
        image = AsciiLetters.create("verdana.ttf", 10, 256, 64, 3)
        bytes = image.get_bytes()
        self.letters = image.letters

        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return

        self.view = glm.mat4()
        view = glo.UniformLocation.create(self.shader.program, "V")
        self.props = [
            glo.ShaderProp(lambda x: view.set_mat4(
                x), lambda:glm.value_ptr(self.view)),
        ]

        self.texture = glo.Texture(image.img.width, image.img.height, bytes)

        vbo = glo.Vbo()
        vbo.set_vertices(vertices, is_dynamic=True)
        ibo = glo.Ibo()
        ibo.set_indices(indices)
        layout = glo.VertexLayout.create_list(self.shader.program)
        logger.debug(layout)
        self.vao = glo.Vao(
            vbo, layout, ibo)

    def update_vertices(self, x, y, w, h, letter):
        pos = self.index * 4
        l, r, b, t = letter.get_uv()
        vertices[pos] = Vertex(float(x-w), float(y-h), l, b)
        vertices[pos+1] = Vertex(float(x+w), float(y-h), r, b)
        vertices[pos+2] = Vertex(float(x+w), float(y+h), r, t)
        vertices[pos+3] = Vertex(float(x-w), float(y+h), l, t)
        self.vao.vbo.update(vertices)
        self.index += 1

    def drag(self, input: Input):
        if self._input and not self._input.left and input.left:
            # pressed
            letter = self.letters[self.index]
            logger.debug(f'{input}: {letter}')
            self.update_vertices(
                input.x, input.y, self.size, self.size, letter)
        self._input = input
        w = input.width
        h = input.height

        if input.wheel < 0:
            self.size -= 1
        elif input.wheel > 0:
            self.size += 1

        self.view = glm.ortho(
            0, w,
            h, 0,
            0, 1)

    def render(self):
        if not self.is_initialized:
            self.initialize()
            self.is_initialized = True

        if not self.shader:
            return

        with self.shader:
            GL.glEnable(GL.GL_BLEND)
            # GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE)
            for prop in self.props:
                prop.update()
            self.texture.bind()
            self.vao.draw(self.index * 6)
            self.texture.unbind()
            GL.glDisable(GL.GL_BLEND)


if __name__ == '__main__':
    image = AsciiLetters.create("DejaVuSans.ttf", 10, 256, 64, 2)
    image.save('tmp.png')
    print(image.letters)

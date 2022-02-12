from typing import Optional, Dict, NamedTuple
import ctypes
import pkgutil
from OpenGL import GL
from pydear import nanovg
from pydear import glo

P_PATH = ctypes.POINTER(nanovg.GLNVGpath)
P_CALL = ctypes.POINTER(nanovg.GLNVGcall)

vs = pkgutil.get_data('pydear', '/assets/nanovg.vs')
assert(vs)
VS = vs
fs = pkgutil.get_data('pydear', '/assets/nanovg.fs')
assert(fs)
FS = fs

FLAGS = 0


def check_gl_error():
    while True:
        err = GL.glGetError()
        if err == GL.GL_NO_ERROR:
            break
        print(f"Error {err}")


def convertBlendFuncFactor(factor: nanovg.NVGblendFactor):
    match factor:
        case nanovg.NVGblendFactor.NVG_ZERO: return GL.GL_ZERO
        case nanovg.NVGblendFactor.NVG_ONE: return GL.GL_ONE
        case nanovg.NVGblendFactor.NVG_SRC_COLOR: return GL.GL_SRC_COLOR
        case nanovg.NVGblendFactor.NVG_ONE_MINUS_SRC_COLOR: return GL.GL_ONE_MINUS_SRC_COLOR
        case nanovg.NVGblendFactor.NVG_DST_COLOR: return GL.GL_DST_COLOR
        case nanovg.NVGblendFactor.NVG_ONE_MINUS_DST_COLOR: return GL.GL_ONE_MINUS_DST_COLOR
        case nanovg.NVGblendFactor.NVG_SRC_ALPHA: return GL.GL_SRC_ALPHA
        case nanovg.NVGblendFactor.NVG_ONE_MINUS_SRC_ALPHA: return GL.GL_ONE_MINUS_SRC_ALPHA
        case nanovg.NVGblendFactor.NVG_DST_ALPHA: return GL.GL_DST_ALPHA
        case nanovg.NVGblendFactor.NVG_ONE_MINUS_DST_ALPHA: return GL.GL_ONE_MINUS_DST_ALPHA
        case nanovg.NVGblendFactor.NVG_SRC_ALPHA_SATURATE: return GL.GL_SRC_ALPHA_SATURATE
        case _: return GL.GL_INVALID_ENUM


class GLNVGblend(NamedTuple):
    srcRGB: int
    dstRGB: int
    srcAlpha: int
    dstAlpha: int


def blendCompositeOperation(op) -> GLNVGblend:
    blend = GLNVGblend(
        convertBlendFuncFactor(op.srcRGB),  # type: ignore
        convertBlendFuncFactor(op.dstRGB),  # type: ignore
        convertBlendFuncFactor(op.srcAlpha),  # type: ignore
        convertBlendFuncFactor(op.dstAlpha))  # type: ignore
    if blend.srcRGB == GL.GL_INVALID_ENUM or blend.dstRGB == GL.GL_INVALID_ENUM or blend.srcAlpha == GL.GL_INVALID_ENUM or blend.dstAlpha == GL.GL_INVALID_ENUM:
        return GLNVGblend(
            GL.GL_ONE,  # type: ignore
            GL.GL_ONE_MINUS_SRC_ALPHA,  # type: ignore
            GL.GL_ONE,  # type: ignore
            GL.GL_ONE_MINUS_SRC_ALPHA)  # type: ignore

    return blend


class StencilFunc(NamedTuple):
    func: int = GL.GL_ALWAYS  # type: ignore
    ref: int = 0
    mask: int = 0xffffffff


class Texture(NamedTuple):
    info: nanovg.NVGtextureInfo
    resource: glo.Texture


class Pipeline:
    def __init__(self) -> None:
        shader = glo.Shader.load(VS, FS)
        assert(shader)
        self._shader = shader
        self.texture = glo.UniformLocation.create(self._shader.program, "tex")
        self.view = glo.UniformLocation.create(
            self._shader.program, "viewSize")
        # UBO
        self.frag = glo.UniformBlockIndex.create(self._shader.program, "frag")
        GL.glUniformBlockBinding(
            self._shader.program, self.frag.index, 0)
        align = GL.glGetIntegerv(GL.GL_UNIFORM_BUFFER_OFFSET_ALIGNMENT)
        self._fragSize = ctypes.sizeof(
            nanovg.GLNVGfragUniforms) + align - ctypes.sizeof(nanovg.GLNVGfragUniforms) % align

        check_gl_error()

    def use(self):
        self._shader.use()


def gl_pixel_type(pixel_type: nanovg.NVGtexture):
    match pixel_type:
        case nanovg.NVGtexture.NVG_TEXTURE_RGBA:
            return GL.GL_RGBA
        case nanovg.NVGtexture.NVG_TEXTURE_ALPHA:
            return GL.GL_RED
        case _:
            raise NotImplementedError()


class Renderer:
    def __init__(self) -> None:
        self.next_id = 1
        self._textures: Dict[int, Texture] = {}
        self._pipeline: Optional[Pipeline] = None

        # context
        self._texure = 0
        self._stencilMask = 0xffffffff
        self._stencilFunc = StencilFunc()
        self._srcRGB = {}
        self._srcAlpha = {}
        self._dstRGB = {}
        self._dstAlpha = {}
        self.shader = None
        self._vertBuf = 0
        self._vertArr = 0
        self._fragBuf = 0

        # cache
        self._blendFunc = GLNVGblend(0, 0, 0, 0)

    def __del__(self):
        pass

    def create_texture(self, image_type: nanovg.NVGtexture, w: int, h: int, flags: int, data) -> int:
        id = self.next_id
        resource = glo.Texture(
            w, h, data, pixel_type=gl_pixel_type(image_type))
        info = nanovg.NVGtextureInfo(
            id,
            0,
            w,
            h,
            image_type,
            flags
        )
        self._textures[id] = Texture(info, resource)
        self.next_id += 1
        return id

    def update_texture(self, image: int, x: int, y: int, w: int, h: int, data) -> bool:
        match self._textures.get(image):
            case (_, resource):
                resource.update(x, y, w, h, data)
                return True
        return False

    def delete_texture(self, image: int) -> bool:
        del self._textures[image]
        return True

    def get_texture(self, image: int) -> Optional[nanovg.NVGtextureInfo]:
        match self._textures.get(image):
            case (info, _):
                return info

    def blendFuncSeparate(self, blend: GLNVGblend):
        if self._blendFunc != blend:
            self._blendFunc = blend
            GL.glBlendFuncSeparate(blend.srcRGB, blend.dstRGB,
                                   blend.srcAlpha, blend.dstAlpha)

    def setUniforms(self, uniformOffset: int):
        GL.glBindBufferRange(
            GL.GL_UNIFORM_BUFFER, 0, self._fragBuf,
            uniformOffset, ctypes.sizeof(nanovg.GLNVGfragUniforms))

    def bind_texture(self, image: int):
        if image == 0:
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
            self._texure = 0
            return
        match self._textures.get(image):
            case (_, resource):
                if self._texure != resource.handle:
                    resource.bind()
                    self._texure = resource.handle
            case _:
                raise RuntimeError()

    def stencilMask(self, mask: int):
        if self._stencilMask != mask:
            self._stencilMask = mask
            GL.glStencilMask(mask)

    def stencilFunc(self, stencilFunc: StencilFunc):
        if self._stencilFunc != stencilFunc:
            self._stencilFunc = stencilFunc
            GL.glStencilFunc(stencilFunc.func,
                             stencilFunc.ref, stencilFunc.mask)

    def fill(self, call: nanovg.GLNVGcall,  pPath: P_PATH):
        paths = ctypes.pointer(pPath[call.pathOffset])  # type: ignore

        # Draw shapes
        GL.glEnable(GL.GL_STENCIL_TEST)
        self.stencilMask(0xff)
        self.stencilFunc(StencilFunc(GL.GL_ALWAYS, 0, 0xff))  # type: ignore
        GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)

        # set bindpoint for solid loc
        self.setUniforms(call.uniformOffset)  # type: ignore
        self.bind_texture(0)

        GL.glStencilOpSeparate(GL.GL_FRONT, GL.GL_KEEP,
                               GL.GL_KEEP, GL.GL_INCR_WRAP)
        GL.glStencilOpSeparate(GL.GL_BACK, GL.GL_KEEP,
                               GL.GL_KEEP, GL.GL_DECR_WRAP)
        GL.glDisable(GL.GL_CULL_FACE)
        for i in range(call.pathCount):  # type: ignore
            GL.glDrawArrays(GL.GL_TRIANGLE_FAN,
                            paths[i].fillOffset, paths[i].fillCount)
        GL.glEnable(GL.GL_CULL_FACE)

        # Draw anti-aliased pixels
        GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)

        self.setUniforms(call.uniformOffset +
                         self._pipeline._fragSize)  # type: ignore
        self.bind_texture(call.image)  # type: ignore

        # Draw fill
        self.stencilFunc(StencilFunc(
            GL.GL_NOTEQUAL, 0x0, 0xff))  # type: ignore
        GL.glStencilOp(GL.GL_ZERO, GL.GL_ZERO, GL.GL_ZERO)
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP,
                        call.triangleOffset, call.triangleCount)

        GL.glDisable(GL.GL_STENCIL_TEST)

    def convexFill(self, call: nanovg.GLNVGcall, pPaths: P_PATH):
        paths = ctypes.pointer(pPaths[call.pathOffset])  # type: ignore

        self.setUniforms(call.uniformOffset)  # type: ignore
        self.bind_texture(call.image)  # type: ignore

        for i in range(call.pathCount):  # type: ignore
            GL.glDrawArrays(GL.GL_TRIANGLE_FAN,
                            paths[i].fillOffset, paths[i].fillCount)
            # Draw fringes
            if paths[i].strokeCount > 0:
                GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, paths[i].strokeOffset,
                                paths[i].strokeCount)

    def stroke(self, call: nanovg.GLNVGcall, pPaths: P_PATH):
        assert(self._pipeline)
        paths = ctypes.pointer(pPaths[call.pathOffset])  # type: ignore
        self.setUniforms(call.uniformOffset)  # type: ignore
        self.bind_texture(call.image)  # type: ignore
        # Draw Strokes
        for i in range(call.pathCount):  # type: ignore
            GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, paths[i].strokeOffset,
                            paths[i].strokeCount)

    def triangles(self, call: nanovg.GLNVGcall):
        self.setUniforms(call.uniformOffset)  # type: ignore
        self.bind_texture(call.image)  # type: ignore
        GL.glDrawArrays(GL.GL_TRIANGLES, call.triangleOffset,
                        call.triangleCount)

    def __enter__(self):
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_BLEND)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_SCISSOR_TEST)
        GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)
        GL.glStencilMask(0xffffffff)
        GL.glStencilOp(GL.GL_KEEP, GL.GL_KEEP, GL.GL_KEEP)
        GL.glStencilFunc(GL.GL_ALWAYS, 0, 0xffffffff)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)
        GL.glBindVertexArray(0)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glUseProgram(0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def render(self, data: nanovg.NVGdrawData):
        if not self._pipeline:
            self._pipeline = Pipeline()
            self._vertArr = GL.glGenVertexArrays(1)
            self._vertBuf = GL.glGenBuffers(1)
            self._fragBuf = GL.glGenBuffers(1)

        # Upload ubo for frag shaders
        GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, self._fragBuf)
        GL.glBufferData(GL.GL_UNIFORM_BUFFER, data.uniformByteSize,
                        ctypes.c_void_p(data.pUniform), GL.GL_STREAM_DRAW)  # type: ignore

        # Upload vertex data
        GL.glBindVertexArray(self._vertArr)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vertBuf)
        GL.glBufferData(GL.GL_ARRAY_BUFFER,
                        data.vertexCount * ctypes.sizeof(nanovg.NVGvertex), ctypes.c_void_p(data.pVertex), GL.GL_STREAM_DRAW)  # type: ignore
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE,
                                 ctypes.sizeof(nanovg.NVGvertex), ctypes.c_void_p(0))
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE,
                                 ctypes.sizeof(nanovg.NVGvertex), ctypes.c_void_p(
                                     0 + 2 * ctypes.sizeof(ctypes.c_float)))

        GL.glBindBuffer(GL.GL_UNIFORM_BUFFER, self._fragBuf)

        p_call = ctypes.cast(ctypes.c_void_p(data.drawData),  # type: ignore
                             P_CALL)
        p_path = ctypes.cast(ctypes.c_void_p(data.pPath),  # type: ignore
                             P_PATH)

        # Set view and texture just once per frame.
        self._pipeline.use()
        self._pipeline.texture.set_int(0)
        self._pipeline.view.set_float2(data.view)
        GL.glActiveTexture(GL.GL_TEXTURE0)

        for i in range(data.drawCount):  # type: ignore
            call = p_call[i]

            blendFunc = blendCompositeOperation(call.blendFunc)

            self.blendFuncSeparate(blendFunc)
            match call.type:
                case nanovg.GLNVGcallType.GLNVG_FILL:
                    self.fill(call, p_path)
                case nanovg.GLNVGcallType.GLNVG_CONVEXFILL:
                    self.convexFill(call, p_path)
                case nanovg.GLNVGcallType.GLNVG_STROKE:
                    self.stroke(call, p_path)
                case nanovg.GLNVGcallType.GLNVG_TRIANGLES:
                    self.triangles(call)


g_renderer = None

RenderCreateTextureType = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
RenderDeleteTextureType = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
RenderUpdateTextureType = ctypes.CFUNCTYPE(
    ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)

P_TEXTURE = ctypes.POINTER(nanovg.NVGtextureInfo)
RrenderGetTextureType = ctypes.CFUNCTYPE(
    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int)


def createTexture(p, texture_type: int, w: int, h: int, flags: int, data) -> int:
    assert(g_renderer)
    return g_renderer.create_texture(nanovg.NVGtexture(texture_type), w, h, flags, ctypes.c_void_p(data))


CreateTexture = RenderCreateTextureType(createTexture)


def deleteTexture(p, image: int) -> bool:
    if not g_renderer:
        return False
    return g_renderer.delete_texture(image)


DeleteTexture = RenderDeleteTextureType(deleteTexture)


def updateTexture(p, image: int, x: int, y: int, w: int, h: int, data) -> bool:
    assert(g_renderer)
    return g_renderer.update_texture(image, x, y, w, h, ctypes.c_void_p(data))


UpdateTexture = RenderUpdateTextureType(updateTexture)


def getTexture(p, image: int):
    assert(g_renderer)
    tex = g_renderer.get_texture(image)
    if not tex:
        return None
    return ctypes.addressof(tex)


GetTexture = RrenderGetTextureType(getTexture)


def init(vg):
    global g_renderer
    g_renderer = Renderer()
    params = nanovg.nvgParams(vg)
    params.renderCreateTexture = ctypes.cast(  # type: ignore
        CreateTexture, ctypes.c_void_p)
    params.renderDeleteTexture = ctypes.cast(  # type: ignore
        DeleteTexture, ctypes.c_void_p)
    params.renderUpdateTexture = ctypes.cast(  # type: ignore
        UpdateTexture, ctypes.c_void_p)
    params.renderGetTexture = ctypes.cast(  # type: ignore
        GetTexture, ctypes.c_void_p)


def delete():
    global g_renderer
    del g_renderer


def render(data: nanovg.NVGdrawData):
    assert(g_renderer)
    with g_renderer:
        g_renderer.render(data)

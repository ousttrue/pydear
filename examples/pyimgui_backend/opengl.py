# -*- coding: utf-8 -*-
from __future__ import absolute_import

import OpenGL.GL as gl
import cydeer.imgui as imgui
import ctypes

from .base import BaseOpenGLRenderer


class ProgrammablePipelineRenderer(BaseOpenGLRenderer):
    """Basic OpenGL integration base class."""

    VERTEX_SHADER_SRC = """
    #version 330

    uniform mat4 ProjMtx;
    in vec2 Position;
    in vec2 UV;
    in vec4 Color;
    out vec2 Frag_UV;
    out vec4 Frag_Color;

    void main() {
        Frag_UV = UV;
        Frag_Color = Color;

        gl_Position = ProjMtx * vec4(Position.xy, 0, 1);
    }
    """

    FRAGMENT_SHADER_SRC = """
    #version 330

    uniform sampler2D Texture;
    in vec2 Frag_UV;
    in vec4 Frag_Color;
    out vec4 Out_Color;

    void main() {
        Out_Color = Frag_Color * texture(Texture, Frag_UV.st);
    }
    """

    def __init__(self):
        self._shader_handle = None
        self._vert_handle = None
        self._fragment_handle = None

        self._attrib_location_tex = None
        self._attrib_proj_mtx = None
        self._attrib_location_position = None
        self._attrib_location_uv = None
        self._attrib_location_color = None

        self._vbo_handle = None
        self._elements_handle = None
        self._vao_handle = None

        super(ProgrammablePipelineRenderer, self).__init__()

    def refresh_font_texture(self):
        # save texture state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)

        import ctypes
        fonts = ctypes.cast(
            self.io.Fonts, ctypes.POINTER(imgui.ImFontAtlas))[0]
        p = (ctypes.c_void_p * 1)()
        width = (ctypes.c_int * 1)()
        height = (ctypes.c_int * 1)()
        channels = (ctypes.c_int * 1)()
        fonts.GetTexDataAsRGBA32(p, width, height, channels)
        pixels = (ctypes.c_ubyte *
                  (width[0] * height[0] * channels[0])).from_address(p[0])

        if self._font_texture is not None:
            gl.glDeleteTextures([self._font_texture])

        self._font_texture = gl.glGenTextures(1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self._font_texture)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width[0],
                        height[0], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, pixels)

        fonts.TextureId = self._font_texture
        gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
        fonts.ClearTexData()

    def _create_device_objects(self):
        # save state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
        last_array_buffer = gl.glGetIntegerv(gl.GL_ARRAY_BUFFER_BINDING)

        last_vertex_array = gl.glGetIntegerv(gl.GL_VERTEX_ARRAY_BINDING)

        self._shader_handle = gl.glCreateProgram()
        # note: no need to store shader parts handles after linking
        vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        gl.glShaderSource(vertex_shader, self.VERTEX_SHADER_SRC)
        gl.glShaderSource(fragment_shader, self.FRAGMENT_SHADER_SRC)
        gl.glCompileShader(vertex_shader)
        gl.glCompileShader(fragment_shader)

        gl.glAttachShader(self._shader_handle, vertex_shader)
        gl.glAttachShader(self._shader_handle, fragment_shader)

        gl.glLinkProgram(self._shader_handle)

        # note: after linking shaders can be removed
        gl.glDeleteShader(vertex_shader)
        gl.glDeleteShader(fragment_shader)

        self._attrib_location_tex = gl.glGetUniformLocation(
            self._shader_handle, "Texture")
        self._attrib_proj_mtx = gl.glGetUniformLocation(
            self._shader_handle, "ProjMtx")
        self._attrib_location_position = gl.glGetAttribLocation(
            self._shader_handle, "Position")
        self._attrib_location_uv = gl.glGetAttribLocation(
            self._shader_handle, "UV")
        self._attrib_location_color = gl.glGetAttribLocation(
            self._shader_handle, "Color")

        self._vbo_handle = gl.glGenBuffers(1)
        self._elements_handle = gl.glGenBuffers(1)

        self._vao_handle = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self._vao_handle)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_handle)

        gl.glEnableVertexAttribArray(self._attrib_location_position)
        gl.glEnableVertexAttribArray(self._attrib_location_uv)
        gl.glEnableVertexAttribArray(self._attrib_location_color)

        gl.glVertexAttribPointer(self._attrib_location_position, 2, gl.GL_FLOAT, gl.GL_FALSE,
                                 20, ctypes.c_void_p(0))
        gl.glVertexAttribPointer(self._attrib_location_uv, 2, gl.GL_FLOAT, gl.GL_FALSE,
                                 20, ctypes.c_void_p(8))
        gl.glVertexAttribPointer(self._attrib_location_color, 4, gl.GL_UNSIGNED_BYTE, gl.GL_TRUE,
                                 20, ctypes.c_void_p(16))

        # restore state
        gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, last_array_buffer)
        gl.glBindVertexArray(last_vertex_array)

    def render(self, draw_data: imgui.ImDrawData):
        # perf: local for faster access
        io = self.io

        display_width = io.DisplaySize.x
        display_height = io.DisplaySize.y
        fb_width = int(display_width * io.DisplayFramebufferScale.x)
        fb_height = int(display_height * io.DisplayFramebufferScale.y)

        if fb_width == 0 or fb_height == 0:
            return

        # ToDo:
        # draw_data.scale_clip_rects(io.FramebufferScale.x, io.FramebufferScale.y)

        # backup GL state
        # todo: provide cleaner version of this backup-restore code
        last_program = gl.glGetIntegerv(gl.GL_CURRENT_PROGRAM)
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)
        last_active_texture = gl.glGetIntegerv(gl.GL_ACTIVE_TEXTURE)
        last_array_buffer = gl.glGetIntegerv(gl.GL_ARRAY_BUFFER_BINDING)
        last_element_array_buffer = gl.glGetIntegerv(
            gl.GL_ELEMENT_ARRAY_BUFFER_BINDING)
        last_vertex_array = gl.glGetIntegerv(gl.GL_VERTEX_ARRAY_BINDING)
        last_blend_src = gl.glGetIntegerv(gl.GL_BLEND_SRC)
        last_blend_dst = gl.glGetIntegerv(gl.GL_BLEND_DST)
        last_blend_equation_rgb = gl. glGetIntegerv(gl.GL_BLEND_EQUATION_RGB)
        last_blend_equation_alpha = gl.glGetIntegerv(
            gl.GL_BLEND_EQUATION_ALPHA)
        last_viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        last_scissor_box = gl.glGetIntegerv(gl.GL_SCISSOR_BOX)
        last_enable_blend = gl.glIsEnabled(gl.GL_BLEND)
        last_enable_cull_face = gl.glIsEnabled(gl.GL_CULL_FACE)
        last_enable_depth_test = gl.glIsEnabled(gl.GL_DEPTH_TEST)
        last_enable_scissor_test = gl.glIsEnabled(gl.GL_SCISSOR_TEST)

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendEquation(gl.GL_FUNC_ADD)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glActiveTexture(gl.GL_TEXTURE0)

        gl.glViewport(0, 0, int(fb_width), int(fb_height))

        ortho_projection = (ctypes.c_float * 16)(
            2.0/display_width, 0.0,                   0.0, 0.0,
            0.0,               2.0/-display_height,   0.0, 0.0,
            0.0,               0.0,                  -1.0, 0.0,
            -1.0,               1.0,                   0.0, 1.0
        )

        gl.glUseProgram(self._shader_handle)
        gl.glUniform1i(self._attrib_location_tex, 0)
        gl.glUniformMatrix4fv(self._attrib_proj_mtx, 1,
                              gl.GL_FALSE, ortho_projection)
        gl.glBindVertexArray(self._vao_handle)

        if draw_data.CmdLists:
            cmd_lists = ctypes.cast(draw_data.CmdLists, ctypes.POINTER(
                ctypes.POINTER(imgui.ImDrawList)))
            # for commands in cmd_lists:
            for i in range(draw_data.CmdListsCount):
                commands = cmd_lists[i][0]

                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_handle)
                # todo: check this (sizes)
                gl.glBufferData(gl.GL_ARRAY_BUFFER,
                                commands.VtxBuffer.Size * 20,
                                ctypes.c_void_p(commands.VtxBuffer.Data), gl.GL_STREAM_DRAW)

                gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER,
                                self._elements_handle)
                # todo: check this (sizes)
                gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, commands.IdxBuffer.Size * 2,
                                ctypes.c_void_p(commands.IdxBuffer.Data), gl.GL_STREAM_DRAW)

                # todo: allow to iterate over _CmdList
                cmd_data = ctypes.cast(
                    commands.CmdBuffer.Data, ctypes.POINTER(imgui.ImDrawCmd))
                for j in range(commands.CmdBuffer.Size):
                    command = cmd_data[j]
                    if command.TextureId:
                        gl.glBindTexture(gl.GL_TEXTURE_2D, command.TextureId)

                    # todo: use named tuple
                    rect = command.ClipRect
                    gl.glScissor(int(rect.x), int(fb_height - rect.w),
                                 int(rect.z - rect.x), int(rect.w - rect.y))
                    gl.glDrawElements(gl.GL_TRIANGLES, command.ElemCount,
                                      gl.GL_UNSIGNED_SHORT, ctypes.c_void_p(command.IdxOffset))

            # restore modified GL state
            gl.glUseProgram(last_program)
            gl.glActiveTexture(last_active_texture)
            gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)
            gl.glBindVertexArray(last_vertex_array)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, last_array_buffer)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER,
                            last_element_array_buffer)
            gl.glBlendEquationSeparate(
                last_blend_equation_rgb, last_blend_equation_alpha)
            gl.glBlendFunc(last_blend_src, last_blend_dst)

            if last_enable_blend:
                gl.glEnable(gl.GL_BLEND)
            else:
                gl.glDisable(gl.GL_BLEND)

            if last_enable_cull_face:
                gl.glEnable(gl.GL_CULL_FACE)
            else:
                gl.glDisable(gl.GL_CULL_FACE)

            if last_enable_depth_test:
                gl.glEnable(gl.GL_DEPTH_TEST)
            else:
                gl.glDisable(gl.GL_DEPTH_TEST)

            if last_enable_scissor_test:
                gl.glEnable(gl.GL_SCISSOR_TEST)
            else:
                gl.glDisable(gl.GL_SCISSOR_TEST)

        gl.glViewport(last_viewport[0], last_viewport[1],
                      last_viewport[2], last_viewport[3])
        gl.glScissor(last_scissor_box[0], last_scissor_box[1],
                     last_scissor_box[2], last_scissor_box[3])

    def _invalidate_device_objects(self):
        if self._vao_handle > -1:
            gl.glDeleteVertexArrays(1, [self._vao_handle])
        if self._vbo_handle > -1:
            gl.glDeleteBuffers(1, [self._vbo_handle])
        if self._elements_handle > -1:
            gl.glDeleteBuffers(1, [self._elements_handle])
        self._vao_handle = self._vbo_handle = self._elements_handle = 0

        gl.glDeleteProgram(self._shader_handle)
        self._shader_handle = 0

        if self._font_texture > -1:
            gl.glDeleteTextures([self._font_texture])
        self.io.fonts.texture_id = 0
        self._font_texture = 0

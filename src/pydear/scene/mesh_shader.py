from typing import Tuple, List
import glm
from .. import glo
from .camera import Camera


def get(camera: Camera) -> Tuple[glo.Shader, List[glo.ShaderProp]]:

    shader = glo.Shader.get('assets/mesh')
    assert shader
    view = glo.UniformLocation.create(shader.program, "uView")
    projection = glo.UniformLocation.create(
        shader.program, "uProjection")
    props = [
        glo.ShaderProp(
            lambda x: view.set_mat4(x),
            lambda:glm.value_ptr(camera.view.matrix)),
        glo.ShaderProp(
            lambda x: projection.set_mat4(x),
            lambda:glm.value_ptr(camera.projection.matrix)),
    ]
    return shader, props

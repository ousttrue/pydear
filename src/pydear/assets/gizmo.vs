#version 330
in vec4 aPosBone;
in vec4 aColor;
in vec4 aNormalState;

out vec4 vColor;

uniform mediump mat4 uVP;
uniform mat4 uBoneMatrices[250];

const int HOVER = 0x01;
const int SELECTED = 0x02;
const int DRAGGED = 0x04;
const int HIDE = 0x08;

void main() {

  vec3 aNormal = aNormalState.xyz;

  int index = int(aPosBone.w);
  mat4 matrix = uBoneMatrices[index];
  vec4 position = (matrix * vec4(aPosBone.xyz, 1));
  vec4 normal = (matrix * vec4(aNormal, 0));

  gl_Position = uVP * position;

  // lambert
  vec3 L = normalize(vec3(-1, 2, 3));
  vec3 N = normalize(normal.xyz);
  float v = max(dot(N, L), 0.2);

  int state = int(aNormalState.w);
  if ((state & SELECTED) != 0 || (state & DRAGGED) != 0) {
    vColor = vec4(aColor.xyz, aColor.a);
  } else if ((state & HOVER) != 0) {
    vec3 color = aColor.xyz * v;
    vColor = vec4(color + (vec3(1, 1, 1) - color) * 0.2, aColor.a);
  } else {
    vColor = vec4(aColor.xyz * v, aColor.a);
  }

  if ((state & HIDE) != 0) {
    gl_Position = vec4(0, 0, 0, 0);
  }
}

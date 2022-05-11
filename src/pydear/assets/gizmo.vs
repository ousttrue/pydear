#version 330
in vec4 aPosBone;
in vec4 aColor;
in vec3 aNormal;

out vec4 vColor;

uniform mediump mat4 uVP;
uniform mat4 uBoneMatrices[250];

void main() {

  int index = int(aPosBone.w);
  vec4 position = (uBoneMatrices[index] * vec4(aPosBone.xyz, 1));
  vec4 normal = (uBoneMatrices[index] * vec4(aNormal, 0));

  gl_Position = uVP * position;

  // lambert
  vec3 L = normalize(vec3(-1, 2, 3));
  vec3 N = normalize(normal.xyz);
  float v = max(dot(N, L), 0.2);

  vColor = vec4(aColor.xyz * v, aColor.a);
}

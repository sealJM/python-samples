#version 330
uniform mat4 in_rot;
uniform mat4 in_per;
uniform vec3 translation;
uniform vec3 scale;

in vec3 in_vert;
in vec3 in_color;

out vec3 v_color;

void main() {
    v_color = in_color;

            // Apply scaling
    vec4 scaled = vec4(in_vert, 1.0) * vec4(scale, 1.0);

            // Apply rotation
    vec4 rotated = in_rot * scaled;

            // Apply translation
    vec4 translated = rotated + vec4(translation, 0.0);

            // Apply perspective transformation
    gl_Position = in_per * translated;
}
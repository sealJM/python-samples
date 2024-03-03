import cv2
import moderngl as gl
import moderngl_window as glw
import numpy as np
import glm
import time
import struct


class Time_D:
    def __init__(self):
        self.start = time.time()
        self.last = self.start

    def delta(self):
        now = time.time()
        delta = now - self.last
        self.last = now
        return delta

    def elapsed(self):
        now = time.time()
        return now - self.start


class Shapes:
    def __init__(self) -> None:
        self.triangle = glm.mat3(
            glm.vec3(1.0, 1.0, 0.0),
            glm.vec3(-1.0, -1.0, 0.0),
            glm.vec3(1.0, -1.0, 0.0),
        )
        self.square = [
            self.triangle,
            glm.mat3(glm.rotate(glm.radians(
                180), glm.vec3(0.0, 0.0, 1.0))) * self.triangle
        ]

    def shape_bytes(self, vectors):
        flatter = [
            val for vertex in vectors for x, y, z in vertex for val in (
                x, y, z
            )]
        return struct.pack('{}f'.format(len(flatter)), *flatter)

    def cube(self):
        rotations = {
            1: glm.vec3(0.0, 1.0, 0.0),
            2: glm.vec3(1.0, 0.0, 0.0),
        }
        translations = {
            0: glm.vec3(0.0, 0.0, 1.0),  # Front
            1: glm.vec3(1.0, 0.0, 0.0),  # Right
            2: glm.vec3(0.0, 0.0, -1.0),  # Back
            3: glm.vec3(-1.0, 0.0, 0.0),  # Left
            4: glm.vec3(0.0, -1.0, 0.0),  # Bottom
            5: glm.vec3(0.0, 1.0, 0.0),  # Top
        }
        cube = []
        for i in range(4):
            # Sides
            rotated = [glm.mat3(glm.rotate(glm.radians(
                90*(i)), rotations[1])
            ) * triangle for triangle in self.square]

            translated = [
                glm.mat3(*[glm.vec3(vertex + translations[i])
                         for vertex in triangle])
                for triangle in rotated
            ]
            cube += translated

        for i in range(4, 6):
            # Top/Bottom
            rotated = [glm.mat3(glm.rotate(glm.radians(
                90+(180*(i-4))), rotations[2])
            ) * triangle for triangle in self.square]

            translated = [
                glm.mat3(*[glm.vec3(vertex + translations[i])
                         for vertex in triangle])
                for triangle in rotated
            ]
            cube += translated
        return cube


width = 640
height = 480
window_cls = glw.get_local_window_cls('pyglet')
window = window_cls(
    size=(width, height), fullscreen=False, title='ModernGL Window',
    resizable=False, vsync=False, gl_version=(3, 3)
)
ctx = window.ctx
ctx.enable(gl.CULL_FACE | gl.DEPTH_TEST)
glw.activate_context(window, ctx=ctx)
window.clear()
window.swap_buffers()

prog = ctx.program(
    vertex_shader="""
        #version 330
        uniform mat4 in_rot;
        uniform mat4 in_per;
        uniform vec3 translation;



        in vec3 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            v_color = in_color;

            // Apply scaling
            vec4 scaled = vec4(in_vert, 1.0) * vec4(2, 2, 2, 1.0);

            // Apply rotation
            vec4 rotated = in_rot * scaled;

            // Apply translation
            vec4 translated = rotated + vec4(translation, 0.0);

            // Apply perspective transformation
            gl_Position = in_per * translated;
        }
    """,
    fragment_shader="""
        #version 330

        in vec3 v_color;

        out vec4 f_color;

        void main() {
            f_color = vec4(v_color, 1.0);
        }
    """,
)

# # Create a buffer for vertex positions
shapes = Shapes()
vertexes = shapes.cube()
vbo_positions = ctx.buffer(data=shapes.shape_bytes(vertexes))


num_vertex = len(vertexes)*3

# Create an empty buffer for vertex colors
r = np.random.rand(num_vertex)
g = np.random.rand(num_vertex)
b = np.random.rand(num_vertex)
colors = np.dstack([r, g, b])
vbo_colors = ctx.buffer(colors.astype("f4").tobytes())


# Create a vertex array object (VAO) using both position and color buffers
vao = ctx.vertex_array(prog, [
    (vbo_positions, '3f', 'in_vert'),
    (vbo_colors, '3f', 'in_color')
])

fbo = ctx.framebuffer(
    color_attachments=[ctx.texture((width, height), 4)]
)

deg = 0.0
t = Time_D()
frame_time = Time_D()
frame = 0
perspective = glm.perspectiveFov(90, width, height, 0.1, 10000)
vao.program["in_per"].write(perspective)
translation = glm.vec3(0.0, 0.0, -10)
vao.program['translation'].write(translation)

fourcc = cv2.VideoWriter_fourcc(*'MPG4')
out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (width, height))


while not window.is_closing:
    # glm.scale(vertices_glm, 0.1)
    # vbo_positions.write(vertex_data.astype("f4").tobytes())
    deg += 0.02
    rotation_matrix = glm.rotate(
        glm.mat4(), glm.radians(deg), glm.normalize(glm.vec3(0.8, 0.8, 0.3)))
    # Pass the rotation matrix to the shader
    vao.program['in_rot'].write(rotation_matrix)

    fbo.use()
    fbo.clear(0.0, 0.0, 0.0, 1.0)
    vao.render(gl.TRIANGLES)

    ctx.copy_framebuffer(window.fbo, fbo)

    window.swap_buffers()

    if frame_time.elapsed() >= 1/60:
        # # Unbind the framebuffer object
        ctx.screen.use()
        frame_time.start = time.time()
        # Read the RGB data from the framebuffer
        frame_data = fbo.read(components=3, dtype='f4')

        # Convert the byte data to numpy array
        frame_np = np.frombuffer(frame_data, dtype=np.float32)

        # Reshape the data to the shape of the framebuffer
        frame_np = frame_np.reshape((height, width, 3))

        # Clip and convert the float values to uint8 (0-255)
        frame_np_uint8 = np.clip(frame_np, 0.0, 1.0) * 255
        frame_np_uint8 = frame_np_uint8.astype(np.uint8)

        # Convert the RGB data to BGR format for OpenCV
        frame_bgr = cv2.cvtColor(frame_np_uint8, cv2.COLOR_RGB2BGR)
        frame_bgr = cv2.flip(frame_bgr, 0)
        # Write the frame to the video file
        out.write(frame_bgr)

    frame += 1
    if frame % 120 == 0:
        frame = 0
        window.title = f"{(120/t.delta()):.0f}"

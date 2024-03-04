import moderngl_window as glw
import moderngl as gl
import numpy as np
# import cv2
import glm

import lib.shaders

from lib.shapes import Shapes
from lib.timer import Time_D


# Build window
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


# Load shaders
vertex = "shaders\\shader.vert"
frag = "shaders\\shader.frag"
prog = lib.shaders.create_shader_program(ctx, vertex, frag)


# # Create a buffer for vertex positions
shapes = Shapes()
vertexes = shapes.cube()
vbo_positions = ctx.buffer(shapes.shape_bytes(vertexes))


# Create a buffer for vertex colors
num_vertex = len(vertexes)*3
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


# Convert 2d space to 3d perspective
perspective = glm.perspectiveFov(90, width, height, 0.1, 10000)
vao.program["in_per"].write(perspective)

# Generic offset
translation = glm.vec3(0.0, 0.0, -10)
vao.program['translation'].write(translation)


# fourcc = cv2.VideoWriter_fourcc(*'MPG4')
# out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (width, height))

t = Time_D()
# frame_time = Time_D()
deg = 0.0
frame = 0
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

    # if frame_time.elapsed() >= 1/60:
    #     # # Unbind the framebuffer object
    #     ctx.screen.use()
    #     frame_time.start = frame_time.current()
    #     # Read the RGB data from the framebuffer
    #     frame_data = fbo.read(components=3, dtype='f4')

    #     # Convert the byte data to numpy array
    #     frame_np = np.frombuffer(frame_data, dtype=np.float32)

    #     # Reshape the data to the shape of the framebuffer
    #     frame_np = frame_np.reshape((height, width, 3))

    #     # Clip and convert the float values to uint8 (0-255)
    #     frame_np_uint8 = np.clip(frame_np, 0.0, 1.0) * 255
    #     frame_np_uint8 = frame_np_uint8.astype(np.uint8)

    #     # Convert the RGB data to BGR format for OpenCV
    #     frame_bgr = cv2.cvtColor(frame_np_uint8, cv2.COLOR_RGB2BGR)
    #     frame_bgr = cv2.flip(frame_bgr, 0)
    #     # Write the frame to the video file
    #     out.write(frame_bgr)

    frame += 1
    if frame % 120 == 0:
        frame = 0
        window.title = f"{(120/t.delta()):.0f}"

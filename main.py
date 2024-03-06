import numpy as np
import glm

# from lib.mp4_out import mp4_write
from lib.render_loop import render_loop
from lib.shaders import create_shader_program
from lib.window import new_window
from lib.shapes import Shapes


def main():
    ctx, window = new_window()

    # Load shaders
    vertex = "shaders\\shader.vert"
    frag = "shaders\\shader.frag"
    prog = create_shader_program(ctx, vertex, frag)

    # # Create a buffer for vertex positions
    shapes = Shapes()
    vertexes = shapes.cube_1x1()
    vbo_positions = ctx.buffer(shapes.shape_bytes(vertexes))

    # Create a buffer for vertex colors
    num_vertex = len(vertexes)
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
        color_attachments=[ctx.texture((window.width, window.height), 4)]
    )

    # Convert 2d space to 3d perspective
    perspective = glm.perspectiveFov(
        90, window.width, window.height, 0.1, 10000)
    vao.program["in_per"].write(perspective)

    # Generic offset
    translation = glm.vec3(0.0, 0.0, -2)
    vao.program['translation'].write(translation)

    # # Setup for writing to mp4 file
    # fourcc = cv2.VideoWriter_fourcc(*'MPG4')
    # out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (width, height))

    # Begin render loop
    render_loop(ctx, window, fbo, vao)


if __name__ == "__main__":
    main()

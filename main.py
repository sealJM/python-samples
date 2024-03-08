# from lib.mp4_out import mp4_write
from lib.render_loop import render_loop
from lib.shaders import create_shader_program
from lib.window import new_window
from lib.shapes import Shapes
import numpy as np


def main():
    objects = []
    ctx, window = new_window()

    # Load shaders
    vertex = "shaders\\shader.vert"
    frag = "shaders\\shader.frag"
    prog = create_shader_program(ctx, vertex, frag)

    # Init Objects
    for i in range(1000):
        objects.append(Shapes(ctx, prog, window))
        objects[i].z = np.random.uniform(-15, -30)
        objects[i].x = np.random.uniform(-50, 50)
        objects[i].y = np.random.uniform(-50, 50)
        objects[i].rot = np.random.uniform(-0.1, 0.1)

        objects[i].cube()
        objects[i].buffer()

    fbo = ctx.framebuffer(
        ctx.renderbuffer((window.width, window.height)),
        ctx.depth_renderbuffer((window.width, window.height)),
    )

    # # Setup for writing to mp4 file
    # fourcc = cv2.VideoWriter_fourcc(*'MPG4')
    # out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (width, height))

    # Begin render loop
    render_loop(ctx, fbo, window, objects)


if __name__ == "__main__":
    main()

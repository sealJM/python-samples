# from lib.mp4_out import mp4_write
from lib.render_loop import render_loop
from lib.shaders import create_shader_program
from lib.window import new_window
from lib.shapes import Shapes


def main():
    objects = []
    ctx, window = new_window()

    # Load shaders
    vertex = "shaders\\shader.vert"
    frag = "shaders\\shader.frag"
    prog = create_shader_program(ctx, vertex, frag)

    cube1 = Shapes(ctx, prog, window)
    cube1.z = -10.0
    cube1.x = 0
    cube1.rot = 0.01
    cube1.cube(5, 10)
    cube1.buffer()
    objects.append(cube1)

    cube2 = Shapes(ctx, prog, window)
    cube2.z = -10.0
    cube2.x = 0.5
    cube2.rot = -0.01
    cube2.cube(10, 5, 2)
    cube2.buffer()
    objects.append(cube2)

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

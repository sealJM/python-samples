import moderngl as gl
import glm

from lib.timer import Time_D


def render_loop(ctx, window, fbo, vao):
    t = Time_D()
    # frame_time = Time_D()
    deg = 0.0
    frame = 0
    while not window.is_closing:

        deg += 0.02
        rotation_matrix = glm.rotate(
            glm.mat4(),
            glm.radians(deg),
            glm.normalize(glm.vec3(0.8, 0.3, 0.6))
        )
        # Pass the rotation matrix to the shader
        vao.program['in_rot'].write(rotation_matrix)

        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)
        vao.render(gl.TRIANGLES)

        ctx.copy_framebuffer(window.fbo, fbo)

        window.swap_buffers()

        # # Write to video file
        # if frame_time.elapsed() >= 1/60:
        #     mp4_write(ctx, frame_time, fbo, window.height, window.width, out)

        frame += 1
        if frame % 120 == 0:
            frame = 0
            window.title = f"{(120/t.delta()):.0f}"

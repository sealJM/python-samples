from lib.timer import Time_D


def render_loop(ctx, fbo, window, objects):
    t = Time_D()
    # frame_time = Time_D()
    # deg = 0.0
    frame = 0
    while not window.is_closing:
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)

        for i in objects:
            i.draw()

        ctx.copy_framebuffer(window.fbo, fbo)
        window.swap_buffers()

        # # Write to video file
        # if frame_time.elapsed() >= 1/60:
        #     mp4_write(ctx, frame_time, fbo, window.height, window.width, out)

        frame += 1
        if frame % 120 == 0:
            frame = 0
            window.title = f"{(120/t.delta()):.0f}"

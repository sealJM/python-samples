import moderngl_window as glw
import moderngl as gl


def new_window():
    # Build window
    width = 1280
    height = 720
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
    return ctx, window

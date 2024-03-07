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
    ctx.enable_only(flags=gl.DEPTH_TEST | gl.CULL_FACE)
    glw.activate_context(window, ctx=ctx)

    return ctx, window

import moderngl as gl


def load_shader(file_path):
    # Read shader source code from file
    with open(file_path, 'r') as file:
        shader_source = file.read()

    return shader_source


def create_shader_program(ctx, vertex, fragment):
    # Load vertex and fragment shaders
    vertex_shader = load_shader(vertex)
    fragment_shader = load_shader(fragment)

    # Create program object
    shader_program = ctx.program(vertex_shader, fragment_shader)

    return shader_program


# Example usage
if __name__ == "__main__":
    # Create ModernGL context
    ctx = gl.create_standalone_context()

    vertex_shader_file = "shaders\\shader.vert"
    fragment_shader_file = "shaders\\shader.frag"

    shader_program = create_shader_program(
        ctx,
        vertex_shader_file,
        fragment_shader_file
    )

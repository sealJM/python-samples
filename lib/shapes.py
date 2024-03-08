import glm
import struct
import numpy as np
import moderngl as gl
# import itertools


class Shapes:
    def __init__(self, ctx, prog, window) -> None:
        self.ctx = ctx
        self.prog = prog
        self.window = window

        self.scale = 1
        self.rot = 0
        self.deg = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.shape = []
        self.index = []

    def shape_bytes(self, vertexes):
        return struct.pack('f' * len(vertexes), *vertexes)

    def index_bytes(self, indices):
        return struct.pack('I' * len(indices), *indices)

    def cube(self, x=1, y=1, z=1) -> None:
        x, y, z = x/2, y/2, z/2
        self.shape = [
            x, y, z,  # 0
            -x, y, z,  # 1
            -x, -y, z,  # 2
            x, -y, z,  # 3

            x, y, -z,  # 4
            x, -y, -z,  # 5
            -x, -y, -z,  # 6
            -x, y, -z  # 7
        ]

        self.index = [
            4, 7, 0, 1, 3, 2, 5, 6,  # top/front/bottom
            0xFFFFFFFF,
            2, 1, 6, 7, 5, 4, 3, 0  # left/back/right
        ]

    def buffer(self):
        self.vbo_positions = self.ctx.buffer(self.shape_bytes(self.shape))
        ibo = self.ctx.buffer(self.index_bytes(self.index))

        # Create a buffer for vertex colors
        num_vertex = (len(self.shape)-1)//3
        r = np.random.rand(num_vertex)
        g = np.random.rand(num_vertex)
        b = np.random.rand(num_vertex)
        colors = np.dstack([r, g, b])
        vbo_colors = self.ctx.buffer(colors.astype("f4").tobytes())

        # Create a vertex array object
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.vbo_positions, '3f', 'in_vert'),
                (vbo_colors, '3f', 'in_color')
            ],
            ibo
        )

        # Convert 2d space to 3d perspective
        perspective = glm.perspectiveFov(
            90, self.window.width, self.window.height, 0.1, 1000)
        self.vao.program["in_per"].write(perspective)

    def draw(self):
        # Position
        translation = glm.vec3(
            self.x, self.y*glm.sin(glm.radians(self.deg)), self.z)
        self.vao.program['translation'].write(translation)

        # Scale
        scale = glm.vec3(self.scale)
        self.vao.program['scale'].write(scale)

        # Rotation
        self.deg += self.rot
        rotation_matrix = glm.rotate(
            glm.mat4(),
            glm.radians(self.deg),
            glm.normalize(glm.vec3(0.0, 0.1, 0.0))
        )
        self.vao.program['in_rot'].write(rotation_matrix)

        # for i in range(0, len(self.shape), 3):
        #     self.shape[i:i+3] = (rotation_matrix *
        #                          glm.vec3(self.shape[i:i+3])).to_list()
        # self.vbo_positions.write(self.shape_bytes(self.shape))

        self.vao.render(gl.TRIANGLE_STRIP)


"""
    # Old way using pure triangles to render but would render duplicate points
    def __init__(self) -> None:
        self.triangle = glm.mat3(
            0.5, 0.5, 0.0,
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
        )

        self.square = [
            self.triangle,
            glm.mat3(glm.rotate(glm.radians(
                180), glm.vec3(0.0, 0.0, 1.0))) * self.triangle
        ]

    def shape_bytes(self, vertexes):
        return struct.pack('f' * len(vertexes), *vertexes)

    def cube_1x1(self):
        rotations = {
            1: (0.0, 1.0, 0.0),  # Sides
            2: (1.0, 0.0, 0.0),  # Top/Bottom
        }
        translations = {
            0: (0.0, 0.0, 0.5),  # Front
            1: (0.5, 0.0, 0.0),  # Right
            2: (0.0, 0.0, -0.5),  # Back
            3: (-0.5, 0.0, 0.0),  # Left
            4: (0.0, -0.5, 0.0),  # Bottom
            5: (0.0, 0.5, 0.0),  # Top
        }

        cube = []
        for i in range(4):
            # Sides
            rotated = [glm.mat3(glm.rotate(glm.radians(
                90*(i)), rotations[1])) * triangle for triangle in self.square]

            translated = []
            for triangle in rotated:
                translated_triangle = glm.mat3([translations[i]]*3) + triangle
                translated.extend(translated_triangle.to_list())
            cube.extend(translated)

        for i in range(4, 6):
            # Top/Bottom
            rotated = [(glm.mat3(glm.rotate(glm.radians(
                90+(180*(i-4))), rotations[2])
            ) * triangle) for triangle in self.square]

            translated = []
            for triangle in rotated:
                translated_triangle = glm.mat3(*[translations[i]]*3) + triangle
                translated.extend(translated_triangle.to_list())

            cube.extend(translated)

        return list(itertools.chain.from_iterable(cube))
"""

import glm
import struct


class Shapes:
    def __init__(self) -> None:
        self.triangle = glm.mat3(
            glm.vec3(1.0, 1.0, 0.0),
            glm.vec3(-1.0, -1.0, 0.0),
            glm.vec3(1.0, -1.0, 0.0),
        )
        self.square = [
            self.triangle,
            glm.mat3(glm.rotate(glm.radians(
                180), glm.vec3(0.0, 0.0, 1.0))) * self.triangle
        ]

    def shape_bytes(self, vectors):
        flatter = [
            val for vertex in vectors for x, y, z in vertex for val in (
                x, y, z
            )]
        return struct.pack('{}f'.format(len(flatter)), *flatter)

    def cube(self):
        rotations = {
            1: glm.vec3(0.0, 1.0, 0.0),
            2: glm.vec3(1.0, 0.0, 0.0),
        }
        translations = {
            0: glm.vec3(0.0, 0.0, 1.0),  # Front
            1: glm.vec3(1.0, 0.0, 0.0),  # Right
            2: glm.vec3(0.0, 0.0, -1.0),  # Back
            3: glm.vec3(-1.0, 0.0, 0.0),  # Left
            4: glm.vec3(0.0, -1.0, 0.0),  # Bottom
            5: glm.vec3(0.0, 1.0, 0.0),  # Top
        }
        cube = []
        for i in range(4):
            # Sides
            rotated = [glm.mat3(glm.rotate(glm.radians(
                90*(i)), rotations[1])
            ) * triangle for triangle in self.square]

            translated = [
                glm.mat3(*[glm.vec3(vertex + translations[i])
                         for vertex in triangle])
                for triangle in rotated
            ]
            cube += translated

        for i in range(4, 6):
            # Top/Bottom
            rotated = [glm.mat3(glm.rotate(glm.radians(
                90+(180*(i-4))), rotations[2])
            ) * triangle for triangle in self.square]

            translated = [
                glm.mat3(*[glm.vec3(vertex + translations[i])
                         for vertex in triangle])
                for triangle in rotated
            ]
            cube += translated
        return cube

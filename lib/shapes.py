import glm
import struct
import itertools


class Shapes:
    def __init__(self) -> None:
        self.triangle = glm.mat3(
            1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0,
            1.0, -1.0, 0.0,
        )

        self.square = [
            self.triangle,
            glm.mat3(glm.rotate(glm.radians(
                180), glm.vec3(0.0, 0.0, 1.0))) * self.triangle
        ]

    def shape_bytes(self, vertexes):
        return struct.pack('f' * len(vertexes), *vertexes)

    def cube(self):
        rotations = {
            1: (0.0, 1.0, 0.0),  # Sides
            2: (1.0, 0.0, 0.0),  # Top/Bottom
        }
        translations = {
            0: (0.0, 0.0, 1.0),  # Front
            1: (1.0, 0.0, 0.0),  # Right
            2: (0.0, 0.0, -1.0),  # Back
            3: (-1.0, 0.0, 0.0),  # Left
            4: (0.0, -1.0, 0.0),  # Bottom
            5: (0.0, 1.0, 0.0),  # Top
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

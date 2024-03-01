import cv2
import numpy as np
import time
from typing import List


class Window:
    def __init__(self, name="Window", width=640, height=480, fs=False) -> None:
        self.name = name
        self.width = width
        self.height = height
        if fs is True:
            self.width = 2560
            self.height = 1440
            cv2.namedWindow(name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(
                name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def show(self, screen):
        cv2.imshow(self.name, screen)


class Time_D:
    def __init__(self):
        self.start = time.time()
        self.last = self.start

    def delta(self):
        now = time.time()
        delta = now - self.last
        self.last = now
        return delta

    def elapsed(self):
        now = time.time()
        return now - self.start


class Rainbow:
    def __init__(self, w) -> None:
        # Create 1d array for width
        self.x = np.linspace(0, 1, w.width)
        # Create screen array for colour space
        self.screen = np.zeros((w.height, w.width, 3), dtype=np.uint8)
        self.w = w
        self.c = 128

    def render(self, t):
        # Blank the screen
        # self.screen[:, :, :] = 0

        # Time elapsed is used to move the rotation of colours
        t = t.elapsed()

        # Calculate the colour for each pixel based off pi, colours in 3 phase
        b = self.c*(np.sin((self.x+(t))*np.pi))+self.c
        g = self.c*(np.sin(((self.x+(t))*np.pi)+((2/3)*np.pi)))+self.c
        r = self.c*(np.sin(((self.x+(t))*np.pi)+((4/3)*np.pi)))+self.c

        # # This was redundant added to sine wave formula
        # Scale the output of the colour value to 256 bit
        # b_scaled = (b * 255).astype(np.uint8)
        # g_scaled = (g * 255).astype(np.uint8)
        # r_scaled = (r * 255).astype(np.uint8)

        # Set the colour of the pixels in the given width across the y axis
        self.screen[:, 0:self.w.width, 0] = b
        self.screen[:, 0:self.w.width, 1] = g
        self.screen[:, 0:self.w.width, 2] = r

        # # Old loop way
        # # Create a gradient rainbow image
        # for x in range(w.width):
        #     b = 0.5*(math.sin(((x/w.width)+t)*np.pi))+0.5
        #     g = 0.5*(math.sin((((x/w.width)+t)*np.pi)+((2/3)*math.pi)))+0.5
        #     r = 0.5*(math.sin((((x/w.width)+t)*np.pi)+((4/3)*math.pi)))+0.5
        #     screen[:, x, 0] = b * 255  # Blue channel
        #     screen[:, x, 1] = g * 255  # Green channel
        #     screen[:, x, 2] = r * 255  # Red channel
        self.w.show(self.screen)
        return self.screen


class Quaternion:
    Vector4 = List[float]
    Screen = List[np.uint8]

    def __init__(self, w) -> None:
        # Create screen array for colour space
        self.screen = np.zeros((w.height, w.width, 3), dtype=np.uint8)
        self.window = w
        self.w = 1.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        # self.deg = 0
        self.v = np.array([
            [0.0, 1.0, 1.0, 1.0],
            [0.0, -1.0, 1.0, 1.0],
            [0.0, -1.0, -1.0, 1.0],
            [0.0, 1.0, -1.0, 1.0],
            [0.0, 1.0, 1.0, -1.0],
            [0.0, -1.0, 1.0, -1.0],
            [0.0, -1.0, -1.0, -1.0],
            [0.0, 1.0, -1.0, -1.0],
            # Add more vertices as needed
        ])
        self.scale = 50
        self.size = 2

    def render(self) -> Screen:
        # Blank the screen
        self.screen[:, :, :] = 0

        # Apply rotation to each point in the array
        self.rotate()

        # Draw lines between every pair of adjacent points
        for i in range(len(self.v)):
            for j in range(i + 1, len(self.v)):
                # Calculate coordinates for the current and next point
                x1 = int(self.scale *
                         self.v[i][1]) + int(self.window.width / 2)
                y1 = -int(self.scale *
                          self.v[i][2]) + int(self.window.height / 2)
                x2 = int(self.scale *
                         self.v[j][1]) + int(self.window.width / 2)
                y2 = -int(self.scale *
                          self.v[j][2]) + int(self.window.height / 2)
                # Draw a line between the current and next point
                cv2.line(self.screen, (x1, y1), (x2, y2),
                         (255, 255, 255), thickness=1)

        for v in self.v:
            # Set the colour of the pixels in the given width across the y axis
            x = int(self.scale*v[1])+int(self.window.width/2)
            y = -int(self.scale*v[2])+int(self.window.height/2)
            self.screen[y-self.size:y+self.size,
                        x-self.size:x+self.size, :] = 255

        self.window.show(self.screen)
        return self.screen

    def rotate(self):

        # Old code, was using deg before
        # angle = (np.pi/180) * self.deg
        # axis = np.array([0.5, 0.7, 1.0])  # Rotation around the z-axis
        # axis /= np.linalg.norm(axis)
        # rotation_q = np.array(
        #     [np.cos(angle / 2), *np.sin(angle / 2) * axis])  # [w, x, y, z]

        # Quad defining rotation
        rotation_q = np.array([1.0, self.x, self.y, self.z])
        # Normalize the quad
        rotation_q /= np.linalg.norm(rotation_q)

        for x, i in enumerate(self.v):
            # Rotate the vectors using quaternion multiplication
            self.v[x] = self.quaternion(rotation_q, i)

    @staticmethod
    def quaternion(q1: Vector4, q2: Vector4) -> Vector4:
        # Multiplies left then inverse right with point
        rotated_v = Quaternion.q_mult(q1, q2)
        rotated_v = Quaternion.q_mult(rotated_v, Quaternion.q_conjugate(q1))
        return rotated_v

    @staticmethod
    def q_mult(q1: Vector4, q2: Vector4) -> Vector4:
        # Performs vector multiplication
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
        z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
        return np.array([w, x, y, z])

    @staticmethod
    def q_conjugate(q: Vector4) -> Vector4:
        # conjugate of quad
        w, x, y, z = q
        return np.array([w, -x, -y, -z])


def main():
    # Init window
    w = Window('Cube')
    # Init timer object
    t = Time_D()

    # Init rainbow
    # rainbow = Rainbow(w)

    # Init QuaternionCube
    quad = Quaternion(w)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MPG4')
    out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (w.width, w.height))

    # Main loop
    frame = 0
    while (True):
        screen = quad.render()
        quad.x = 0.008
        quad.y = 0.004
        quad.z = 0.002

        # screen = rainbow.render(t)
        out.write(screen)

        # Press 'q' to exit the loop
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

        # Calculate FPS averaged over 60 frames
        frame += 1
        if frame % 60 == 0:
            frame = 0
            print(60/t.delta())

    # Release everything when done
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

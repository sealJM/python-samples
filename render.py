import cv2
import numpy as np
import time


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

    def rainbow(self, t):
        # Blank the screen
        # self.screen[:, :, :] = 0

        # Time elapsed is used to move the rotation of colours
        t = t.elapsed()

        # Calculate the colour for each pixel based off pi, colours in 3 phase
        b = self.c*(np.sin((self.x+(t))*np.pi))+c
        g = self.c*(np.sin(((self.x+(t))*np.pi)+((2/3)*np.pi)))+self.c
        r = self.c*(np.sin(((self.x+(t))*np.pi)+((4/3)*np.pi)))+self.c

        # # This was redundant added to sine wave formula
        # Scale the output of the colour value to 256 bit
        # b_scaled = (b * 255).astype(np.uint8)
        # g_scaled = (g * 255).astype(np.uint8)
        # r_scaled = (r * 255).astype(np.uint8)

        # Set the colour of the pixels in the given width across the y axis
        self.screen[:, 0:w.width, 0] = b
        self.screen[:, 0:w.width, 1] = g
        self.screen[:, 0:w.width, 2] = r

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


def main():
    # Init window
    w = Window('Rainbow')
    # Init timer object
    t = Time_D()
    # Init rainbow
    rainbow = Rainbow(w)

    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'MPG4')
    # out = cv2.VideoWriter('video.mp4', fourcc, 60.0, (w.width, w.height))

    # Main loop
    frame = 0
    while (True):

        rainbow.rainbow(t)

        # screen = rainbow(w, t)
        # out.write(screen)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Calculate FPS averaged over 60 frames
        frame += 1
        if frame % 60 == 0:
            frame = 0
            print(60/t.delta())

    # Release everything when done
    # out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

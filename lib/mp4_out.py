# import cv2
import numpy as np


def mp4_write(ctx,  frame_time, fbo, height, width, out):
    # Unbind the framebuffer object
    ctx.screen.use()
    frame_time.start = frame_time.current()
    # Read the RGB data from the framebuffer
    frame_data = fbo.read(components=3, dtype='f4')

    # Convert the byte data to numpy array
    frame_np = np.frombuffer(frame_data, dtype=np.float32)

    # Reshape the data to the shape of the framebuffer
    frame_np = frame_np.reshape((height, width, 3))

    # Clip and convert the float values to uint8 (0-255)
    frame_np_uint8 = np.clip(frame_np, 0.0, 1.0) * 255
    frame_np_uint8 = frame_np_uint8.astype(np.uint8)

    # Convert the RGB data to BGR format for OpenCV
    frame_bgr = cv2.cvtColor(frame_np_uint8, cv2.COLOR_RGB2BGR)
    frame_bgr = cv2.flip(frame_bgr, 0)
    # Write the frame to the video file
    out.write(frame_bgr)

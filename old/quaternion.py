import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define quaternion multiplication


# Function to update the plot
def update(val):
    angle = slider.val * np.pi / 180  # Convert degrees to radians
    rotation_q = np.array([np.cos(angle / 2), *np.sin(angle / 2) * axis])
    rotated_v = q_mult(q_mult(rotation_q, v), q_conjugate(rotation_q))
    ax.clear()
    ax.quiver(0, 0, 0, v[1], v[2], v[3], color='r', label='Original Vector')
    ax.quiver(0, 0, 0, rotated_v[1], rotated_v[2],
              rotated_v[3], color='b', label='Rotated Vector')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    fig.canvas.draw_idle()


def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

# Define quaternion conjugate


def q_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])


# Define a vector to be rotated
# Quaternion representing a vector along the y-axis
v = np.array([0.0, 0.0, 0.0, 1.0])


# Define a rotation quaternion (e.g., 90 degrees around the z-axis)
angle = (np.pi/180) * 45  # 90 degrees in radians
axis = np.array([1.0, 0.0, 0.0])  # Rotation around the z-axis
axis /= np.linalg.norm(axis)
rotation_q = np.array(
    [np.cos(angle / 2), *np.sin(angle / 2) * axis])  # [w, x, y, z]

# Rotate the vector using quaternion multiplication
rotated_v = q_mult(q_mult(rotation_q, v), q_conjugate(rotation_q))

print("Original vector:", v)
print("Rotated vector:", rotated_v)

# Plot the vectors
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Original vector
ax.quiver(0, 0, 0, v[1], v[2], v[3], color='r', label='Original Vector')

# Rotated vector
ax.quiver(0, 0, 0, rotated_v[1], rotated_v[2],
          rotated_v[3], color='b', label='Rotated Vector')

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Add a slider to control the rotation angle
slider_ax = plt.axes([0.1, 0.02, 0.8, 0.03])
slider = Slider(slider_ax, 'Angle (degrees)', -180,
                180, valinit=0)
slider.on_changed(update)


plt.show()

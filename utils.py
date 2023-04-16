import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm

FRAME_DURATION = 150  # ms
ROTATION_RATIO = 1  # Degrees per FRAME_DURATION
INITIAL_ROTATION = 180  # Degrees
ELEVATION = 30  # View elevation in degrees


def create_3d_plot(colors, color_goal, rotation):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    r, g, b = np.array(colors).T
    ax.scatter(r, g, b, c=colors, marker='.')
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    rotation[0] = (rotation[0] + ROTATION_RATIO) % 360
    ax.view_init(azim=rotation[0], elev=ELEVATION)

    ax.scatter([color_goal.r / 255], [color_goal.g / 255], [color_goal.b / 255], c='r', marker='o')

    return fig


def plot_data(colors_list, color_goal):
    print("Plot progress")
    frames = []
    rotation = [INITIAL_ROTATION]
    for i, colors in tqdm(enumerate(colors_list), total=len(colors_list)):
        fig = create_3d_plot(colors, color_goal, rotation)
        plt.title(f"Generation {i}")
        fig.canvas.draw()
        frame = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(Image.fromarray(frame))
        plt.close(fig)

        # Save the frames as a GIF
    frames[0].save('generational_point_plot.gif', format='GIF', append_images=frames[1:], save_all=True,
                   duration=FRAME_DURATION,
                   loop=0)

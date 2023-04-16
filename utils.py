import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm


# Define a function to create a 3D scatter plot with normalized RGB colors
def create_3d_plot(colors, color_goal):
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

    ax.scatter([color_goal.r / 255], [color_goal.g / 255], [color_goal.b / 255], c='r', marker='o')

    return fig


def plot_data(colors_list, color_goal):
    # Create a list of figures to be saved as frames in the GIF
    print("Plot progress")
    frames = []
    for i, colors in tqdm(enumerate(colors_list), total=len(colors_list)):
        fig = create_3d_plot(colors, color_goal)
        fig.canvas.draw()
        # Get the RGBA array of the figure
        frame = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(Image.fromarray(frame))
        plt.close(fig)  # Close the figure to prevent it from displaying in the notebook

    # Save the frames as a GIF
    frames[0].save('3d_point_plot.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)

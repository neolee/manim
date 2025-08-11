import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def draw_mandelbrot(ax, xmin, xmax, ymin, ymax, width, height, max_iter):
    image = np.zeros((height, width))
    for row in range(height):
        for col in range(width):
            x = xmin + (xmax - xmin) * col / width
            y = ymin + (ymax - ymin) * row / height
            image[row, col] = mandelbrot(complex(x, y), max_iter)
    ax.imshow(image,
              extent=(xmin, xmax, ymin, ymax),
              cmap='viridis')  # can be `viridis` `inferno` `plasma` `cividis` `magma` etc.
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')

def on_select(eclick, erelease):
    global xmin, xmax, ymin, ymax
    xmin, xmax = min(eclick.xdata, erelease.xdata), max(eclick.xdata, erelease.xdata)
    ymin, ymax = min(eclick.ydata, erelease.ydata), max(eclick.ydata, erelease.ydata)
    ax.clear()
    draw_mandelbrot(ax, xmin, xmax, ymax, ymin, width, height, max_iter)
    plt.draw()

width, height = 800, 800
max_iter = 100
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
draw_mandelbrot(ax, xmin, xmax, ymin, ymax, width, height, max_iter)

rs = RectangleSelector(ax, on_select, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

plt.show()

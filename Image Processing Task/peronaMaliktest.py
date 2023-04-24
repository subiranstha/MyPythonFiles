import numpy as np
from scipy import misc, ndimage
import sys
np.set_printoptions(threshold=sys.maxsize)


def PeronaMalik(im, iterations, delta, kappa): # im should be a numpy array and always must be in float64:
    # initial condition
    u = im

    # center pixel distances
    dx = 1
    dy = 1
    dd = np.sqrt(2)

    # 2D finite difference windows
    windows = [
        np.array(
            [[0, 1, 0], [0, -1, 0], [0, 0, 0]], np.float64
        ),
        np.array(
            [[0, 0, 0], [0, -1, 0], [0, 1, 0]], np.float64
        ),
        np.array(
            [[0, 0, 0], [0, -1, 1], [0, 0, 0]], np.float64
        ),
        np.array(
            [[0, 0, 0], [1, -1, 0], [0, 0, 0]], np.float64
        ),
        np.array(
            [[0, 0, 1], [0, -1, 0], [0, 0, 0]], np.float64
        ),
        np.array(
            [[0, 0, 0], [0, -1, 0], [0, 0, 1]], np.float64
        ),
        np.array(
            [[0, 0, 0], [0, -1, 0], [1, 0, 0]], np.float64
        ),
        np.array(
            [[1, 0, 0], [0, -1, 0], [0, 0, 0]], np.float64
        ),
    ]

    for r in range(iterations):
        # approximate gradients
        nabla = [ndimage.convolve(u, w) for w in windows]

        # approximate diffusion function
        diff = [1. / (1 + (n / kappa) ** 2) for n in nabla]

        # update image
        terms = [diff[i] * nabla[i] for i in range(4)]
        terms += [(1 / (dd ** 2)) * diff[i] * nabla[i] for i in range(4, 8)]
        u = u + delta * (sum(terms))

    return u # now u is the difused image


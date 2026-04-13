import numpy as np
from PyQt6.QtCore import QPoint

from shape import Shape

def radius(startpoint, endpoint):
    return np.sqrt((endpoint.x() - startpoint.x())**2 + (endpoint.y() - startpoint.y())**2)

def translate(shape, startpoint, endpoint):
    transition_start = np.array([
        [startpoint.x()],
        [startpoint.y()],
    ])

    transition_end = np.array([
        [endpoint.x()],
        [endpoint.y()],
    ])

    transition_vector = transition_end - transition_start

    points = np.array(shape.get_coordinates()).T

    result_matrix = points + transition_vector

    new_shape = list(map(lambda p: QPoint(*p), np.array(result_matrix[0:2].T, dtype=int)))

    return Shape(new_shape)
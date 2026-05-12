import numpy as np
from PyQt6.QtCore import QPoint

from shape import Shape

def radius(startpoint, endpoint):
    return np.sqrt((endpoint.x() - startpoint.x())**2 + (endpoint.y() - startpoint.y())**2)

def transform(shape, origin, startpoint, endpoint):
    origin = point_to_vector(origin)
    startpoint = point_to_vector(startpoint)
    endpoint = point_to_vector(endpoint)

    transformation = transformation_vector(origin, startpoint, endpoint)

    points = np.array(shape.get_coordinates()).T
    shape_matrix = np.vstack([
        points, np.ones([len(points[0])])
    ])

    result_matrix = translation_matrix(origin) @ transformation_matrix(transformation) @ translation_matrix(-origin) @ shape_matrix

    return array_to_shape(result_matrix)

def transformation_vector(origin, startpoint, endpoint):
    M = np.vstack([np.hstack([origin, startpoint, endpoint]), np.ones(3)])

    s = M[:2, [1]]

    T = translation_matrix(-origin)
    P = T @ M

    s2 = P[:2, [1]]
    e2 = P[:2, [2]]

    s = e2 / s2

    return s


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


def translation_matrix(v):
    M = np.eye(3)
    M[0][2] = v[0][0]
    M[1][2] = v[1][0]
    return M

def transformation_matrix(v):
    M = np.eye(3)

    if np.shape(v)[0] == 1:
        M[0, 0] = M[1, 1] = v[0][0]

    else:
        M[0][0] = v[0][0]
        M[1][1] = v[1][0]

    return M

def rotatation_matrix(phi):
    c = np.cos(phi)
    s = np.sin(phi)

    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])

def point_to_vector(point:QPoint):
    return np.array([
        [point.x()],
        [point.y()]
    ])

def array_to_shape(array):
    new_shape = list(map(lambda p: QPoint(*p), np.array(array[0:2].T, dtype=int)))
    return Shape(new_shape)

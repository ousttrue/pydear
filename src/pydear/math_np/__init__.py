import numpy


class Matrix:
    def __init__(self, value: numpy.ndarray) -> None:
        self.value = value

    @staticmethod
    def identity():
        return Matrix(numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype='float'))

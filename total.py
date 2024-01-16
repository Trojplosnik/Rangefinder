import math

import numpy

from Models.Pixel import Pixel
from Models.AccelerationDimensions import AccelerationDimensions


class Total:
    def __init__(self, acceleration_dimensions: AccelerationDimensions,
                 # focal_length: float, known_real_distance: float,
                 known_real_distance: tuple[float], focal_length_prediction: float,
                 center_pixel: Pixel, known_pixels: list[Pixel]):
        self.known_real_distance = known_real_distance
        self.center_pixel = center_pixel
        self.g = acceleration_dimensions
        # self.focal_length = focal_length
        self.known_pixels = list(map(self.convert_coordinates, known_pixels))
        # list(map(self.convert_coordinates, known_pixels))
        self.focal_length = self.find_focal_length(focal_length_prediction,
                                                   *known_real_distance,
                                                   *self.known_pixels)
        self.known_F = self.find_F(self.known_pixels[0], self.known_pixels[1])

    # def find_F(self, p1: Pixel, p2: Pixel) -> float:
    #     a = self.a(p1, p2)
    #     b = self.b(p1, p2)
    #     c = self.c(p1, p2)
    #     d = self.d()
    #     e = self.e(p1, p2)
    #     f = self.f(p1, p2)
    #     return math.sqrt(a * (self.focal_length ** 2)
    #                      + b * self.focal_length + c) / \
    #         abs(d * (self.focal_length ** 2) + e * self.focal_length + f)
    def find_F(self, p1: Pixel, p2: Pixel) -> float:
        a = self.a(p1, p2)
        b = self.b(p1, p2)
        c = self.c(p1, p2)
        d = self.d()
        e = self.e(p1, p2)
        f = self.f(p1, p2)
        chicl = math.sqrt(a * (self.focal_length ** 2) + b * self.focal_length + c)
        # if d * (self.focal_length ** 2) + e * self.focal_length + f <= 0:
        #     print('*************')
        #     print(d * (self.focal_length ** 2) + e * self.focal_length + f)
        #     print('*************')
        znam = math.sqrt(d * (self.focal_length ** 2) + e * self.focal_length + f)
        return chicl / znam

    def convert_coordinates(self, p: Pixel):
        return Pixel(p.y - self.center_pixel.y, -p.x + self.center_pixel.x)

    # def find_focal_length(self, focal_length_prediction: float,
    #                       first_known_real_distance: float,
    #                       second_known_real_distance: float,
    #                       p1: Pixel, p2: Pixel, q1: Pixel, q2: Pixel) -> float:
    #     k = (first_known_real_distance / second_known_real_distance) ** 2
    #     a1 = self.a(p1, p2)
    #     b1 = self.b(p1, p2)
    #     c1 = self.c(p1, p2)
    #     d = self.d()
    #     e1 = self.e(p1, p2)
    #     f1 = self.f(p1, p2)
    #     a2 = self.a(q1, q2)
    #     b2 = self.b(q1, q2)
    #     c2 = self.c(q1, q2)
    #     e2 = self.e(q1, q2)
    #     f2 = self.f(q1, q2)
    #     coef_x6 = d ** 2 * (a1 + k * a2)
    #     coef_x5 = d * (2 * a1 * e2 + b1 * d - 2 * k * a2 * e1 - k * b2 * d)
    #     coef_x4 = (2 * a1 * d * f2 + a1 * e2 ** 2 + 2 * b1 * d * e2 + c1 * d ** 2) \
    #               - k * (2 * a2 * d * f1 + a2 * e1 ** 2 + 2 * b2 * d * e1 + c2 * d ** 2)
    #     coef_x3 = (2 * a1 * e2 * f2 + 2 * b1 * d * f2 + 2 * c1 * d * e2) \
    #               - k * (2 * a2 * e1 * f1 + 2 * b2 * d * f1 + 2 * c2 * d * e1)
    #     coef_x2 = (a1 * f2 ** 2 + 2 * b1 * e2 * f2 + 2 * c1 * d * f2 + c1 * e2 ** 2) \
    #               - k * (a2 * f1 ** 2 + 2 * b2 * e1 * f1 + 2 * c2 * d * f1 + c2 * e1 ** 2)
    #     coef_x1 = b1 * f2 ** 2 + 2 * c1 * e2 * f2 - k * (b2 * f1 ** 2 + 2 * c2 * e1 * f1)
    #     coef_x0 = c1 * f2 ** 2 - k * c2 * f1 ** 2
    #     coefficients = [coef_x6, coef_x5, coef_x4, coef_x3, coef_x2, coef_x1, coef_x0]
    #     roots = numpy.roots(coefficients)
    #     # list(map(abs, numpy.roots(coefficients)))
    #     nearest = min(roots, key=lambda x: abs(x - focal_length_prediction))
    #     return abs(nearest)

    def find_focal_length(self, focal_length_prediction: float,
                          first_known_real_distance: float,
                          second_known_real_distance: float,
                          p1: Pixel, p2: Pixel, q1: Pixel, q2: Pixel) -> float:
        k = (first_known_real_distance / second_known_real_distance) ** 2
        a1 = self.a(p1, p2)
        b1 = self.b(p1, p2)
        c1 = self.c(p1, p2)
        d = self.d()
        e1 = self.e(p1, p2)
        f1 = self.f(p1, p2)
        a2 = self.a(q1, q2)
        b2 = self.b(q1, q2)
        c2 = self.c(q1, q2)
        e2 = self.e(q1, q2)
        f2 = self.f(q1, q2)
        coef_x4 = a1 * d - k * a2 * d
        coef_x3 = (b1 * d + a1 * e2) - k * (b2 * d + a2 * e1)
        coef_x2 = (a1 * f2 + d * c1 + e2 * b1) - k * (a2 * f1 + d * c2 + e1 * b2)
        coef_x1 = (b1 * f2 + e2 * c1) - k * (b2 * f1 + e1 * c2)
        coef_x0 = c1 * f2 - k * c2 * f1
        coefficients = [coef_x4, coef_x3, coef_x2, coef_x1, coef_x0]
        roots = list(map(abs, numpy.roots(coefficients)))
        # list(map(abs, numpy.roots(coefficients)))
        print(roots)
        nearest = min(roots, key=lambda x: abs(x - focal_length_prediction))
        return nearest

    def a(self, p1: Pixel, p2: Pixel) -> float:
        return (self.g.x ** 2 + self.g.z ** 2) * (p1.x - p2.x) ** 2 + \
            (self.g.y ** 2 + self.g.z ** 2) * (p1.y - p2.y) ** 2 + \
            2 * self.g.x * self.g.y * (p2.x - p1.x) * (p2.y - p1.y)

    def b(self, p1: Pixel, p2: Pixel) -> float:
        return 2 * self.g.z * (p2.x * p1.y - p1.x * p2.y) \
            * (self.g.y * (p1.x - p2.x) + self.g.x * (p2.y - p1.y))

    def c(self, p1: Pixel, p2: Pixel) -> float:
        return (self.g.x ** 2 + self.g.y ** 2) * \
            ((p2.x * p1.y - p1.x * p2.y) ** 2)

    def d(self) -> float:
        return self.g.z ** 2

    def e(self, p1: Pixel, p2: Pixel) -> float:
        return -(self.g.x * self.g.z * p2.x + self.g.y * self.g.z * p2.y
                 + self.g.x * self.g.z * p1.x + self.g.y * self.g.z * p1.y)

    def f(self, p1: Pixel, p2: Pixel) -> float:
        return self.g.x ** 2 * p1.x * p1.y + self.g.x * self.g.y * p2.x * p1.y \
            + self.g.x * self.g.y * p1.x * p2.y + self.g.y ** 2 * p1.y * p2.y

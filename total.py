import math
from structures import Pixel, AccelerationDimensions

import numpy


class Total:
    def __init__(self, acceleration_dimensions: AccelerationDimensions,
                 focal_length: float, known_real_distance: float,
                 center_pixel: Pixel, known_pixels: list[Pixel]):
        self.known_real_distance = known_real_distance
        self.center_pixel = center_pixel
        self.g = acceleration_dimensions
        self.focal_length = focal_length
        # self.focal_length = self.find_focal_length(focal_length_prediction,
        #                                            *known_real_distance,
        #                                            *known_pixels)
        self.known_F = self.find_F(self.convert_coordinates(known_pixels[0]),
                                   self.convert_coordinates(known_pixels[1]))

    def find_F(self, p1: Pixel, p2: Pixel) -> float:
        a = self.a(p1, p2)
        b = self.b(p1, p2)
        c = self.c(p1, p2)
        d = self.d()
        e = self.e(p1, p2)
        f = self.f(p1, p2)
        return math.sqrt(a * (self.focal_length ** 2) + b * self.focal_length + c) \
               / abs(d * (self.focal_length ** 2) + e * self.focal_length + f)

    def convert_coordinates(self, p: Pixel):
        return Pixel(p.y - self.center_pixel.y, self.center_pixel.x - p.x)

    # def find_focal_length(self, focal_length_prediction: float,
    #                       first_known_real_distance: float,
    #                         second_known_real_distance: float,
    #             p1: Pixel, p2: Pixel, q1: Pixel, q2: Pixel) -> float:
    #     k = (first_known_real_distance / second_known_real_distance) ** 2
    #     a1 = self.a(p1, p2)
    #     b1 = self.b(p1, p2)
    #     c1 = self.c(p1, p2)
    #     d1 = self.d()
    #     e1 = self.e(p1, p2)
    #     f1 = self.f(p1, p2)
    #     a2 = self.a(q1, q2)
    #     b2 = self.b(q1, q2)
    #     c2 = self.c(q1, q2)
    #     d2 = self.d()
    #     e2 = self.e(q1, q2)
    #     f2 = self.f(q1, q2)
    #     coefficients = [k * a2 * d1 ** 2 - a1 * d2 ** 2,
    #                      2 * k * a2 * d1 * e1 - 2 * a1 * d2 * e2,
    #                     (2 * k * a2 * d1 * f1 + k * a2 * e1 ** 2)
    #                     - (2 * a1 * d2 * f2 + a1 * e2 ** 2),
    #                     2 * k * a2 * e1 * f1 - 2 * a1 * e2 * f2,
    #                     k * a2 * f1 ** 2 - a1 * f2 ** 2]
    #     roots = numpy.roots(coefficients).tolist()
    #     nearest = min(roots, key=lambda x: abs(x - focal_length_prediction))
    #     return nearest

    def a(self, p1: Pixel, p2: Pixel) -> float:
        return (self.g.x ** 2 + self.g.y ** 2) * (p1.x - p2.x) ** 2 + \
               (self.g.y ** 2 + self.g.z ** 2) * (p1.y - p2.y) ** 2 + \
               2 * self.g.x * self.g.y * (p2.x - p1.x) * (p2.y - p1.y)

    def b(self, p1: Pixel, p2: Pixel) -> float:
        return 2 * self.g.z * (p2.x * p1.y - p1.x * p2.y) \
               * (self.g.y * (p1.x - p2.x) + self.g.x * (p2.y - p1.y))

    def c(self, p1: Pixel, p2: Pixel) -> float:
        return (self.g.x ** 2 + self.g.y ** 2) * (p2.x * p1.y - p1.x * p2.y) ** 2

    def d(self) -> float:
        return self.g.z ** 2

    def e(self, p1: Pixel, p2: Pixel) -> float:
        return -(self.g.x * self.g.z * p2.x + self.g.y * self.g.z * p2.y
                 + self.g.x * self.g.z * p1.x + self.g.y * self.g.z * p1.y)

    def f(self, p1: Pixel, p2: Pixel) -> float:
        return self.g.x ** 2 * p1.x * p1.y + self.g.x * self.g.y * p2.x * p1.y + \
               self.g.x * self.g.y * p1.x * p2.y + self.g.y ** 2 * p1.y * p2.y

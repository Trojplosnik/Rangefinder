import math
from structures import Pixel, AccelerationDimensions


class Total:
    def __init__(self, acceleration_dimensions: AccelerationDimensions,
                 focal_length: float, known_real_distance: float,
                 p1_known: Pixel, p2_known: Pixel):
        self.known_real_distance = known_real_distance
        self.g = acceleration_dimensions
        self.focal_length = focal_length
        self.known_F =  self.find_F(p1_known, p2_known)


    def find_F(self, p1: Pixel, p2: Pixel) -> float:
        a = (self.g.x ** 2 + self.g.y ** 2) * (p1.x - p2.x) ** 2 + \
            (self.g.y ** 2 + self.g.z ** 2) * (p1.y - p2.y) ** 2 + \
            2 * self.g.x * self.g.y * (p2.x - p1.x) ** 2 * (p2.y - p1.y) ** 2
        b = 2 * self.g.z * (p2.x * p1.y - p1.x * p2.y) \
            * (self.g.y * (p1.x - p2.y) + self.g.x * (p2.y - p1.y))
        c = (self.g.x ** 2 + self.g.y ** 2) * (p2.x * p1.y - p1.x * p2.y) ** 2
        d = self.g.z ** 2
        e = -(self.g.x * self.g.z * p2.x + self.g.y * self.g.z * p2.y
              + self.g.x * self.g.z * p1.x + self.g.y * self.g.z * p1.y)
        f = self.g.x ** 2 * p1.x * p1.y + self.g.x * self.g.y * p2.x * p1.y + \
            self.g.x * self.g.y * p1.x * p2.y + self.g.y ** 2 * p1.y * p2.y
        return math.sqrt(a * (self.focal_length ** 2) + b * self.focal_length + c) \
            / abs(d * (self.focal_length ** 2) + e * self.focal_length + f)

import math


class Calculate:

    def __init__(self):
        self.T = 1
        self.theta = 0.2
        pass

    def get_noiseless_g(self, g_x: float, g_y: float, g_z: float) -> list:
        noiseless_g_list = list()
        pass

    def get_weight_formulated_by_the_Gaussian_function(self, t, tau):
        w = 1 / (math.sqrt(2 * math.pi * self.theta)) * math.exp(-1 * (t - tau) ** 2 / (2 * self.theta ** 2))
        return w


if __name__ == '__main__':
    pass
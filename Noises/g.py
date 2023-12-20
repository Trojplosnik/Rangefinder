import math


class Calculate:

    def __init__(self):
        self.T = 1
        self.theta = 0.2
        self.tau = 0.5
        pass

    def get_noiseless_g(self, g_x: list, g_y: list, g_z: list) -> list:
        noiseless_g_list = list()
        new_g_x = 0
        new_g_y = 0
        new_g_z = 0
        tmp = 0
        for i in range(self.tau - self.T / 2, self.tau + self.T / 2):
            tmp += self.get_weight_formulated_by_the_Gaussian_function(t=i, tau=self.tau)
        # tmp2 = 0
        # for i in range(self.tau - self.T / 2, self.tau + self.T / 2):
        #     tmp += self.get_weight_formulated_by_the_Gaussian_function(t=i, tau=self.tau)

    def get_weight_formulated_by_the_Gaussian_function(self, t, tau):
        w = 1 / (math.sqrt(2 * math.pi * self.theta)) * math.exp(-1 * (t - tau) ** 2 / (2 * self.theta ** 2))
        return w


def get_nearest(fs: list, f: float):
    nearest = min(fs, key=lambda x: abs(x - f))
    return nearest


if __name__ == '__main__':
    fs = list()
    fs.append(1.5)
    fs.append(2.3)
    fs.append(3.4)
    fs.append(4.1)

    f = 2.7
    print(get_nearest(fs, f))
    pass

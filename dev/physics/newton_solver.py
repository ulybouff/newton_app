import numpy as np

class NewtonSolver:
    def __init__(self, l, I0, S, N, a, d, D, n, L):
        self.l = l
        self.I0 = I0
        self.S = S
        self.N = N
        self.a = a
        self.d = d
        self.D = D
        self.n = n
        self.L = L

    def calculate(self, y_array):
        l_eff = self.l / self.n
        
        val1 = np.pi * self.a * y_array / (l_eff * self.D)
        I_diff = np.where(np.abs(val1) < 1e-9, 1.0, (np.sin(val1) / val1) ** 2)

        val2 = np.pi * self.d * y_array / (l_eff * self.D)
        denom_inter = self.N * np.sin(val2)
        I_inter = np.where(np.abs(denom_inter) < 1e-9, 1.0, (np.sin(self.N * val2) / denom_inter) ** 2)

        val3 = np.pi * self.d * self.S / (l_eff * self.L)
        V = np.where(np.abs(val3) < 1e-9, 1.0, np.abs(np.sin(val3) / val3))

        I = self.I0 * I_diff * ((1 - V) + V * I_inter)

        return {
            'I_diff': I_diff,
            'I_inter': I_inter,
            'V': V,
            'I': I
        }
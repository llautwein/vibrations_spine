import numpy as np
from scipy.integrate import solve_ivp


class MassSpringSpineModel:
    """
    Models transmission of vibrations through the human spine as one-dimensional chain of damped springs.
    In this model, there is no further damping by a cushion involved, the impact of the vibration happen
    directly on the pelvis.
    """
    def __init__(self, constant_handler, A, omega):
        """
        Class variables:

        (Vectors of size n)
        Provided by ConstantHandler (see comments there)

        (Scalars)
        A: amplitude of external, sinusoidal vibration
        omega: frequency of external, sinusoidal vibration (in rad/s)
        """
        self.m = constant_handler.m
        self.n = len(self.m)
        self.k = constant_handler.k
        self.c = constant_handler.c
        self.A = A
        self.omega = omega
        self.setup_system()

    def setup_system(self):
        left_upper = np.zeros((self.n, self.n))
        right_upper = np.identity(self.n)

        left_lower = np.zeros((self.n, self.n))
        left_lower[self.n - 1, self.n - 1] = - self.k[self.n-1] / (self.m[self.n-1] * self.omega**2)

        right_lower = np.zeros((self.n, self.n))
        right_lower[self.n - 1, self.n - 1] = - self.c[self.n - 1] / (self.m[self.n-1] * self.omega)

        for i in range(0, self.n - 1):
            left_lower[i, i] = (- self.k[i] - self.k[i+1]) / (self.m[i] * self.omega**2)
            left_lower[i + 1, i] = self.k[i+1] / (self.m[i+1] * self.omega**2)
            left_lower[i, i + 1] = self.k[i+1] / (self.m[1] * self.omega**2)
            right_lower[i, i] = (- self.c[i] - self.c[i+1]) / (self.m[i] * self.omega)
            right_lower[i + 1, i] = self.c[i+1] / (self.m[i+1] * self.omega)
            right_lower[i, i + 1] = self.c[i+1] / (self.m[i] * self.omega)

        self.system_matrix = np.block([
            [left_upper, right_upper],
            [left_lower, right_lower]
        ])
        b = np.zeros(self.n * 2)
        b[self.n] = self.A/(self.m[0]*self.omega**2)
        self.force_vector = b

    def ode_system(self, t, y, system_matrix, force_vector):
        dydt = system_matrix @ y + force_vector * np.sin(t)
        return dydt

    def solve(self, t_span, y0, t_eval):
        sol = solve_ivp(self.ode_system, t_span, y0, args=(self.system_matrix, self.force_vector),
                        method="RK45", atol=1e-7, rtol=1e-7, t_eval=t_eval)
        dri = self.dri(sol)
        return sol, dri

    def dri(self, sol):
        natural_frequency = np.sqrt(self.k[self.n-1]/self.m[self.n-1])
        gravity = 9.81
        if self.n == 1:
            dri = natural_frequency**2 * max(sol.y[0]) / gravity
        else:
            dri = natural_frequency**2 * max(abs(sol.y[self.n-2] - sol.y[self.n-1])) / gravity
        return dri





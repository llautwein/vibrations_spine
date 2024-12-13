import numpy as np
from scipy.integrate import solve_ivp


class MassSpringSpineModel:
    """
    Models transmission of vibrations through the human spine as one-dimensional chain of damped springs.
    """
    def __init__(self, constant_handler, mode, **kwargs):
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
        self.mode = mode
        if mode == "sinusoidal":
            self.sine_amplitude = kwargs.get("sine_amplitude", 0)
            self.omega = kwargs.get("sine_hertz", 0) * 2 * np.pi
        if mode == "impulsive":
            self.omega = 1
            self.impulse_amplitude = kwargs.get("impulse_amplitude", 0)
            self.impulse_peak = kwargs.get("impulse_peak", 0)
            self.eps = kwargs.get("eps", 0)
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
            left_lower[i, i + 1] = self.k[i+1] / (self.m[i] * self.omega**2)
            right_lower[i, i] = (- self.c[i] - self.c[i+1]) / (self.m[i] * self.omega)
            right_lower[i + 1, i] = self.c[i+1] / (self.m[i+1] * self.omega)
            right_lower[i, i + 1] = self.c[i+1] / (self.m[i] * self.omega)

        self.system_matrix = np.block([
            [left_upper, right_upper],
            [left_lower, right_lower]
        ])
        b = np.zeros(self.n * 2)
        if self.mode == "sinusoidal":
            b[self.n] = self.sine_amplitude/(self.m[0]*self.omega**2)
        elif self.mode == "impulsive":
            b[self.n] = self.impulse_amplitude/(self.m[0])
        self.force_vector = b

    def ode_system(self, t, y):
        if self.mode == "sinusoidal":
            dydt = self.system_matrix @ y + self.force_vector * np.sin(t)
        elif self.mode == "impulsive":
            dydt = self.system_matrix @ y + self.force_vector * np.exp(-(t - self.impulse_peak)**2/self.eps)
        return dydt

    def solve(self, t_span, y0, t_eval):
        sol = solve_ivp(self.ode_system, t_span, y0, atol=1e-12, rtol=1e-12, t_eval=t_eval, method="RK45")
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





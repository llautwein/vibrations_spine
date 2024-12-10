import numpy as np
from scipy.integrate import solve_ivp

class SeatCushionModel:

    def __init__(self, m, k, c, B, omega, compr_thr, k1c, k3c, c_c):
        """
        Class variables:

        (Vector of size n)
        m: masses,

        (Vector of size n)
        k: stiffness coefficients,
        c: damping coefficients,

        (Scalars)
        B: amplitude of external, sinusoidal vibration
        omega: frequency of external, sinusoidal vibration (in Hertz)
        compr_thr: compression threshold for the seat cushion which activates the cubic term if exceeded
        k1c: linear cushion stiffness
        k3c: cubic cushion stiffnes
        c_c: cushion damping
        """
        self.m = m
        self.n = len(m)
        self.k = k
        self.c = c
        self.B = B
        self.omega = omega
        self.compr_thr = compr_thr
        self.k1c = k1c
        self.k3c = k3c
        self.c_c = c_c
        self.setup_system()

    def setup_system(self):
        left_upper = np.zeros((self.n, self.n))
        right_upper = np.identity(self.n)

        left_lower = np.zeros((self.n, self.n))
        left_lower[self.n - 1, self.n - 1] = - self.k[self.n - 1] / (self.m[self.n - 1] * self.omega ** 2)

        right_lower = np.zeros((self.n, self.n))
        right_lower[self.n - 1, self.n - 1] = - self.c[self.n - 1] / (self.m[self.n - 1] * self.omega)

        for i in range(0, self.n - 1):
            left_lower[i, i] = (- self.k[i] - self.k[i + 1]) / (self.m[i] * self.omega ** 2)
            left_lower[i + 1, i] = self.k[i + 1] / (self.m[i + 1] * self.omega ** 2)
            left_lower[i, i + 1] = self.k[i + 1] / (self.m[1] * self.omega ** 2)
            right_lower[i, i] = (- self.c[i] - self.c[i + 1]) / (self.m[i] * self.omega)
            right_lower[i + 1, i] = self.c[i + 1] / (self.m[i + 1] * self.omega)
            right_lower[i, i + 1] = self.c[i + 1] / (self.m[i] * self.omega)

        self.system_matrix = np.block([
            [left_upper, right_upper],
            [left_lower, right_lower]
        ])

    def ode_system(self, t, y):
        print(t)
        dydt = self.system_matrix @ y + self.force_cushion(t, y[0], y[self.n])
        return dydt

    def force_cushion(self, t, x1, dx1dt):
        xs = self.B * np.sin(t*self.omega)
        if x1 - xs > 0:
            return np.zeros(2*self.n)
        elif x1 - xs > self.compr_thr:
            f_c = (- self.k1c/(self.m[1]*self.omega**2)
                   + self.k1c*self.B/(self.m[1]*self.omega**2)*np.sin(self.omega*t)
                   - self.c_c/(self.m[1]*self.omega)*dx1dt
                   + self.c_c*self.B/(self.m[1]*self.omega) * np.cos(t*self.omega))
            final_force = np.zeros(2*self.n)
            final_force[0] = f_c
            return final_force
        else:
            f_c = (- self.k1c / (self.m[1] * self.omega ** 2)
                   + self.k1c * self.B / (self.m[1] * self.omega ** 2) * np.sin(self.omega * t)
                   - self.c_c / (self.m[1] * self.omega) * dx1dt
                   + self.c_c * self.B / (self.m[1] * self.omega) * np.cos(t * self.omega)
                   - self.k3c/(self.m[1]*self.omega**2)*(x1 - self.B * np.sin(self.omega*t))**3)
            final_force = np.zeros(2 * self.n)
            final_force[0] = f_c
            return final_force

    def solve(self, t_span, y0, t_eval):
        sol = solve_ivp(self.ode_system, t_span, y0,
                        method="RK45", atol=1e-6, rtol=1e-6, t_eval=t_eval)
        return sol
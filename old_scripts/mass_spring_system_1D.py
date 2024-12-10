import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def system_of_equations(t, y, A, B):
    dydt = A @ y + B * np.sin(t)
    return dydt


n = 3
mu = 1
alpha = 10

left_upper = np.zeros((n, n))
right_upper = np.identity(n)

left_lower = np.zeros((n, n))
left_lower[n-1, n-1] = -1

right_lower = np.zeros((n, n))
right_lower[n-1, n-1] = -1 * mu

for i in range(0, n-1):
    left_lower[i, i] = -2
    left_lower[i+1, i] = 1
    left_lower[i, i+1] = 1
    right_lower[i, i] = -2 * mu
    right_lower[i + 1, i] = 1 * mu
    right_lower[i, i + 1] = 1 * mu


A_n = np.block([
    [left_upper, right_upper],
    [left_lower, right_lower]
])
B_n = np.zeros(2*n)
B_n[n] = alpha

y0 = np.zeros(2*n)
#y0 = np.array([1, 0, 0, -1, 0, 0])
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

sol = solve_ivp(system_of_equations, t_span, y0, args=(A_n, B_n), method="RK45", atol=1e-6, rtol=1e-6, t_eval=t_eval)

plt.figure(figsize=(10, 6))

for i in range(n):
    plt.plot(sol.t, sol.y[i], label=f"Displacement of mass {i+1}")

# plt.plot(sol.t, np.sin(sol.t), label=f"Sinusoidal vibration")

plt.title('Displacement of each mass in the system')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()

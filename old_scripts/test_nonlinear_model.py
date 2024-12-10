import numpy as np
from old_scripts import nonlinear_human_body_chain_model as nhbcm
import matplotlib.pyplot as plt

# masses, spring constants, damping coefficients (order: pelvis, core, torso, head)
m = np.array([1])
k = np.array([10])
c = np.array([10])
c3 = 10
n = len(m)

# amplitude, frequency
A = 10
hertz = 1
omega = 2*np.pi * hertz

HumanModel = nhbcm.HumanBodyChainModel(m, k, c, c3, A, omega)

y0 = np.zeros(2*n)
t_span = (0, 100)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

sol = HumanModel.solve(t_span, y0, t_eval)

plt.figure(figsize=(10, 6))


for i in range(0, n):
    plt.plot(sol.t, sol.y[i], label=f"Mass {i+1}")

plt.title('Displacement of each mass in the system')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()

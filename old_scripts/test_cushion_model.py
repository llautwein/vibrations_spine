import numpy as np
import mass_spring_spine_model as hbcm
import seat_cushion_model as scm
import matplotlib.pyplot as plt

# masses, spring constants, damping coefficients (order: pelvis, core, torso, head)
m = np.array([1, 1, 1.5])
k = np.array([10, 10, 10])
c = np.array([10, 10, 10])
n = len(m)

# amplitude, frequency
A = 10
hertz = 1
omega = 2*np.pi * hertz

compr_thr = 0.1
k1c = 10
k3c = 10
c_c = 10

SeatModel = scm.SeatCushionModel(m, k, c, A, omega, compr_thr, k1c, k3c, c_c)

y0 = np.zeros(2*n)
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

sol = SeatModel.solve(t_span, y0, t_eval)

plt.figure(figsize=(10, 6))
labels = ["Pelvis", "Lower body (core)", "Head"]

for i in range(0, n):
    plt.plot(sol.t, sol.y[i], label=labels[i])

plt.title('Displacement of each mass in the system')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()

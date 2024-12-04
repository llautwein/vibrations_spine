import numpy as np
import human_body_chain_model as hbcm
import matplotlib.pyplot as plt

# masses, spring constants, damping coefficients
m = np.array([7, 20, 30, 5])
k = np.array([15000, 20000, 10000, 1000])
c = np.array([1000, 1300, 1000, 200])
n = len(m)

# amplitude, frequency
A = 1
hertz = 10
omega = 2*np.pi * hertz

HumanModel = hbcm.HumanBodyChainModel(m, k, c, A, omega)

y0 = np.zeros(2*n)
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

sol = HumanModel.solve(t_span, y0, t_eval)

plt.figure(figsize=(10, 6))
labels = ["Pelvis", "Lower body (core)", "Torso", "Head"]

for i in range(n):
    plt.plot(sol.t, sol.y[i], label=labels[i])

#plt.plot(sol.t, np.sin(sol.t*omega), label=f"Sinusoidal vibration")

plt.title('Displacement of each mass in the system')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()

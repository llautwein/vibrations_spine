import numpy as np
import mass_spring_spine_model as hbcm
import matplotlib.pyplot as plt

# masses, spring constants, damping coefficients (order: pelvis, core, torso, head)
m = np.array([1])
k = np.array([1])
c = np.array([10])
n = len(m)

print(2*np.sqrt(m[0]*k[0]))
print(2*m[0]*k[0])
#print(2*np.sqrt(m[1]*k[1]))

# amplitude, frequency
A = 1
hertz = 2
omega = 2*np.pi * hertz

HumanModel = hbcm.HumanBodyChainModel(m, k, c, A, omega)

y0 = np.zeros(2*n)
t_span = (0, 200)
t_eval = np.linspace(t_span[0], t_span[1], 10000)

sol = HumanModel.solve(t_span, y0, t_eval)

plt.figure(figsize=(10, 6))

for i in range(0, n):
    plt.plot(sol.t, sol.y[i], label=f"Displacement of mass {i+1}")

plt.title('Displacement of each mass in the system')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()

import numpy as np
import visualiser

# this script visualises the resonance effect in the human body model
# the plot shows on the x-axis scaling between 0.5 * natual_frequency to 2*natural_frequency
# on the y-axis maximal amplitude of the response of the system
# -> amplitude is maximal when external frequency matches the natural frequency of the system

# masses, spring constants, damping coefficients (order: pelvis, core, torso, head)
m = np.array([5])
k = np.array([4805])
c = np.array([69.44])
n = len(m)

natural_frequency = np.sqrt(k[0]/m[0])
damping_ratio = c[0]/(2*np.sqrt(m[0]*k[0]))
gravity = 9.81

print(f"Natural frequency of the spine model: {natural_frequency/(2*np.pi)}")
print(f"Damping ratio of the spine model: {damping_ratio}")

# amplitude
A = 1
frequency = 20

visualiser = visualiser.Visualiser()
visualiser.resonance_test(m[0], k[0], c[0], A)
visualiser.plot_dri(m[0], k[0], c[0], A)
visualiser.plot_displacements(m, k, c, A, omega=frequency)


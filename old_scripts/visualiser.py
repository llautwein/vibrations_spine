import numpy as np
import matplotlib.pyplot as plt
import mass_spring_spine_model as hbcm


class Visualiser:
    def __init__(self):
        pass

    def resonance_test(self, m, k, c, A):
        # resonance test for a mass spring system with one mass
        natural_frequency = np.sqrt(k / m)
        damping_ratio = c / (2 * np.sqrt(m * k))
        print(f"Natural frequency of the spine model: {natural_frequency / (2 * np.pi)} [Hertz]")
        print(f"Damping ratio of the spine model: {damping_ratio}")
        scale = np.linspace(0.5, 2, 20)
        hertz = scale * (natural_frequency / (2 * np.pi))

        abs_amp = []
        for j in range(len(hertz)):
            omega = 2 * np.pi * hertz[j]
            HumanModel = hbcm.HumanBodyChainModel([m], [k], [c], A, omega)

            y0 = np.zeros(2)
            t_span = (0, 100)
            t_eval = np.linspace(t_span[0], t_span[1], 10000)

            sol = HumanModel.solve(t_span, y0, t_eval)
            abs_amp.append((max(abs(sol.y[0]))))
            print(f"DRI: {HumanModel.dri(sol)}")
        plt.figure()
        plt.plot(hertz, abs_amp)
        plt.title('Resonance effect of the system')
        plt.xlabel('External frequency')
        plt.ylabel('Maximal displacement of the mass')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_dri(self, m, k, c, A):
        natural_frequency = np.sqrt(k / m)
        scale = np.linspace(0.5, 2, 20)
        hertz = scale * (natural_frequency / (2 * np.pi))
        dri = []
        for j in range(len(hertz)):
            omega = 2 * np.pi * hertz[j]
            HumanModel = hbcm.HumanBodyChainModel([m], [k], [c], A, omega)

            y0 = np.zeros(2)
            t_span = (0, 100)
            t_eval = np.linspace(t_span[0], t_span[1], 10000)

            sol = HumanModel.solve(t_span, y0, t_eval)
            dri.append(HumanModel.dri(sol))
        plt.figure()
        plt.plot(hertz, dri)
        plt.title('DRI in dependence of frequencies near the natural frequency')
        plt.xlabel('External frequency')
        plt.ylabel("DRI")
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_displacements(self, m, k, c, A, omega, t_span, t_eval):
        HumanModel = hbcm.HumanBodyChainModel(m, k, c, A, omega)

        y0 = np.zeros(2 * len(m))

        sol = HumanModel.solve(t_span, y0, t_eval)

        plt.figure(figsize=(10, 6))
        #for i in range(0, len(m)):
        plt.plot(sol.t, sol.y[len(m)], label=f"Displacement of the head")

        plt.title('Displacement of each mass in the system')
        plt.xlabel('Time')
        plt.ylabel('Displacement')
        plt.legend()
        plt.grid(True)
        plt.show()

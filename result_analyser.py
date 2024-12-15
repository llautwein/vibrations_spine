import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import mass_spring_spine_model as mssm
import constants_handler

# ToDo: Impulsive forcing: plot for maximal displacement of the head vs. amplitude for different damping ratios


class ResultAnalyser:
    """
    This class gets the model as an input, solves it with different choices of variables and visualises
    the results in plots. For different visualisations, various methods are implemented.
    """
    def __init__(self, model_constants):
        self.model_constants = model_constants
        self.n = len(self.model_constants.m)
        self.y0 = np.zeros(2*self.n)
        params = {'legend.fontsize': '28',
                  'axes.labelsize': '28',
                  'axes.titlesize': '28',
                  'xtick.labelsize': '28',
                  'ytick.labelsize': '28'}
        pylab.rcParams.update(params)


class MSSMAnalyser(ResultAnalyser):

    def __init__(self, model_constants):
        super().__init__(model_constants)
        self.natural_frequency = np.sqrt(self.model_constants.k[self.n-1] / self.model_constants.m[self.n-1])

    def displacement(self, bool_plot_all, t_span, mode, **kwargs):
        """
        Plots displacement of head (and cushion) for one external forcing function
        :param bool_plot_all: if true, cushion and head displacement are plotted. if false, only head
        :param t_span: Time interval in seconds
        :param mode: Either sinusoidal or impulsive for the forcing functions
        :param kwargs: for sine: sine_amplitude and sine_hert; for impulsive: impulse_amplitude and impulse_peak
        :return: Plot
        """
        if mode == "sinusoidal":
            sine_amplitude = kwargs.get("sine_amplitude", 0)
            sine_hertz = kwargs.get("sine_hertz", 0)
            spine_model = mssm.MassSpringSpineModel(self.model_constants, "sinusoidal",
                                                    sine_amplitude=sine_amplitude, sine_hertz=sine_hertz)
            t_span[1] *= sine_hertz * 2 * np.pi
            sol, dri = spine_model.solve(t_span, self.y0)
            t_span[1] /= sine_hertz * 2 * np.pi

            plt.figure()
            if bool_plot_all:
                labels = ["Cushion", "Head"]
                plt.plot(sol.t / (sine_hertz * 2 * np.pi), sol.y[0] * 1000, label=labels[0])
                plt.plot(sol.t / (sine_hertz * 2 * np.pi), sol.y[self.n-1] * 1000, label=labels[1], color="r")
            else:
                plt.plot(sol.t / (sine_hertz*2*np.pi), sol.y[self.n-1]*1000, label="Displacement of the head for sine")
            plt.xlabel("Time t [s]")
            plt.ylabel("Relative Displacement [mm]")
            plt.grid(True)
            plt.legend()
            plt.show()
        elif mode == "impulsive":
            impulse_amplitude = kwargs.get("impulse_amplitude", 0)
            impulse_peak = kwargs.get("impulse_peak", 0)
            eps = kwargs.get("eps", 0)
            spine_model = mssm.MassSpringSpineModel(self.model_constants, "impulsive", impulse_amplitude=impulse_amplitude,
                                                    impulse_peak=impulse_peak, eps=eps)
            sol, dri = spine_model.solve(t_span, self.y0)

            plt.figure()
            if bool_plot_all:
                labels = ["Cushion", "Head"]
                plt.plot(sol.t, sol.y[0] * 1000, label=labels[0])
                plt.plot(sol.t, sol.y[self.n-1] * 1000, label=labels[1], color="r")
            else:
                plt.plot(sol.t, sol.y[self.n-1]*1000, label="Displacement of the head for sine")
            plt.xlabel("Time t [s]")
            plt.ylabel("Relative Displacement [mm]")
            plt.legend()
            plt.grid(True)
            plt.show()

    def frequency_head_displacement_sine(self, t_span, sine_hertz_values, sine_amplitude):
        """
        Plots head displacement for different frequencies
        :param t_span: Interval in seconds
        :param sine_hertz_values: Hertz of the sinusoidal vibration
        :param sine_amplitude: Amplitude of sine function
        :return: Plot
        """
        t_values = []
        solutions = []
        labels = []
        for i in range(len(sine_hertz_values)):

            spine_model = mssm.MassSpringSpineModel(self.model_constants, "sinusoidal",
                                                    sine_amplitude=sine_amplitude, sine_hertz=sine_hertz_values[i])
            t_span[1] *= sine_hertz_values[i] * 2 * np.pi
            sol, dri = spine_model.solve(t_span, self.y0)
            t_span[1] /= sine_hertz_values[i] * 2 * np.pi
            solutions.append(sol.y[self.n-1])
            t_values.append(sol.t / (sine_hertz_values[i] * 2 * np.pi))
            labels.append(f"{sine_hertz_values[i]} Hz")

        plt.figure()
        for j in range(len(sine_hertz_values)):
            plt.plot(t_values[j], solutions[j]*1000, label=labels[j])
        plt.xlabel("Time t [s]")
        plt.ylabel("Relative Displacement of the head [mm]")
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.show()

    def resonance(self, t_span, sine_amplitude):
        """
        Visualises resonance effect, i.e. plots maximal displacement against frequencies
        :param t_span: Time interval in seconds in which the model should be solved
        :param sine_amplitude: Amplitude of the sine
        :return: Plot
        """
        scale = np.linspace(0.5, 2, 100)
        frequencies = scale * self.natural_frequency / (2*np.pi)
        max_displacements = []
        dri_values = []
        for i in range(len(frequencies)):
            print(f"Resonance test: solving for omega={round(frequencies[i]/(2*np.pi), 2)}")
            spine_model = mssm.MassSpringSpineModel(self.model_constants, "sinusoidal",
                                                    sine_amplitude=sine_amplitude, sine_hertz=frequencies[i])
            t_span[1] *= frequencies[i] * 2 * np.pi
            sol, dri = spine_model.solve(t_span, self.y0)
            t_span[1] /= frequencies[i] * 2 * np.pi
            max_displacements.append(max(sol.y[self.n-1]))
            dri_values.append(dri)

        plt.figure()
        plt.plot(frequencies, np.array(max_displacements) * 1000)
        plt.xlabel('External frequency [Hz]')
        plt.ylabel('Max. displacement [mm]')
        plt.axvline(x=self.natural_frequency/(2*np.pi), color='r', linestyle='--',
                    label="Natural frequency of the system")
        plt.legend()
        plt.grid(True)
        plt.show()

    def amplitude_max_displacements_sine(self, damping_ratios, t_span, sine_amplitudes, sine_hertz):
        """
        Plots maximal displacement of the head against the sinusoidal amplitude for different cushion damping ratios
        :param damping_ratios: Damping ratios of the cushion
        :param t_span: Time t in seconds
        :param sine_amplitudes: Amplitudes of the sine function
        :param sine_hertz: Frequency in Hz of the sine function
        :return: Plot
        """
        final_result = []
        labels = []
        for i in range(len(damping_ratios)):
            print(f"Amplitude displacement plot: solving for damping ratio={round(damping_ratios[i], 2)}")
            self.model_constants = constants_handler.CushionMDOFModel5(damping_ratios[i])
            max_displacements = []
            for j in range(len(sine_amplitudes)):
                spine_model = mssm.MassSpringSpineModel(self.model_constants, "sinusoidal",
                                                        sine_amplitude=sine_amplitudes[j], sine_hertz=sine_hertz)
                t_span[1] *= sine_hertz * 2 * np.pi
                sol, dri = spine_model.solve(t_span, self.y0)
                t_span[1] /= sine_hertz * 2 * np.pi
                max_displacements.append(1000*max(abs(sol.y[len(self.model_constants.m)-1])))
            final_result.append(max_displacements)
            labels.append(f"Damping ratio = {damping_ratios[i]}")

        plt.figure()
        for k in range(len(damping_ratios)):
            plt.plot(sine_amplitudes, final_result[k], label=labels[k])
        plt.xlabel('Sinusoidal amplitude [N]')
        plt.ylabel('Maximal displacement of the head [mm]')
        plt.legend()
        plt.grid(True)
        plt.show()

    def frequency_max_displacement_sine(self, damping_ratios, t_span, sine_hertz_values, sine_amplitude):
        """
        Plots maximal displacement against different frequencies for sinusoidal vibrations
        :param damping_ratios: Damping ratios of the cushion
        :param t_span: Time in seconds for which the model should be solved
        :param sine_hertz_values: The frequencies of the sine function in Hz
        :param sine_amplitude: Amplitude of the sine function
        :return: Plot
        """
        final_result = []
        labels = []
        for i in range(len(damping_ratios)):
            print(f"Frequency displacement plot: solving for damping ratio={round(damping_ratios[i], 2)}")
            self.model_constants = constants_handler.CushionMDOFModel5(damping_ratios[i])
            max_displacements = []
            for j in range(len(sine_hertz_values)):
                spine_model = mssm.MassSpringSpineModel(self.model_constants, "sinusoidal",
                                                        sine_amplitude=sine_amplitude,
                                                        sine_hertz=sine_hertz_values[j])
                t_span[1] *= sine_hertz_values[j]
                sol, dri = spine_model.solve(t_span, self.y0)
                t_span[1] /= sine_hertz_values[j]
                max_displacements.append(1000 * max(abs(sol.y[len(self.model_constants.m) - 1])))
            final_result.append(max_displacements)
            labels.append(f"Damping ratio = {damping_ratios[i]}")

        plt.figure()
        for k in range(len(damping_ratios)):
            plt.plot(sine_hertz_values, final_result[k], label=labels[k])
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Maximal displacement of the head [mm]')
        plt.legend()
        plt.grid(True)
        plt.show()





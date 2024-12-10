import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import mass_spring_spine_model as mssm

# ToDo: adjust t_span so that the model is solved for the same amount of seconds?
# ToDo: solution measure
# ToDo: DRI extension to multiple masses?


class ResultAnalyser:
    """
    This class gets the model as an input, solves it with different choices of variables and visualises
    the results in plots. For different visualisations, various methods are implemented.
    """
    def __init__(self, model_constants):
        self.model_constants = model_constants
        self.n = len(self.model_constants.m)
        self.y0 = np.zeros(2*self.n)
        params = {'legend.fontsize': 'xx-large',
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)

    def displacement(self, t_span, t_eval, mode, **kwargs):
        pass


class MSSMAnalyser(ResultAnalyser):

    def __init__(self, model_constants):
        super().__init__(model_constants)
        self.natural_frequency = np.sqrt(self.model_constants.k[self.n-1] / self.model_constants.m[self.n-1])

    def displacement(self, t_span, t_eval, mode, **kwargs):
        if mode == "sinusoidal":
            sine_amplitude = kwargs.get("sine_amplitude", 0)
            sine_hertz = kwargs.get("sine_hertz", 0)
            sine_frequency = sine_hertz * 2 * np.pi

            spine_model = mssm.MassSpringSpineModel(self.model_constants, sine_amplitude, sine_frequency)
            sol, dri = spine_model.solve(t_span, self.y0, t_eval)

            plt.figure()
            plt.plot(sol.t / sine_frequency, sol.y[self.n-2] * 1000, label="Displacement of the head")
            plt.xlabel("Time t [s]")
            plt.ylabel("Relative Displacement y [mm]")
            plt.show()

    def resonance(self, t_span, t_eval, sine_amplitude):
        scale = np.linspace(0.5, 2, 100)
        frequencies = scale * self.natural_frequency
        max_displacements = []
        dri_values = []
        for i in range(len(frequencies)):
            print(f"Resonance test: solving for omega={round(frequencies[i]/(2*np.pi), 2)}")
            spine_model = mssm.MassSpringSpineModel(self.model_constants, sine_amplitude, frequencies[i])
            sol, dri = spine_model.solve(t_span, self.y0, t_eval)
            max_displacements.append(max(sol.y[self.n-1]))
            dri_values.append(dri)

        plt.figure()
        plt.plot(frequencies / (2*np.pi), np.array(max_displacements) * 1000)
        plt.xlabel('External frequency omega [Hz]')
        plt.ylabel('Max. displacement [mm]')
        plt.axvline(x=self.natural_frequency/(2*np.pi), color='r', linestyle='--',
                    label="Natural frequency of the system")
        plt.legend()
        plt.grid(True)
        plt.show()

    def amplitude_dri(self, t_span, t_eval, sine_amplitudes):
        dri_values = []
        for i in range(len(sine_amplitudes)):
            print(f"Amplitude DRI plot: solving for A={round(sine_amplitudes[i], 2)}")
            spine_model = mssm.MassSpringSpineModel(self.model_constants, sine_amplitudes[i], self.natural_frequency)
            sol, dri = spine_model.solve(t_span, self.y0, t_eval)
            dri_values.append(dri)

        plt.figure()
        plt.plot(sine_amplitudes, dri_values)
        plt.xlabel('Sinusoidal amplitude [Unit?]')
        plt.ylabel('Dynamic Response Index')
        plt.legend()
        plt.grid(True)
        plt.show()




import constants_handler
import result_analyser
import numpy as np

model_constants = constants_handler.CushionMDOFModel5(1.6)
result_analyser = result_analyser.MSSMAnalyser(model_constants)

t_span = [0, 20]

# "sinusoidal", sine_amplitude=10, sine_hertz=5
# "impulsive", impulse_amplitude=10, impulse_peak=1, eps=1e-3

#result_analyser.displacement(True, t_span, t_eval, "sinusoidal", sine_amplitude=20, sine_hertz=1)
#result_analyser.resonance(t_span, t_eval, sine_amplitude=10)

damping_ratios = [0, 0.5, 1.6]
sine_amplitudes = np.linspace(1, 100, 20)
#result_analyser.amplitude_max_displacements_sine(damping_ratios, t_span, sine_amplitudes, 5)

# try more values for the hertz parameter!!!
sine_hertz_values = np.linspace(1, 10, 50)
result_analyser.frequency_max_displacement_sine(damping_ratios, t_span, sine_hertz_values, sine_amplitude=10)

t_span = [0, 3]
#result_analyser.frequency_head_displacement_sine(t_span, [1, 3, 5, 7], 20)



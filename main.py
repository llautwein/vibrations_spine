import constants_handler
import result_analyser
import numpy as np

model_constants = constants_handler.CushionMDOFModel5(1.6)
result_analyser = result_analyser.MSSMAnalyser(model_constants)

t_span = [0, 10]

# "sinusoidal", sine_amplitude=10, sine_hertz=5
# "impulsive", impulse_amplitude=10, impulse_peak=1, eps=1e-3

#result_analyser.displacement(False, t_span, "sinusoidal", sine_amplitude=10, sine_hertz=8.4)
#result_analyser.resonance(t_span, sine_amplitude=10)

damping_ratios = [0.0, 1.6, 3.2]

sine_hertz_values = np.linspace(1, 6, 50)
result_analyser.frequency_max_displacement_sine(damping_ratios, t_span, sine_hertz_values, sine_amplitude=10)

sine_amplitudes = np.linspace(1, 20, 20)
#result_analyser.amplitude_max_displacements_sine(damping_ratios, t_span, sine_amplitudes, 1.41)

t_span = [0, 5]
#result_analyser.time_head_displacement_sine(t_span, [1.41, 3, 5], 10)

impulse_amplitudes = np.linspace(1, 20, 20)
#result_analyser.amplitude_max_displacements_impulsive(damping_ratios, t_span, impulse_amplitudes, 1)

t_span = [0, 5]
#result_analyser.time_head_displacement_impulsive(t_span, [1, 10, 20], 1)



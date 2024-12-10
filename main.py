import constants_handler
import result_analyser
import numpy as np

model_constants = constants_handler.MDOFModel()
result_analyser = result_analyser.MSSMAnalyser(model_constants)

t_span = (0, 100)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

result_analyser.displacement(t_span, t_eval, "sinusoidal", sine_amplitude=100, sine_hertz=5)
#result_analyser.resonance(t_span, t_eval, sine_amplitude=100)
result_analyser.amplitude_dri(t_span, t_eval, np.linspace(1, 100, 20))




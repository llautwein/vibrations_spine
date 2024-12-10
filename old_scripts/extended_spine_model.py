import numpy as np
import visualiser
import mass_spring_spine_model as hb
import constants_handler

# Weight of one vertebra in this section of the spine
# the sacrum and coccyx consists of 9 fused vertebra which are assumed to weigh 10 grams each
head_weight = 5
cervical_weight = 0.0063
thoracic_weight = 0.0087
lumbar_weight = 0.179
sacrum_weight = 0.09

mass_head = [head_weight]
mass_cervical_spine = [cervical_weight for i in range(7)]
mass_thoracic_spine = [thoracic_weight for i in range(12)]
mass_lumbar_spine = [lumbar_weight for i in range(5)]
mass_sacrum_spine = [sacrum_weight]

masses = mass_sacrum_spine + mass_lumbar_spine + mass_thoracic_spine + mass_cervical_spine + mass_head

# corresponding spring constants
k_head = 4805
k_cervical = 6
k_thoracic = 8.4
k_lumbar = 17.2
k_sacrum = 86.5

spring_constants_head = [k_head]
spring_constants_cervical_spine = [k_cervical for i in range(7)]
spring_constants_thoracic_spine = [k_thoracic for i in range(12)]
spring_constants_lumbar_spine = [k_lumbar for i in range(5)]
spring_constants_sacrum_spine = [k_sacrum]

spring_constants = (spring_constants_sacrum_spine + spring_constants_lumbar_spine + spring_constants_thoracic_spine +
                    spring_constants_cervical_spine + spring_constants_head)

# corresponding damping coefficients
c_head = 69.44
c_cervical = 0.09
c_thoracic = 0.12
c_lumbar = 0.25
c_sacrum = 1.25

damping_head = [c_head]
damping_cervical_spine = [c_cervical for i in range(7)]
damping_thoracic_spine = [c_thoracic for i in range(12)]
damping_lumbar_spine = [c_lumbar for i in range(5)]
damping_sacrum_spine = [c_sacrum]

damping_coefficients = (damping_sacrum_spine + damping_lumbar_spine + damping_thoracic_spine +
                        damping_cervical_spine + damping_head)

# amplitude, frequency
A = 10
hertz = 4
omega = 2*np.pi*hertz
t_span = (0, 100)
t_eval = np.linspace(t_span[0], t_span[1], 1000)

constants_handler = constants_handler.MDOFModel()
model = hb.HumanBodyChainModel(constants_handler, 1, 1)
#visualiser = visualiser.Visualiser()
#visualiser.plot_displacements(masses, spring_constants, damping_coefficients, A, omega, t_span, t_eval)


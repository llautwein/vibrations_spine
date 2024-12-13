import numpy as np


class ConstantsHandler:
    """
    This class summarises all the constants needed for the respective human spine model, i.e. the masses,
    spring constants and damping coefficients.
    The class consists only of the constructor, which defines the constants.
    Subclasses are used for the different models.
    """

    def __init__(self):
        pass


class test(ConstantsHandler):

    def __init__(self):
        super().__init__()
        self.m = [34.51, 34.51, 34.51, 34.51]
        self.k = [9.66e4, 9.66e4, 9.66e4, 9.66e4]
        self.c = [818.1, 818.1, 818.1, 818.1]


class SDOFModel(ConstantsHandler):
    """
    Single degree of freedom model (one mass one spring)
    """

    def __init__(self):
        super().__init__()
        self.m = [34.51]
        self.k = [9.66e4]
        self.c = [818.1]


class MDOFModel26(ConstantsHandler):
    """
    Models the human spine with multiple degrees of freedom with 26 masses:
    -> 24 vertebrae correspond to lumbar, thoracic and cervical spine.
    The sacrum and coccyx consists of 9 vertebrae which are fused together. Therefore, they are assumed to be just
    one bigger mass. Similarly, the head is assumed to be another big mass attached to the end of the spine.
    In this case, there is no seat considered. Thus, the force is directly exerted on the sacrum with no additional
    damping.
    Natural frequency of the human spine is assumed to be 5 Hz, the damping ratio is 0.224.
    """
    def __init__(self):
        super().__init__()
        self.omega_n = 5
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

        self.m = mass_sacrum_spine + mass_lumbar_spine + mass_thoracic_spine + mass_cervical_spine + mass_head

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

        self.k = (spring_constants_sacrum_spine + spring_constants_lumbar_spine + spring_constants_thoracic_spine +
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

        self.c = (damping_sacrum_spine + damping_lumbar_spine + damping_thoracic_spine +
                  damping_cervical_spine + damping_head)


class MDOFModel5(ConstantsHandler):

    def __init__(self):
        super().__init__()
        self.m = [10, 25, 20, 4, 5]
        self.k = [9860, 24649, 19719, 3943, 4805]
        self.c = [141, 352, 281, 56, 70]


class CushionMDOFModel26(MDOFModel26):
    """
    Models the effect of further damping with a seat cushion by adding one more mass below the spine
    which is modelled by the MDOF model from above. The mass and spring constant of the cushion are
    taken from literature while we vary the damping coefficient based on the damping ratio.
    """

    def __init__(self, cushion_damping_ratio):
        super().__init__()
        m_cushion = 3
        k_cushion = 20000
        c_cushion = 2 * cushion_damping_ratio * np.sqrt(m_cushion * k_cushion)
        self.m = [m_cushion] + self.m
        self.k = [k_cushion] + self.k
        self.c = [c_cushion] + self.c


class CushionMDOFModel5(MDOFModel5):
    """
    Models the effect of further damping with a seat cushion by adding one more mass below the spine
    which is modelled by the MDOF model from above. The mass and spring constant of the cushion are
    taken from literature while we vary the damping coefficient based on the damping ratio.
    """

    def __init__(self, cushion_damping_ratio):
        super().__init__()
        m_cushion = 3
        k_cushion = 20000
        c_cushion = 2 * cushion_damping_ratio * np.sqrt(m_cushion * k_cushion)
        self.m = [m_cushion] + self.m
        self.k = [k_cushion] + self.k
        self.c = [c_cushion] + self.c


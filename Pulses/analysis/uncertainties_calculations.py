import numpy as np
from uncertainties import ufloat

# Uncertainties for the transmission line

delay = np.array([ufloat(151, 0.05),
                  ufloat(132, 0.05),
                  ufloat(116, 0.05),
                  ufloat(98, 0.05),
                  ufloat(76, 0.05),
                  ufloat(62, 0.05),
                  ufloat(42, 0.05),
                  ufloat(22, 0.05)])

units = np.array([41, 36, 31, 26, 21, 16, 11, 6])

delay_per_unit = delay / units
print(delay_per_unit.mean())

# Uncertainties for the coaxial cable



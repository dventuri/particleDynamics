"""
Calculation of solids mass flow inlet for the riser simulation case of:
CARLOS VARAS, A. E.; PETERS, E. A. J. F.; KUIPERS, J. A. M. CFD-DEM
simulations and experimental validation of clustering phenomena and riser
hydrodynamics. "Chemical Engineering Science", 169, 246-258, 2017.
"""
import numpy as np

#Solids mass flux
Gs = 32 #kg/(m²s)

#Area of downcomer (estimated 2" comercial tube)
Dd = 2*0.0254        #inches to meters
Ad = np.pi*D**2/4    #m²

#Solids mass flow rate
Rs = Gs*Ad

#Calculate solids mass inlet in "eta" (kg_part/kg_air)
U = 6.74        #fluid inlet velocity (m/s)
Ai = 0.006*0.07 #fluid inlet area (m²)
rhof = 1.2      #fluid density (kg/m³)

eta = Rs/(rhof*U*Ai)
print(eta)
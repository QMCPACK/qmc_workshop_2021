#! /usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

# Load the data
d = np.loadtxt(sys.argv[1])

# Unpack lattice constant and energy columns
a = d[:,0]
E = d[:,1]

# Fit 4th order polynomial to data
p = np.polyfit(a,E,4)

# Evalute interpolation points
ai = np.linspace(a.min(),a.max(),2000)
Ei = np.polyval(p,ai)

# Determine approximate equilibrium lattice constant
a_eqm = ai[Ei.argmin()]

# Print lattice constant
print('\nEquilibrium lattice constant: {:6.4f} A'.format(a_eqm))

# Plot data and equation of state fit
plt.figure(tight_layout=True)
plt.plot(2*[a_eqm],[Ei.min(),Ei.max()],'k--',lw=2,label='Eqm. Lattice')
plt.plot(ai,Ei,'r-',lw=2,label='Quartic fit')
plt.plot(a,E,'bo',label='PBE Energy')
plt.xlabel('Lattice parameter $a$ ($\AA{}$)',fontsize=16)
plt.ylabel('PBE Energy per f.u. (Ry)',fontsize=16)
plt.title('PBE Equation of State of Diamond',fontsize=16)
plt.legend(fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

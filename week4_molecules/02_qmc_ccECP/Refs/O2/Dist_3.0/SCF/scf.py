
#! /usr/bin/env python3

import numpy as np
from numpy import array

### generated pyscfimport text ###
from pyscf import df, scf, dft
### end generated pyscfimport text ###





### generated system text ###
from pyscf import gto as gto_loc
mol = gto_loc.Mole()
mol.verbose  = 5
mol.atom     = '''
               O    0.00000000   0.00000000   0.00000000
               O    0.00000000   0.00000000   3.00000000
               '''
mol.basis    = 'ccecp-ccpvtz'
mol.unit     = 'A'
mol.ecp      = 'ccecp'
mol.charge   = 0
mol.spin     = 2
mol.symmetry = False
mol.build()
### end generated system text ###




### generated calculation text ###
mf = scf.ROKS(mol).density_fit()
mf.max_cycle=200
mf.level_shift=0.0
mf.xc          = 'SCAN'
mf.tol         = '1e-10'
e_scf = mf.kernel()
### end generated calculation text ###



### generated conversion text ###
from PyscfToQmcpack import savetoqmcpack
savetoqmcpack(mol,mf,'scf')
### end generated conversion text ###


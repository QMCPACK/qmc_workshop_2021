from pyscf import scf

# Nexus expands this with Mole info

### generated system text ###
from pyscf import gto as gto_loc
mol = gto_loc.Mole()
mol.atom     = '''
               Li   0.00000000   0.00000000   0.00000000
               H    1.59490000   0.00000000   0.00000000
               '''
mol.basis    = 'ccecp-ccpvqz'
mol.unit     = 'A'
mol.ecp      = 'ccecp'
mol.charge   = 0
mol.spin     = 0
mol.symmetry = True
mol.build()
### end generated system text ###



mf = scf.RHF(mol)
mf.kernel()

### generated conversion text ###
from PyscfToQmcpack import savetoqmcpack
savetoqmcpack(mol,mf,'scf')
### end generated conversion text ###


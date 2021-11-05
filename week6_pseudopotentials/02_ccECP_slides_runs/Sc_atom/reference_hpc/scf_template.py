#!/usr/bin/env python3

import sys, os
from pyscf import scf, gto
import numpy as np
from urllib.request import urlretrieve

### Set the current working directory
cwd = os.getcwd()
pplib = "http://pseudopotentiallibrary.org/recipes"
pptype = "ccECP"

### Retrieve basis and ECP files from pseudopotentiallibrary.org
atom1 = "Sc"
bastype1 = "cc-pVTZ"
basfile1 = "{0}.{1}.nwchem".format(atom1,bastype1)
ecpfile1 = "{0}.{1}.nwchem".format(atom1,pptype)
xmlfile1 = "{0}.{1}.xml".format(atom1,pptype)
urlretrieve("{0}/{1}/{2}/{3}".format(pplib,atom1,pptype,basfile1), filename=basfile1)
urlretrieve("{0}/{1}/{2}/{3}".format(pplib,atom1,pptype,ecpfile1), filename=ecpfile1)
urlretrieve("{0}/{1}/{2}/{3}".format(pplib,atom1,pptype,xmlfile1), filename=xmlfile1)

###~~~~ Build the molecule ~~~~

# Nexus expands this with Mole info
$system

with open(os.path.join(cwd,basfile1)) as f:
    bas1 = f.read()
with open(os.path.join(cwd,ecpfile1)) as f:
    ecp1 = f.read()
mol.basis = {atom1: gto.basis.parse(bas1)} 
mol.ecp = {atom1: gto.basis.parse_ecp(ecp1)}
mol.build()

#~~~Run HF on molecule~~~~
mf = scf.ROHF(mol)
mf.irrep_nelec = {
'Ag' : (3,2),   # s, dz^2, dx^2-y^2
'B3u': (1,1),   # x    1
'B1u': (1,1),   # z    0
'B2u': (1,1),   # y   -1
'B2g': (0,0),   # xz   1
'B3g': (0,0),   # yz  -1
'B1g': (0,0),   # xy  -2
'Au' : (0,0)    # xyz  
}
mf.max_cycle=100
mf.chkfile='scf.chkfile'
en=mf.kernel()
mf.analyze()


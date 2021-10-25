#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import generate_physical_system
from nexus import generate_pyscf

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()


settings(
    results    = '',
    sleep      = 3,
    machine    = 'ws'+str(cores),
    )

system = generate_physical_system(
    structure = 'Be2.xyz',            # Be2 geometry located in the Be2.xyz file
    )

# perform Hartree Fock in all electron and a cc-pvtz basis set
scf = generate_pyscf(
    identifier = 'scf',                          # log output goes to scf.out
    path       = 'Be2/cc-pvtz/HF/SCF',           # directory to run in
    job        = job(serial=True,app='python3'), # pyscf must run serially         
    system     = system,
    mole       = obj(                            # used to make Mole() inputs
        basis    = 'cc-pvtz', 
        symmetry = True,                         
        verbose  = 5,
        ),
    calculation = obj(
        method      = 'ROHF',                    # Restricted Orbital Hartree Fock
        df_fitting  = True,                      # Density fitting
        max_cycle   = 200,                       # Max SCF cycles
        level_shift = 0.0,                       # Mixing orbitals for convergence
        tol         = '1e-10',                   # Accuracy needed for convergence
        ),
    save_qmc   = True ,                          # Save the orbital to QMCPACK format
    )

run_project()

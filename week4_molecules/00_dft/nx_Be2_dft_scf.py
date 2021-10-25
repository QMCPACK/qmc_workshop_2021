#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
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

XC=["LDA","PBE","PBE0","SCAN"]                  #Loop around multiple XC functionals
MyBasis=["cc-pvdz","cc-pvtz","cc-pvqz"]       #Loop around multiple basis sets  
for x in XC:
    for y in MyBasis:
        # perform DFT 
        scf = generate_pyscf(
            identifier = 'scf',                         # log output goes to scf.out
            path       = 'Be2/'+y+'/'+x+'/SCF',         # directory to run in
            job        = job(serial=True,app='python3'),# pyscf must run serially         
            system     = system,
            mole       = obj(                           # used to make Mole() inputs
                basis    = y, 
                symmetry = True,
                verbose  = 5,
                ),
            calculation = obj(
                method      = 'ROKS',                   # Restricted Orbital Kohn Sham
                df_fitting  = True,                     # Density fitting
                max_cycle   = 200,                      # Max SCF cycles
                level_shift = 0.0,                      # Mixing orbitals for convergence
                tol         = '1e-10',                  # Accuracy needed for convergence
                xc          = x,                        # Exchange and correlation functional                                     
                ),                                     
            save_qmc   = True ,                         # Save the orbital to QMCPACK format
            )

for y in MyBasis:
    # perform Hartree Fock!
    scf = generate_pyscf(
        identifier = 'scf',                             # log output goes to scf.out
        path       = 'Be2/'+y+'/HF/SCF',                # directory to run in
        job        = job(serial=True,app='python3'),    # pyscf must run serially         
        system     = system,
        mole       = obj(                               # used to make Mole() inputs
            basis    = y, 
            symmetry = True,
            verbose  = 5,
            ),
        calculation = obj(
            method      = 'ROHF',                       # Restricted Orbital Hartree Fock
            df_fitting  = True,                         # Density fitting
            max_cycle   = 200,                          # Max SCF cycles
            level_shift = 0.0,                          # Mixing orbitals for convergence
            tol         = '1e-10',                      # Accuracy needed for convergence
            ),                                                                                
        save_qmc        = True ,                        # Save the orbital to QMCPACK format
        )

run_project()

#! /usr/bin/env python3

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()

# Import Nexus functions
from nexus import settings,job,run_project
from nexus import generate_physical_system
from nexus import generate_pwscf

# User settings
settings(
    pseudo_dir = '../pseudopotentials', # Pseudopotential directory
    results    = '',                    # Don't store results separately
    sleep      = 3,                     # Workflow polling frequency (s)
    machine    = 'ws'+str(cores),       # Executing on simple workstation
    )

# Equilibrium lattice constant of diamond (Angstrom)
a_eqm = 3.57

# Calculate diamond equation of state (energy vs. lattice constant)
for scale in [.85,.90,.95,1.00,1.05,1.10,1.15]:

    # Rescaled lattice constant for calculation
    a = scale*a_eqm

    # Details of the physical system
    system = generate_physical_system(
        units = 'A',                  # Angstrom units
        axes  = [[a/2, a/2,   0],     # Cell axes
                 [  0, a/2, a/2],
                 [a/2,   0, a/2]],
        elem  = ['C','C'],            # Element names
        posu  = [[0.00, 0.00, 0.00],  # Element positions (crystal units)
                 [0.25, 0.25, 0.25]],
        C     = 4,                    # Pseudpotential valence charge
        )

    # PBE calculation with Quantum Espresso
    scf = generate_pwscf(
        identifier   = 'scf',                      # In/out file prefix
        path         = 'a_{:6.4f}'.format(a),      # Run directory
        job          = job(cores=cores,app='pw.x'),# Job details
        input_type   = 'generic',                  # QE inputs below
        calculation  = 'scf',                      # SCF calculation
        input_dft    = 'pbe',                      # PBE functional
        ecutwfc      = 200,                        # PW energy cutoff (Ry)
        conv_thr     = 1e-8,                       # SCF conv threshold (Ry)
        system       = system,                     # System from above
        pseudos      = ['C.ccECP.upf'],            # Pseudopotential files
        kgrid        = (4,4,4),                    # M.P. k-point grid
        kshift       = (0,0,0),                    # M.P. grid shift
        )

#end for

# Execute the workflow
run_project()

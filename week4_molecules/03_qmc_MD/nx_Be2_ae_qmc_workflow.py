#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system
from nexus import generate_convert4qmc
from nexus import generate_cusp_correction
from nexus import generate_qmcpack

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()


settings(
    results    = '',
    sleep      = 3,
    machine    = 'ws'+str(cores),
    )

system = generate_physical_system(
    structure = 'Be2.xyz',  # Be2 atomic structure
    )



# convert orbitals to QMCPACK format
c4q = generate_convert4qmc(
    identifier   = 'c4q',
    path         = 'Be2/QP',
    job          = job(cores=1),
    add_cusp      = True, 
    multidet    = 'QP.h5', 
    orbitals    = 'QP.h5',
    )

# calculate cusp correction
cc = generate_cusp_correction(
    identifier   = 'cusp',
    path         = 'Be2/QP2',
    job          = job(cores=4),
    system       = system,
    dependencies = (c4q,'orbitals'),
    )

# collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'), # pyscf changes particle positions
           (c4q,'orbitals' ),
           (cc,'cuspcorr' )]


# optimize 2-body Jastrow
optJ2 = generate_qmcpack(
          identifier        = 'opt',
          path              = 'Be2/optJ2_msd',         # directory to run in
          job               = job(cores=cores),
          system            = system,
          J2                = True,         # 2-body B-spline Jastrow
          J1_rcut           = 6.0,          # 6 Bohr cutoff for J1
          J2_rcut           = 8.0,          # 8 Bohr cutoff for J2
          seed              = 42,           # Fix the seed (lab only)
          qmc               = 'opt',        # Wavefunction optimization run
          minmethod         = 'oneshift',   # Energy minimization
          init_cycles       = 4,            # 4 iterations allowing larger parameter changes
          cycles            = 8,            # 8 production iterations
          warmupsteps       = 10,
          blocks            = 20,
          steps             = 3,
          timestep          = 0.1,
          init_minwalkers   = 0.1,
          minwalkers        = 0.5,
          samples           = 25600,        # VMC samples per iteration
          dependencies      = orbdeps,
          )


# optimize 3-body Jastrow
optJ3 = generate_qmcpack(
          identifier        = 'opt',
          path              = 'Be2/optJ3_msd',         # directory to run in
          job               = job(cores=cores),
          system            = system,
          J3                = True,         # 3-body B-spline Jastrow
          seed              = 42,           # Fix the seed (lab only)
          qmc               = 'opt',        # Wavefunction optimization run
          minmethod         = 'oneshift',   # Energy minimization
          init_cycles       = 4,            # 4 iterations allowing larger parameter changes
          cycles            = 8,            # 8 production iterations
          warmupsteps       = 10,
          blocks            = 20,
          steps             =  5,
          timestep          = 0.1,
          init_minwalkers   = 0.1,
          minwalkers        = 0.5,
          samples           = 25600,        # VMC samples per iteration
          dependencies      = orbdeps+[(optJ2,'jastrow')],
          )

# run DMC with cusp Correction and 1,2 and 3 Body Jastrow function 
qmc = generate_qmcpack(
          identifier      = 'dmc',
          seed            = 42,
          path            = 'Be2/dmc_msd',       # directory to run in
          job             = job(cores=cores),                  # Submit with the number of cores available
          system          = system,                                                                                  
          jastrows        = [],                                                                                      
          qmc             = 'dmc',                             # dmc run
          vmc_samples     = 4096,                              # Number of Samples (selected from a VMC step)
          warmupsteps     = 50,                                # Number of Equilibration steps
          vmc_warmupsteps = 100,                                # Number of Equilibration steps
          vmc_blocks      = 800,                               # Number of VMC blocks (To generate the DMC samples) 
          vmc_steps       = 20,                                # Number of VMC steps (To generate DMC samples)
          vmc_timestep    = 0.1,                               # VMC Timestep (To Generate DMC samples)
          timestep        = 0.01,                              # DMC timestep
          timestep_factor = 0.5,                               # Reduce by 1/2
          ntimesteps      = 3,                                 # 4 times, i.e. [0.01, 0.005, 0.0025, 0.00125] timesteps
          steps           = 20,                                # start with small number for large timesteps [autocorrelation]
          blocks          = 100,                               # Number of DMC blocks
          dependencies    = orbdeps+[(optJ3,'jastrow')],       # Dependece (1B and 2B Jastrows)
          )
   
run_project()

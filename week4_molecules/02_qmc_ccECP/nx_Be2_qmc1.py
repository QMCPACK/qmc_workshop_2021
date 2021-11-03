#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system
from nexus import generate_pyscf
from nexus import generate_convert4qmc
from nexus import generate_cusp_correction
from nexus import generate_qmcpack

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()


settings(
    pseudo_dir = 'pseudopotentials',
    results    = '',
    sleep      = 3,
    machine    = 'ws'+str(cores),
    )

ppset(
    label   = 'ccecp',
    qmcpack = ['Be.ccECP.xml'],
    )

system = generate_physical_system(
    structure = 'Be2.xyz',            # Be2 geometry located in the Be2.xyz file
    Be=2,
    )

# perform DFT 
scf = generate_pyscf(
    identifier = 'scf',                         # log output goes to scf.out
    path       = 'Be2/SCF',         # directory to run in
    job        = job(serial=True,app='python3'),# pyscf must run serially         
    system     = system,
    mole       = obj(                           # used to make Mole() inputs
        basis    = 'ccecp-ccpvtz', 
        ecp      = 'ccecp',
        symmetry = True,
        verbose  = 5,
        ),
    calculation = obj(
        method      = 'ROKS',                   # Restricted Orbital Kohn Sham
        df_fitting  = True,                     # Density fitting
        max_cycle   = 200,                      # Max SCF cycles
        level_shift = 0.0,                      # Mixing orbitals for convergence
        tol         = '1e-10',                  # Accuracy needed for convergence
        xc          = 'SCAN',                        # Exchange and correlation functional                                     
        ),                                     
    save_qmc   = True ,                         # Save the orbital to QMCPACK format
    )


# convert orbitals to QMCPACK format
c4q = generate_convert4qmc(
    identifier   = 'c4q',
    path         = 'Be2/SCF',         # directory to run in
    job          = job(cores=1),
    dependencies = (scf,'orbitals'),              # Create a dependency to DFT success
    )

# collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'),                   # pyscf changes particle positions
         (c4q,'orbitals' )]


              


# optimize 2-body Jastrow
optJ2 = generate_qmcpack(
    identifier        = 'opt',
    path              = 'Be2/optJ2',         # directory to run in
    job               = job(cores=cores),
    system            = system,
    pseudos           = 'ccecp',
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
    path              = 'Be2/optJ3',         # directory to run in
    job               = job(cores=cores),
    system            = system,
    pseudos           = 'ccecp',
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
   
   

# run DMC with 1,2 and 3 Body Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'dmc',
    seed         = 42,
    path         = 'Be2/dmc_Tstep',        # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,                                                                                  
    pseudos      = 'ccecp',
    jastrows     = [],                                                                                      
    qmc          = 'dmc',                             # dmc run
    vmc_samples  = 2048,                             # Number of Samples (selected from a VMC step)
    warmupsteps  = 200,                              # Number of Equilibration steps
    vmc_blocks   = 200,                               # Number of VMC blocks (To generate the DMC samples) 
    vmc_steps    = 20,                                # Number of VMC steps (To generate DMC samples)
    vmc_timestep = 0.1,                               # VMC Timestep (To Generate DMC samples)
    timestep     = 0.03,                              # DMC timestep
    timestep_factor = 0.5,                            # Reduce by 1/2
    ntimesteps      = 4,                              # 4 times, i.e. [0.03, 0.015, 0.0075, 0.00375] timesteps
    steps           = 5,                             # start with small number for large timesteps [autocorrelation]
    blocks          = 200,                            # Number of DMC blocks
    dependencies = orbdeps+[(optJ3,'jastrow')],       # Dependece (1B 2B and 3B  Jastrows)
    )
   
run_project()
   

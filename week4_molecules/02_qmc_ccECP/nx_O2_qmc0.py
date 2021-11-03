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
    qmcpack = ['O.ccECP.xml'],
    )

system = generate_physical_system(
    units        = 'A',
    elem        = ['O','O'],
    pos         = [[0.000000, 0.000000, 0.000000],
                  [0.000000, 0.00000, 1.208]],
    O=6,
    )

# perform DFT 
scf = generate_pyscf(
    identifier = 'scf',                         # log output goes to scf.out
    path       = 'O2/Calibration/SCF',         # directory to run in
    job        = job(serial=True,app='python3'),# pyscf must run serially         
    system     = system,
    mole       = obj(                           # used to make Mole() inputs
        basis    = 'ccecp-ccpvtz', 
        ecp      = 'ccecp',
        symmetry = True,
        spin     =2,
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
    path         = 'O2/Calibration/SCF',         # directory to run in
    job          = job(cores=1),
    dependencies = (scf,'orbitals'),              # Create a dependency to DFT success
    )

# collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'),                   # pyscf changes particle positions
         (c4q,'orbitals' )]


              


# optimize 2-body Jastrow
optJ2 = generate_qmcpack(
    identifier        = 'opt',
    path              = 'O2/Calibration/optJ2',         # directory to run in
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
    path              = 'O2/Calibration/optJ3',         # directory to run in
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
    use_nonlocalpp_deriv = 'no',
    minwalkers        = 0.5,
    samples           = 256000,        # VMC samples per iteration
    dependencies      = orbdeps+[(optJ2,'jastrow')],
    )
   
   
#### VMC BLOCKS TO ASSES EFFECTS OF JASTROWS

# run VMC with no Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'O2/Calibration/vmc_NoJ',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    qmc          = 'vmc',                             # vmc run
    seed         = 42,                                # Fix the seed (lab only)          
    warmupsteps  = 30,                                # Number of Equilibration steps
    blocks       = 400,                               # Number of blocks 
    steps        =   20,                              # Number of steps to reduce autocorrelation
    timestep     = 0.1,                               # Time Step
    dependencies = orbdeps,                           # Dependece (No Jastrows)
    )

# run VMC with 1,2 Body Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'O2/Calibration/vmc_2J',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,                                                                        
    pseudos      = 'ccecp',
    jastrows     = [],                                                                            
    qmc          = 'vmc',                             # vmc run
    seed         = 42,                                # Fix the seed (lab only)          
    warmupsteps  = 30,                                # Number of Equilibration steps
    blocks       = 400,                               # Number of blocks 
    steps        =   20,                              # Number of steps to reduce autocorrelation
    timestep     = 0.1,                               # Time Step
    dependencies = orbdeps+[(optJ2,'jastrow')],       # Dependece (1B and 2B Jastrows)
    )


# run VMC with 1,2 and 3 Body Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'O2/Calibration/vmc_3J',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,                                                                        
    pseudos      = 'ccecp',
    jastrows     = [],                                                                            
    qmc          = 'vmc',                             # vmc run
    seed         = 42,                                # Fix the seed (lab only)          
    warmupsteps  = 30,                                # Number of Equilibration steps
    blocks       = 400,                               # Number of blocks 
    steps        =   20,                              # Number of steps to reduce autocorrelation
    timestep     = 0.1,                               # Time Step
    dependencies = orbdeps+[(optJ3,'jastrow')],       # Dependece (1B, 2B and 3B Jastrows)
    )


#### DMC BLOCKS TO ASSES EFFECTS OF JASTROWS

# run DMC with no Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'dmc',
    seed         = 42,
    path         = 'O2/Calibration/dmc_NoJ',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    qmc          = 'dmc',                             # dmc run
    vmc_samples  = 1024,                              # Number of Samples (selected from a VMC step)
    warmupsteps  = 50,                                # Number of Equilibration steps
    vmc_blocks   = 50,                                # Number of VMC blocks (To generate the DMC samples) 
    vmc_steps    = 20,                                # Number of VMC steps (To generate DMC samples)
    vmc_timestep = 0.1,                               # VMC Timestep (To Generate DMC samples)
    timestep     = 0.01,                              # DMC timestep
    steps        =   30,                              # Number of DMC steps to reduce autocorrelation
    blocks       =  250,                              # Number of DMC blocks
    dependencies = orbdeps,                           # Dependece (No Jastrows)
    )


# run DMC with 1,2 Body Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'dmc',
    seed         = 42,
    path         = 'O2/Calibration/dmc_2J',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,                                                                                  
    pseudos      = 'ccecp',
    jastrows     = [],                                                                                      
    qmc          = 'dmc',                             # dmc run
    vmc_samples  = 1024,                              # Number of Samples (selected from a VMC step)
    warmupsteps  = 50,                                # Number of Equilibration steps
    vmc_blocks   = 50,                                # Number of VMC blocks (To generate the DMC samples) 
    vmc_steps    = 20,                                # Number of VMC steps (To generate DMC samples)
    vmc_timestep = 0.1,                               # VMC Timestep (To Generate DMC samples)
    timestep     = 0.01,                              # DMC timestep
    steps        =   30,                              # Number of DMC steps to reduce autocorrelation
    blocks       =  250,                              # Number of DMC blocks
    dependencies = orbdeps+[(optJ2,'jastrow')],       # Dependece (1B and 2B Jastrows)
  )


# run DMC with 1,2 and 3 Body Jastrow function 
qmc = generate_qmcpack(
    identifier   = 'dmc',
    seed         = 42,
    path         = 'O2/Calibration/dmc_3J',         # directory to run in
    job          = job(cores=cores),                  # Submit with the number of cores available
    system       = system,                                                                                  
    pseudos      = 'ccecp',
    jastrows     = [],                                                                                      
    qmc          = 'dmc',                             # dmc run
    vmc_samples  = 1024,                              # Number of Samples (selected from a VMC step)
    warmupsteps  = 50,                                # Number of Equilibration steps
    vmc_blocks   = 50,                                # Number of VMC blocks (To generate the DMC samples) 
    vmc_steps    = 20,                                # Number of VMC steps (To generate DMC samples)
    vmc_timestep = 0.1,                               # VMC Timestep (To Generate DMC samples)
    timestep     = 0.01,                              # DMC timestep
    steps        =   30,                              # Number of DMC steps to reduce autocorrelation
    blocks       =  250,                              # Number of DMC blocks
    dependencies = orbdeps+[(optJ3,'jastrow')],       # Dependece (1B and 2B Jastrows)
    )
   
run_project()
   

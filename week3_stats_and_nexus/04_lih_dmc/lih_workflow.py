#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system
from nexus import generate_pyscf
from nexus import generate_convert4qmc
from nexus import generate_qmcpack

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()


settings(
    pseudo_dir = '../pseudopotentials',
    results    = '',
    sleep      = 3,
    machine    = 'ws'+str(cores),
    )

ppset(
    label   = 'ccecp',
    qmcpack = ['Li.ccECP.xml','H.ccECP.xml'],
    )

system = generate_physical_system(
    structure = 'LiH.xyz',  # LiH atomic structure
    Li        = 1,          # Li pseudo Zeff
    H         = 1,          # H pseudo Zeff
    )

# Perform Hartree-Fock
scf = generate_pyscf(
    identifier = 'scf',               # Log output goes to scf.out
    path       = 'LiH/hf',            # Directory to run in
    job        = job(serial=True,app='python3'), 
    template   = './scf_template.py', # PySCF template file
    system     = system,
    mole       = obj(                 # Used to make Mole() inputs
        ecp      = 'ccecp',
        basis    = 'ccecp-ccpvqz',
        symmetry = True,
        ),
    save_qmc   = True,                # Save wfn data for qmcpack
    )

# Convert orbitals to QMCPACK format
c4q = generate_convert4qmc(
    identifier   = 'c4q',
    path         = 'LiH/hf',
    job          = job(cores=1),
    no_jastrow   = True,
    dependencies = (scf,'orbitals'),
    )

# Collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'), # pyscf changes particle positions
           (c4q,'orbitals' )]

# Optimize the Jastrow factor
opt = generate_qmcpack(
    identifier   = 'opt',
    path         = 'LiH/opt',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    J2           = True,         # 2-body B-spline Jastrow
    J1_rcut      = 6.0,          # 6 Bohr cutoff for J1
    J2_rcut      = 8.0,          # 8 Bohr cutoff for J2
    seed         = 42,           # Fix the seed (lab only)
    qmc          = 'opt',        # Wavefunction optimization run
    minmethod    = 'oneshift',   # Energy minimization
    init_cycles  = 4,            # 4 iterations allowing larger parameter changes
    cycles       = 8,            # 8 production iterations
    samples      = 25600,        # VMC samples per iteration
    dependencies = orbdeps,
    )


# Lab: first DMC calculation
qmc = generate_qmcpack(
    identifier    = 'dmc',
    path          = 'LiH/dmc',
    job           = job(cores=cores),
    system        = system,
    pseudos       = 'ccecp',
    jastrows      = [],
    seed          = 42,       # Fix the seed (lab only)
    qmc           = 'dmc',    # DMC run
    vmc_samples   = 1024,     # DMC walker population sampled from VMC
    vmc_blocks    = 200,      
    vmc_steps     = 20,
    vmc_timestep  = 0.3,
    eq_dmc        = True,     # Add DMC equilibration
    eq_blocks     = 30,       # Use a small number of blocks
    eq_steps      = 10,      
    eq_timestep   = 0.02,     # Use a larger timestep
    blocks        = 1000,     # Large number of blocks for production
    steps         = 10,       # 10 steps/block averages out some autocorr time
    timestep      = 0.01,     # Smaller production timestep 
    nonlocalmoves = True,     # Use T-moves scheme w/ non-local pseudopotentials
    dependencies  = orbdeps+[(opt,'jastrow')],
    )

# Lab: DMC timestep extrapolation
qmc = generate_qmcpack(
    identifier      = 'dmc',
    path            = 'LiH/dmc_textrap',
    job             = job(cores=cores),
    system          = system,
    pseudos         = 'ccecp',
    jastrows        = [],
    seed            = 42,       # Fix the seed (lab only)
    qmc             = 'dmc',    # DMC run
    vmc_samples     = 1024,     # Initial DMC population from VMC
    vmc_blocks      = 200,
    vmc_steps       = 20,
    vmc_timestep    = 0.3,
    timestep        = 0.04,     # Start with 0.04/Ha timestep
    timestep_factor = 0.5,      # Reduce by 1/2
    ntimesteps      = 3,        # 3 times, i.e. [0.04, 0.02, 0.01] timesteps
    blocks          = 1000,     # Use 1000 blocks
    steps           = 4,        # Start w/ few steps, increase for smaller timesteps 
    nonlocalmoves   = True,     # Use T-moves scheme w/ non-local pseudopotentials
    dependencies    = orbdeps+[(opt,'jastrow')],
    )

# Lab: DMC population control bias
qmc = generate_qmcpack(
    identifier    = 'dmc',
    path          = 'LiH/dmc_pop_256',
    job           = job(cores=cores),
    system        = system,
    pseudos       = 'ccecp',
    jastrows      = [],
    seed          = 42,       # Fix the seed (lab only)
    qmc           = 'dmc',    # DMC run
    vmc_blocks    = 200,      # Same as first DMC run
    vmc_steps     = 20,
    vmc_timestep  = 0.3,
    vmc_samples   = 256,      # Except with smaller population
    eq_dmc        = True,     
    eq_blocks     = 30,
    eq_steps      = 10,
    eq_timestep   = 0.02,
    blocks        = 1000,
    steps         = 40,       # Steps adjusted to keep errorbar constant
    timestep      = 0.01,
    nonlocalmoves = True,
    dependencies  = orbdeps+[(opt,'jastrow')],
    )


run_project()

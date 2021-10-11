#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system
from nexus import generate_pyscf
from nexus import generate_convert4qmc
from nexus import generate_qmcpack,read_input,vmc

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


# Lab: estimate VMC energy equilibration, mean, variance, and errorbar
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'LiH/vmc_hf',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    qmc          = 'vmc',             # VMC run
    seed         = 42,                # Fix the seed (lab only)
    warmupsteps  = 0,
    blocks       = 200,
    steps        = 3,
    timestep     = 0.1,
    dependencies = orbdeps,
    )


# Lab: estimate VMC autocorrelation time
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'LiH/vmc_ac',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = read_input('opt.J2.xml',format='qmcpack').get('jastrows'),
    seed         = 42,                # Fix the seed (lab only)
    calculations = 9*[                # Perform 9 VMC calculations in sequence
        vmc(warmupsteps  = 20,
            blocks       = 200,
            steps        = 3,
            timestep     = 0.1,
            )],
    dependencies = orbdeps,
    )


# Lab: obtain more precise estimates via the Central Limit Theorem
qmc = generate_qmcpack(
    identifier   = 'vmc_1x',
    path         = 'LiH/vmc_clt',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = read_input('opt.J2.xml',format='qmcpack').get('jastrows'),
    qmc          = 'vmc',             # VMC run
    seed         = 42,                # Fix the seed (lab only)
    warmupsteps  = 20,
    blocks       = 400,
    steps        = 5,
    timestep     = 0.3,
    dependencies = orbdeps,
    )

qmc = generate_qmcpack(
    identifier   = 'vmc_9x',
    path         = 'LiH/vmc_clt',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = read_input('opt.J2.xml',format='qmcpack').get('jastrows'),
    qmc          = 'vmc',             # VMC run
    seed         = 42,                # Fix the seed (lab only)
    warmupsteps  = 20,
    blocks       = 3600,
    steps        = 5,
    timestep     = 0.3,
    dependencies = orbdeps,
    )


run_project()

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
    qmcpack = ['H.ccECP.xml','O.ccECP.xml'],
    )

system = generate_physical_system(
    structure = 'H2O.xyz',  # LiH atomic structure
    H         = 1,          # H pseudo Zeff
    O         = 6,          # O pseudo Zeff
    )

# perform Hartree-Fock
scf = generate_pyscf(
    identifier = 'scf',               # log output goes to scf.out
    path       = 'H2O/hf',            # directory to run in
    job        = job(serial=True,app='python3'), 
    template   = './scf_template.py', # pyscf template file
    system     = system,
    mole       = obj(                 # used to make Mole() inputs
        ecp      = 'ccecp',
        basis    = 'ccecp-ccpvqz',
        symmetry = True,
        ),
    save_qmc   = True,                # save wfn data for qmcpack
    )

# convert orbitals to QMCPACK format
c4q = generate_convert4qmc(
    identifier   = 'c4q',
    path         = 'H2O/hf',
    job          = job(cores=1),
    no_jastrow   = True,
    hdf5         = True,              # use hdf5 format
    dependencies = (scf,'orbitals'),
    )

# collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'), # pyscf changes particle positions
           (c4q,'orbitals' )]


# run VMC with HF wavefunction
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'H2O/vmc_hf',
    job          = job(cores=2),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    qmc          = 'vmc',             # vmc run
    seed         = 42,
    warmupsteps  = 0,
    blocks       = 200,
    steps        =   3,
    timestep     = 0.1,
    dependencies = orbdeps,
    )


run_project()

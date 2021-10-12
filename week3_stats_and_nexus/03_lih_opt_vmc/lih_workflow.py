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

# Lab: judging wavefunction optimization
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

# Lab: obtaining the VMC ground state energy
qmc = generate_qmcpack(
    identifier   = 'vmc',
    path         = 'LiH/vmc',
    job          = job(cores=cores),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    seed         = 42,           # Fix the seed (lab only)
    qmc          = 'vmc',        # VMC run
    blocks       = 800,
    steps        = 100,
    timestep     = 0.3,
    dependencies = orbdeps+[(opt,'jastrow')],
    )

run_project()

#! /usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import ppset
from nexus import generate_physical_system
from nexus import generate_pyscf
from nexus import generate_convert4qmc
from nexus import generate_qmcpack
from nexus import vmc,dmc
from qmcpack_input import density

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
    dependencies = (scf,'orbitals'),
    )

# collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'), # pyscf changes particle positions
           (c4q,'orbitals' )]


# optimize 2-body Jastrow
optJ2 = generate_qmcpack(
    identifier      = 'opt',
    path            = 'H2O/optJ2',
    job             = job(cores=2),
    system          = system,
    pseudos         = 'ccecp',
    J2              = True,
    J2_rcut         = 8.0,
    qmc             = 'opt',          # use opt defaults
    minmethod       = 'oneshiftonly', # adjust for oneshift
    init_cycles     = 3,
    init_minwalkers = 0.1,
    cycles          = 3,
    samples         = 25600,
    dependencies    = orbdeps,
    )


# run VMC with HF wavefunction
qmc = generate_qmcpack(
    identifier   = 'dmc',
    path         = 'H2O/dmc_J2',
    job          = job(cores=4),
    system       = system,
    pseudos      = 'ccecp',
    jastrows     = [],
    estimators = [density(delta=(0.02,0.02,0.02),x_min=0,x_max=8,y_min=0,y_max=8,z_min=0,z_max=8)], # Grid spacing in bohr
    #qmc          = 'vmc',             # vmc run
    seed         = 42,
    #warmupsteps  = 0,
    #blocks       = 200,
    #steps        =   3,
    #timestep     = 0.1,
    calculations   = [
        vmc(
            warmupsteps         =           0,
            blocks              =         200,
            steps               =           3,
            substeps            =          15,
            timestep            =         0.1,
            samplesperthread    =         250, 
            ),
        dmc(
            warmupsteps         =          30,
            blocks              =         300,
            steps               =          10,
            timestep            =        0.02,
            nonlocalmoves       =        'v1',
            reconfiguration     =       False,
            ),
    ],
    dependencies = orbdeps+[(optJ2,'jastrow')],
    )


run_project()

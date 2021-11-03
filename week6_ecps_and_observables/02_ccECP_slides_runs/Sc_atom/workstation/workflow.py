#!/usr/bin/env python3

from nexus import settings,job,run_project,obj
from nexus import generate_physical_system
from nexus import generate_pyscf
from nexus import generate_convert4qmc
from nexus import generate_qmcpack,loop,linear,vmc,dmc

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()

settings(
    pseudo_dir    = 'pseudo',
    results       = '.',
    runs          = 'runs',
    status_only   = 0,
    generate_only = 0,
    sleep         = 10,		# In seconds
    machine    = 'ws'+str(cores),
    )

system = generate_physical_system(
    structure = 'geom.xyz',
    Sc         = 11,	# 11 valence electrons
    net_spin   = 1,	# 2S
    net_charge = 0,
    )

sims = []

## Perform SCF
scf = generate_pyscf(
    identifier = 'scf',	# Log output goes to scf.out
    path       = 'scf',	# Directory to run in
    job        = job(serial=True,app='python3'),
    system     = system,
    template   = 'scf_template.py',	# pyscf template file
    mole       = obj(			# used for the Mole() object
        verbose  = 4,
        symmetry = 'D2h',
        ),
    save_qmc   = True,			# save wfn data for qmcpack
    )
sims.append(scf)

###### convert orbitals to QMCPACK format
c4q = generate_convert4qmc(
    identifier   = 'c4q',
    path         = 'c4q',
    job          = job(cores=1),
    no_jastrow   = True,
    dependencies = (scf,'orbitals'),
    )
sims.append(c4q)

### collect dependencies relating to orbitals
orbdeps = [(c4q,'particles'), # pyscf changes particle positions
           (c4q,'orbitals' ),]


### Run VMC without Jastrow for sanity check
gs_noj = generate_qmcpack(
    identifier   = 'gs_noj',
    path         = 'gs_noj',
    job          = job(cores=cores),
    system       = system,
    pseudos        = ['Sc.ccECP.xml'],
    jastrows     = [],
    calculations   = [
        vmc(
            walkers     =   1,
            warmupsteps =  20,
            blocks      =   5,
            steps       =  50,
            substeps    =   2,
            timestep    = 0.7,
            ),
        ],
    dependencies = orbdeps,
    )
sims.append(gs_noj)

##### OPTIMIZATION methods
linopt1 = linear(
    energy               = 0.0,
    unreweightedvariance = 1.0,
    reweightedvariance   = 0.0,
    samples              = int(3e3),
    substeps             = 2,
    steps                = 20,
    blocks               = 20,
    nonlocalpp           = True,
    usedrift             = True,
    minmethod            = 'OneShiftOnly',
    minwalkers           = 1e-3,
    timestep             = 1.0,
    )
linopt2 = linopt1.copy()
linopt2.minwalkers = 0.10
linopt2.samples = linopt1.samples*2

linopt3 = linopt2.copy()
linopt3.unreweightedvariance = 0.0
linopt3.reweightedvariance = 0.10
linopt3.energy = 0.90
linopt3.minwalkers = 0.30
linopt3.samples = linopt2.samples*2

####### optimize 1, 2-body Jastrow
optJ12 = generate_qmcpack(
    identifier     = 'optJ12',
    path           = 'optJ12',
    job            = job(cores=cores),
    system         = system,
    J2             = True,         # 2-body B-spline Jastrow
    J1_rcut        = 12.0,         # Bohr cutoff for J1
    J2_rcut        = 12.0,         # Bohr cutoff for J2
    pseudos        = ['Sc.ccECP.xml'],
    calculations   = [
                loop(max=5, qmc=linopt1),
                loop(max=5, qmc=linopt2),
                loop(max=5, qmc=linopt3),
        ],
    dependencies = orbdeps,
    )
sims.append(optJ12)

###### optimize 3-body Jastrow
optJ123 = generate_qmcpack(
    identifier     = 'optJ123',
    path           = 'optJ123',
    job            = job(cores=cores),
    system         = system,
    J3             = True,
    J3_rcut        = 12.0,
    pseudos        = ['Sc.ccECP.xml'],
    calculations   = [
                loop(max=10, qmc=linopt3),
        ],
    dependencies   = orbdeps+[(optJ12,'jastrow')],
    )
sims.append(optJ123)

t_moves = ['no', 'v0', 'v1']
locality_run = {}

#### run DMC with QMCPACK
MY_TARGET_WALKERS = 16   # Small number for presentation purposes. Needs to be at least a few thousand walkers.

for moves in t_moves:
    name = 'qmc_' + moves

    locality_run[moves] = generate_qmcpack(
        identifier   = name,
        path         = name,
        job          = job(cores=cores),
        system       = system,
        pseudos        = ['Sc.ccECP.xml'],
        jastrows     = [],
        calculations   = [ 
            vmc(
                #walkers     =   1,
                walkers     = int(MY_TARGET_WALKERS/cores),   # Per MPI
                warmupsteps =  20,
                blocks      =   5,
                steps       =  50,
                substeps    =   2,
                timestep    = 0.5,
                ),
            dmc(targetwalkers = MY_TARGET_WALKERS,  # Total walkers
                timestep = 0.02,
                warmupsteps =  int(5/0.02),
                blocks = 5,
                steps = int(1.0/0.02),
                nonlocalmoves = moves,
                checkpoint = 5
                ),
            dmc(targetwalkers = MY_TARGET_WALKERS,  # Total walkers
                timestep = 0.01,
                warmupsteps =  int(2/0.01),
                blocks = 5,
                steps = int(1.0/0.01),
                nonlocalmoves = moves,
                checkpoint = 5
                ),
            dmc(targetwalkers = MY_TARGET_WALKERS,  # Total walkers
                timestep = 0.005,
                warmupsteps =  int(1/0.005),
                blocks = 5,
                steps = int(1.0/0.005),
                nonlocalmoves = moves,
                checkpoint = 5
                ),
            dmc(targetwalkers = MY_TARGET_WALKERS,  # Total walkers
                timestep = 0.0025,
                warmupsteps =  int(1/0.0025),
                blocks = 5,
                steps = int(1.0/0.0025),
                nonlocalmoves = moves,
                checkpoint = 5
                ),
            ],
        dependencies = orbdeps+[(optJ123,'jastrow')],
        )
    sims.append(locality_run[moves])

run_project(sims)


#! /usr/bin/env python3

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()

# Paths to executables.  *** EDIT ME ***
#pwx_bin="${HOME}/qmcpack/external_codes/quantum_espresso/6.7.0/bin/pw.x"
pwx_bin="pw.x"
#wfc_bin="${HOME}/qmcpack/external_codes/quantum_espresso/6.7.0/bin/pw2qmcpack.x"
wfc_bin="pw2qmcpack.x"
#qmc_bin="${HOME}/qmcpack/build-vanilla/bin/qmcpack_complex"
qmc_bin="qmcpack_complex"

# Import Nexus stuff
from nexus import settings,job,run_project
from nexus import generate_physical_system
from nexus import generate_pwscf
from nexus import generate_pw2qmcpack
from nexus import generate_qmcpack
from qmcpack_input import nofk,gofr

# machine settings
settings(
    pseudo_dir = './pseudos',       # Pseudopotential directory
    results    = '',                # Don't store results separately
    sleep      = 5,                 # Workflow polling frequency (sec)
    machine    = 'ws'+str(cores),   # Executing on simple workstation
    )


#
# Step 0.a) Specify the system to simulate
#           This test problem shows a sample workflow for
#           solids in which the DFT and wave function
#           generation is done in a primitive cell using
#           k-points to tile a supercell for subsequent
#           QMC calculations.
#
#           Here, we construct a primitive cell of carbon
#           diamond at ambient density.
#
a = 3.57
primcell  = generate_physical_system(
    units = 'A',                  # Angstrom units
    axes  = [[a/2, a/2,   0],     # Cell axes
             [  0, a/2, a/2],
             [a/2,   0, a/2]],
    elem  = ['C','C'],            # Element names
    posu  = [[0.00, 0.00, 0.00],  # Element positions (crystal units)
             [0.25, 0.25, 0.25]],
    C     = 4,                    # Pseudpotential valence charge
)


# 
# Step 0.b) Here we use Nexus to generate the optimal (most spherical)
#           supercell composed of 8 atoms (4x copies of prim. cell).
#
#           If you wanted to scan the number of twists required to
#           converge the total energy in this supercell, adjust kgrid.
# 
# NB: The number of twists in the supercell determines the number of kpoint
#     needed in the primcell, so a larger supercell, or a denser twistgrid
#     are both more expensive (but still very cheap compared to QMC!)
#
tiled = primcell.structure.tile_opt(4)
tiled.add_symmetrized_kmesh(kgrid=(2,2,2),kshift=(0,0,0))
supercell = generate_physical_system(structure = tiled, C=4)

#
# Step 1.) DFT calculation with Quantum ESPRESSO
#          Note that the system we specify is the primcell
#          and a very large kpoint grid. This is done in order
#          to provide a well-converged density from which we will
#          subsequently generate SPOs to be used in the QMC calculation.
#
scf = generate_pwscf(
    identifier   = 'scf',                      # In/out file prefix
    path         = 'diamond/scf',              # Run directory
    job          = job(cores=cores,
                       app=pwx_bin),           # How to run QE
    input_type   = 'generic',                  # QE inputs below
    calculation  = 'scf',                      # SCF calculation
    input_dft    = 'pbe',                      # PBE functional
    verbosity    = 'high',                     # Show eigenvalues and occupations
    ecutwfc      = 200,                        # PW energy cutoff (Ry)
    ecutrho      = 2000,                       # Density cutoff (Ry)
    nbnd         = 8,                          # Number of SPO's to calculate
    conv_thr     = 1e-10,                      # SCF conv threshold (Ry)
    system       = primcell,                   # System to calculate
    pseudos      = ['C.ccECP.upf'],            # Pseudopotential stuff
    kgrid        = (10,10,10),                 # Dense k-point grid!
    kshift       = (0,0,0),                    # k-point grid shift
)


#
# Step 2.) DFT wave function generation with Quantum ESPRESSO
#          Notice that here we do a nscf calculation using the
#          converged density from the previous scf calculation.
#          And also the kpoints we need are given by the supercell.
#
#          If you look inside the supercell object, you'll see that it
#          knows the map from prim->super cell, and so Nexus will
#          automatically do a primcell calculation with the correct kpoints
#          to tile into the corresponding supercell.
#
nscf = generate_pwscf(
    identifier   = 'nscf',                     # In/out file prefix
    path         = 'diamond/nscf',             # Run directory
    job          = job(cores=cores,
                       app=pwx_bin),           # How to run QE
    input_type   = 'generic',                  # QE inputs below
    calculation  = 'nscf',                     # SCF calculation
    input_dft    = 'pbe',                      # PBE functional
    verbosity    = 'high',                     # Show eigenvalues and occupations
    ecutwfc      = 200,                        # PW energy cutoff (Ry)
    ecutrho      = 2000,                       # Density cutoff (Ry)
    nbnd         = 8,                          # Number of SPO's to calculate
    conv_thr     = 1e-10,                      # SCF conv threshold (Ry)
    system       = supercell,                  # System to calculate
    pseudos      = ['C.ccECP.upf'],            # Pseudopotential stuff
    dependencies = (scf,'charge_density'),
)

# Finally, convert the SPO's to hdf5 format
conv = generate_pw2qmcpack(
    identifier   = 'wfconv',
    path         = 'diamond/nscf',
    job          = job(cores=cores,
                       app=wfc_bin),
    write_psir   = False,
    dependencies = (nscf,'orbitals'),
)


#
# At this point we have a QMC wavefunction that contains all the
# kpoints necessary to tile a 2-atom prim cell into a 8-atom supercell
# with the appropriate twist grid in that supercell. Now we turn to the
# QMC portion of the workflow, which uses only the supercell object.


#
# Step 3.) VMC Jastrow optimization of 1- and 2-body Jastrows
#
# NB: For this problem a 3-body Jastrow does not noticeably
#     improve the wfn. You are encouraged to verify this!
#     [ example J3 block is provided below ]
#
optJ12 = generate_qmcpack(
    identifier      = 'diaqmc',
    path            = 'diamond/optJ12',
    job             = job(cores=cores,
                          threads=cores,
                          app=qmc_bin),
    input_type      = 'basic',
    system          = supercell,    
    pseudos         = ['C.ccECP.xml'],
    twistnum        = 0,
    J1              = True,         # Add a 1-body B-spline Jastrow
    J2              = True,         # Add a 2-body B-spline Jastrow
    J1_rcut         = 3.37,         # Cutoff for J1
    J2_rcut         = 3.37,         # Cutoff for J2
    qmc             = 'opt',        # Do a wavefunction optimization
    minmethod       = 'oneshift',   # Optimization algorithm (assumes energy minimization)
    init_cycles     = 4,            # First 4 iterations allow large parameter changes
    cycles          = 10,           # 8 subsequent iterations with smaller parameter changes
    warmupsteps     = 8,            # First 8 steps are not recorded
    blocks          = 100,          # Number of blocks to write in the .scalar.dat file
    timestep        = 0.1,          # MC step size (nothing to do with time for VMC)
    init_minwalkers = 0.01,         # Smaller values -> bigger parameter change
    minwalkers      = 0.5,          # 
    samples         = 20000,        # VMC samples per iteration
    use_nonlocalpp_deriv = False,
    dependencies    = (conv,'orbitals'),
)

# Now add J3
# Actually, for this particular problem J3 doesn't do anything.
# Nevertheless, here's a sample to try in case you'd like to experiment.
# optJ123 = generate_qmcpack(
#     #block           = True,
#     identifier      = 'diaqmc',
#     path            = 'diamond/optJ123',
#     job             = job(cores=cores,
#                           threads=16,
#                           app=qmc_bin),
#     input_type      = 'basic',
#     system          = supercell,
#     pseudos         = ['C.ccECP.xml'],
#     twistnum        = 0,
#     J3              = True,         # Add a 2-body B-spline Jastrow
#     J3_rcut         = 2.00,         # Cutoff for J3
#     qmc             = 'opt',        # Do a wavefunction optimization
#     minmethod       = 'oneshift',   # Optimization algorithm (assumes energy minimization)
#     init_cycles     = 4,            # First 4 iterations allow large parameter changes
#     init_minwalkers = 0.01,         # Smaller value -> bigger parameter change
#     cycles          = 10,           # Subsequent iterations with smaller parameter changes
#     minwalkers      = 0.5,          # Larger value -> smaller parameter change
#     warmupsteps     = 4,            # First steps are not recorded
#     blocks          = 100,          # Number of blocks to write in the .scalar.dat file
#     timestep        = 0.1,          # MC step size (nothing to do with time for VMC)
#     samples         = 40000,        # VMC samples per iteration
#     use_nonlocalpp_deriv = False,   # Don't include nonlocal pseudo derivatives in optimization (this is nice to have for deep semicore states but expensive!)
#     dependencies    = [(conv,'orbitals'),
#                        (optJ12, 'jastrow')],
# )


#
# Now we are ready for production calculations with an optimized wfn.
# Below, we specify a series of VMC + DMC calculations. QMCPACK can
# run multiple twists in parallel using MPI, but on most laptops it is easier
# to run each twist in serial. So, I have provided examples of both workflows.
#


#
# Step 4.) Production DMC
#          This block will run all 4 supercell twists in parallel.
#          If you are on a small computer, you can run them individually
#          with the code block below this one.
#
# qmc = generate_qmcpack(
#     identifier      = 'dmc',
#     path            = 'diamond/dmc-paralleltwists',
#     job             = job(cores=cores,
#                           threads=cores,
#                           app=qmc_bin),
#     input_type      = 'basic',
#     system          = supercell,        
#     pseudos         = ['C.ccECP.xml'],
#     qmc             = 'dmc',
    
#     # Initial VMC stuff
#     vmc_warmupsteps = 8,      # Number of Equilibration steps
#     vmc_blocks      = 500,    # Number of VMC blocks (To generate the DMC samples) 
#     vmc_steps       = 8,      # Number of VMC steps (To generate DMC samples)
#     vmc_timestep    = 0.1,    # VMC Timestep (To Generate DMC samples)
    
#     # DMC stuff
#     timestep        = 0.02,   # DMC timestep
#     timestep_factor = 0.5,    # Reduce by 1/2
#     ntimesteps      = 3,      # 4 times, i.e. [0.01, 0.005, 0.0025, 0.00125] timesteps
#     steps           = 1,      # start with small number for large timesteps [autocorrelation]
#     blocks          = 200,    # Number of DMC blocks
#     dependencies    = [(conv,'orbitals'),
#                        (optJ12,'jastrow')],
# )


#
# Step 4.) Production DMC - SMALL COMPUTER OPTIMIZATION
#          This block will run all 4 supercell twists in serial.
#          If you are on a small computer, this might be faster.
#
for tw in range(0,4):
    qmc = generate_qmcpack(
        #block        = True,
        identifier      = 'dmc',
        path            = 'diamond/dmc/tw' + str(tw),
        job             = job(cores=cores,
                              threads=cores,
                              app=qmc_bin),
        input_type      = 'basic',
        system          = supercell,        
        twistnum        = tw,
        pseudos         = ['C.ccECP.xml'],
        qmc             = 'dmc',
        
        # Initial VMC stuff
        vmc_warmupsteps = 8,      # Number of Equilibration steps
        vmc_blocks      = 500,    # Number of VMC blocks (To generate the DMC samples) 
        vmc_steps       = 8,      # Number of VMC steps (To generate DMC samples)
        vmc_timestep    = 0.1,    # VMC Timestep (To Generate DMC samples)
        
        # DMC stuff
        timestep        = 0.02,   # DMC timestep
        timestep_factor = 0.5,    # Reduce by 1/2
        ntimesteps      = 3,      # 4 times, i.e. [0.01, 0.005, 0.0025, 0.00125] timesteps
        steps           = 1,      # start with small number for large timesteps [autocorrelation]
        blocks          = 200,    # Number of DMC blocks
        dependencies    = [(conv,'orbitals'),
                           (optJ12,'jastrow')],
    )
    
    # Execute the workflow
    run_project()
 
# End loop

# Execute the workflow - comment out if running in serial
#run_project()




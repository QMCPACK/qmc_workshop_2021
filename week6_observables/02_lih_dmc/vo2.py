#! /usr/bin/env python3

from structure import read_structure, read_cif
from nexus import generate_physical_system

# Obtain the core count of the local machine (lab only)
import os
cores = os.cpu_count()

# Paths to executables.  *** EDIT ME ***
pwx_bin='pw.x'
wfc_bin='pw2qmcpack.x'
qmc_bin='qmcpack_complex'

####################################################################
# Process crystal structure from ICSD (code 237337)                #
####################################################################
xsf_file = './structures/xsf/ICSD_CollCode237337.xsf'
cif_file = './structures/cif/ICSD_CollCode237337.cif'
if not os.path.exists(xsf_file):
    # This is a 6-atom structure
    s = read_structure(cif_file,format='cif')
    s.write(xsf_file)
    if not os.path.exists(pos_file):
        s.write(pos_file)
    #end if
#end if
####################################################################
####################################################################



####################################################################
# Define the physical system as we have seen in other labs         #
####################################################################
vo2_fm = generate_physical_system(
	structure   = s,      # structure information
	net_charge  = 0,      # charge of cell
	net_spin    = 0,      # nup-ndown in cell
	V           = 13,     # Zeff 
	O           = 6,      # Zeff 
    )
####################################################################
####################################################################



####################################################################
# Define the DFT calculation using Quantum Espresso (pwscf)        #
####################################################################
scf = generate_pwscf(
    identifier   = 'scf',                      # In/out file prefix
    path         = 'vo2_fm/scf',               # Run directory
    job          = job(cores=cores,
                       app=pwx_bin),           # How to run QE
    input_type   = 'generic',                  # QE inputs below
    calculation  = 'scf',                      # SCF calculation
    input_dft    = 'pbe',                      # PBE functional
    verbosity    = 'high',                     # Show eigenvalues and occupations
    ecutwfc      = 200,                        # PW energy cutoff (Ry)
    system       = vo2_fm,                     # System to calculate
    pseudos      = ['O.ccECP.upf',
                    'V.ccECP.upf'],            # Pseudopotential stuff
    starting_magnetization = {'V' : 1.0},      # Starting Magnetization
    kgrid        = (4,4,4),                    # Dense k-point grid!
    kshift       = (0,0,0),                    # k-point grid shift
)


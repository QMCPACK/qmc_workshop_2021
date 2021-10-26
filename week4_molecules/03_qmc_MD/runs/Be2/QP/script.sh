#!/bin/bash

qp_create_ezfio Be2.xyz -b cc-pvtz                  #Generating system with cc-pvTz basis set
qp_run scf Be2.ezfio >> scf.out                     #Running HF level of theory
echo "500000" > Be2.ezfio/determinants/n_det_max    #Setting max number of detemrinants to 0.5M
qp_run fci Be2.ezfio > fci0                         #running a first round of sCI
qp_run save_natorb Be.ezfio > NatOrb                #Generating natural orbitals
qp_run fci Be2.ezfio > fci                          #running a first round of sCI
qp_run print_e_conv Be2.ezfio                       # Will generate data for E(det) in Be2.ezfio.1.conv file
echo "1.000e-05" > Be2.ezfio/qmcpack/ci_threshold   # Set the truncation threshold for the Multideterminants coefficients
qp_run truncate_wf_spin  Be2.ezfio > Truncation     # Remove determinants with coeffs smaller than threshold and re-diagonalize hamiltonian
qp_run save_for_qmcpack Be2.ezfio > SaveForQmcpack  # Will generate an HDF5 file needed by nexus (QP2QMCPACK.h5) and a readable version in the redirected output
mv QP2QMCPACK.h5 QP.h5



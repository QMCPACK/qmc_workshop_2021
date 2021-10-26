Molecular Calculations with QMCPACK and Nexus
===================================================================

In this lab, you will learn how to run a diffusion Monte Carlo calculation 
for a small molecule, in this case, Be2 and O2. You will see how to choose 
a trial wavefunction, run an SCF calculation with PySCF, convert the 
wavefunction to the QMCPACK format, then run the Jastrow optimization and 
finally the DMC calculations. At each step of the workflow, we will analyze the 
data and try to understand what motivates the choice of the simulation parameters
such as time steps and number of walkers and will analyze the resulting wavefunction
through the analysis of the variance and the local energy

This lab uses the Nexus workflow 
automation system to compactly represent simulation inputs and perform the 
DFT and QMC calculations in sequence.  While the examples here are designed 
to run on a laptop, Nexus can be used on computational resources ranging from 
desktop machines to clusters and supercomputers, enabling production QMC 
calculations to be performed from within a uniform environment.


There are four main examples in the lab, as described below:

**Example 1: Generating The determinant part of the trial wavefunction : DFT study of te beryllium dimer**

* Run DFT (PySCF) with different functionals and Basissets with Nexus to obtain the energy vs. method .  
* Directory: ``00_dft``

**Example 2: All electron calculation of the total energy of Be2 molecule**

* Run DFT (PySCF) and DMC (QMCPACK) with Nexus to obtain the total energy of the Be2 molecule. In the process we will learn how to:
* Correct the electron-Ion Cusp
* Set Jastrow function and assess their effect on the VMC and DMC energies and variances
* Exrapolate out the time-step error from DMC 
* Estimate the population bias for a given sample size
* Learn how to reduce the error bars through the size of the samples or the size of the DMC blocks
* Understand the effects of the fixed-node error on a DMC run starting multiple basis-sets and DFT-XC functionals 
* Directory: ``01_qmc_SD``

**Example 3: Using Core-correlated Electron Core Potentials for DMC**

* Use an ECP to evaluate only energy from valence elctrons and perform DMC calculations of the ground state total energy of Be2 and the dissociation energy of the Oxygen molecule  with Nexus.  Learn the impact of ECP on Jastrows, DMC time step and variance and ompare it to similar calculations using all electrons simulations. 
* Directory: ``03_qmc_ccECP``


**Example 4: Advanced Wavefunctions**

* Use a more advanced trial wavefunction from selected Confiuration Interaction to improve systematically the nodal surface. The generation of the wavefunction will not be covered in this workshop (see https://github.com/QMCPACK/qmcpack_workshop_2019/tree/master/day2_CIPSI for more details). 
* Directory: ``03_qmc_MD``



All directories contain scripts helping to either extract QMC data (by calling qmca command) or scripts to plot the data shown in the slides. You are encouragedto modify the scripts to meet your needs.


For more information about Nexus and QMCPACK, please consult their respective documentation:

* QMCPACK: https://qmcpack.readthedocs.io/en/develop/
* Nexus: https://nexus-workflows.readthedocs.io/en/latest/

For more information on QMC methods in general (theory and application), 
the 2001 Rev. Mod. Phys. by Foulkes et al. is essential reading:

* https://doi.org/10.1103/RevModPhys.73.33

This lab uses the ``qmca`` and ``qmc-fit`` tools for statistical data analysis.  See their respective documentation for more details:

* qmca: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmca
* qmc-fit: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmcfit

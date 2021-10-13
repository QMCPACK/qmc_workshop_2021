Statistical Analysis + Running QMC Workflows with QMCPACK and Nexus
===================================================================

In this lab, you will familiarize yourself with running VMC, wavefunction 
optimization, and DMC calculations with QMCPACK and analyzing the 
statistical results at each step.  Quantum Monte Carlo (QMC) calculations 
join several constituent calculations (most related to obtaining the trial 
wavefunction) into a computational workflows.  

This lab uses the Nexus workflow 
automation system to compactly represent simulation inputs and perform the 
DFT and QMC calculations in sequence.  While the examples here are designed 
to run on a laptop, Nexus can be used on computational resources ranging from 
desktop machines to clusters and supercomputers, enabling production QMC 
calculations to be performed from within a uniform environment.

Through the examples in this lab, you will familiarize yourself with the 
following topics in statistical analysis and QMC:

**Statistics topics:**

* Estimated mean
* Estimated variance and error-bar
* Equilibration period (a.k.a. Markov chain "Burn-in")
* Temporal autocorrelation
* Central limit theorem
* Statistical significance of energy differences
* Resampled fits

**QMC topics:**

* Orbital file format conversion
* Slater-determinant wavefunction
* Slater-Jastrow wavefunction
* Variational Monte Carlo
* Wavefunction optimization
* DMC equilibration and population dynamics
* DMC timestep extrapolation
* DMC population control bias

There are four main examples in the lab, as described below:

**Example 1: Introduction to running workflows with Nexus**

* Run DFT (Quantum Espresso) with Nexus to obtain the energy vs. volume curve for diamond.  
* Directory: ``01_diamond_eos_workflow``

**Example 2: Statistical analysis of QMC data in general**

* Run Hartree-Fock (PySCF) and VMC (QMCPACK) with Nexus to obtain the total energy of the LiH molecule.  Learn how to obtain reliable estimates of the mean and errorbar accounting for equilibration and temporal autocorrelation.  Learn how to estimate sampling needs using the central limit theorem. 
* Directory: ``02_lih_hf_vmc``

**Example 3: Wavefunction optimization**

* Optimize a Jastrow factor (QMCPACK) and run VMC with Nexus for the LiH molecule.  Use statistically correct energy differences to judge the convergence of the optimization procedure.  Obtain the VMC energy of the optimized Slater-Jastrow trial wavefunction for LiH.
* Directory: ``03_lih_opt_vmc``

**Example 4: Diffusion Monte Carlo**

* Perform DMC (QMCPACK) calculations of the ground state total energy of LiH with Nexus.  Learn about the impact of the DMC timestep on statistical equilibration, autocorrelation, and bias of the total energy.  Use resampled fits to extrapolate the ground state energy to the zero timestep limit.  Learn about DMC branching and population control bias. 
* Directory: ``04_lih_dmc``

For more information about Nexus and QMCPACK, please consult their respective documentation:

* QMCPACK: https://qmcpack.readthedocs.io/en/develop/
* Nexus: https://nexus-workflows.readthedocs.io/en/latest/

For more information on QMC methods in general (theory and application), 
the 2001 Rev. Mod. Phys. by Foulkes et al. is essential reading:

* https://doi.org/10.1103/RevModPhys.73.33

This lab uses the ``qmca`` and ``qmc-fit`` tools for statistical data analysis.  See their respective documentation for more details:

* qmca: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmca
* qmc-fit: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmcfit

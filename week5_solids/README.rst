Calculations on Solids with QMCPACK and Nexus
===================================================================

In this lab, we will study the diamond structure of carbon.
First, you will learn how to use k-points in a primitive cell to
tile a supercell using Quantum ESPRESSO and Nexus. After that, you will
learn how to optimize a Slater-Jastrow wave function. Finally, you will
perform production DMC calculations using twist-averaging to obtain a robust
estimate of the ground state energy under the fixed-node approximation.

In addition, I have included extra examples of hybrid-representation of the
wave function, and also a k-space Jastrow optimization example.

This lab uses the Nexus workflow automation system to compactly represent
simulation inputs and perform the DFT and QMC calculations in sequence.
While the examples here are designed to run on a laptop, Nexus can be used
on computational resources ranging from desktop machines to clusters and
supercomputers, enabling production QMC calculations to be performed from
within a uniform environment.

Although the calculations outlined here are at a single fixed density, you
can modify the scripts to compute an EOS by adjusting the volume and fitting
the resulting data.

NB: I have not included any examples of timestep extrapolation, population bias,
    mixed-estimator corrections, or finite size corrections.
    
All directories contain scripts helping to either extract QMC data (by calling qmca command) or scripts to plot the data shown in the slides. You are encouragedto modify the scripts to meet your needs.
The main script is "solids_example.py". However, included in the "runs/diamond_example_results" directory
are example inputs and outputs for each calculation.

For more information about Nexus and QMCPACK, please consult their respective documentation:

* QMCPACK: https://qmcpack.readthedocs.io/en/develop/
* Nexus: https://nexus-workflows.readthedocs.io/en/latest/

For more information on QMC methods in general (theory and application), 
the 2001 Rev. Mod. Phys. by Foulkes et al. is essential reading:

* https://doi.org/10.1103/RevModPhys.73.33

This lab uses the ``qmca`` and ``qmc-fit`` tools for statistical data analysis.  See their respective documentation for more details:

* qmca: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmca
* qmc-fit: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmcfit

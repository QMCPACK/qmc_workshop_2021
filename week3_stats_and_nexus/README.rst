Statistical Analysis + Running QMC Workflows with QMCPACK and Nexus
===================================================================

In this lab, you will familiarize yourself with running VMC, wavefunction 
optimization, and DMC calculations with QMCPACK and analyzing the 
statistical results at each step.  Quantum Monte Carlo (QMC) calculations 
join several constituent calculations (most related to obtaining the trial 
wavefunction) into a computational workflows.  This lab uses the Nexus workflow 
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

For more information about Nexus and QMCPACK, please consult their respective documentation:

* QMCPACK: https://qmcpack.readthedocs.io/en/develop/
* Nexus: https://nexus-workflows.readthedocs.io/en/latest/

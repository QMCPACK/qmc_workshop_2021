LiH molecule: diffusion Monte Carlo with QMCPACK
================================================

In this example, you will gain experience with projector DMC methods.
DMC is closely related to VMC.  With just the drift-diffusion 
propagator active (no branching), DMC is identical to VMC.  With 
branching, the popluation of walkers is now tied together with 
individual walkers being destroyed or replicated and the entire population 
count fluctating around an average value.  

DMC starts with a population of walkers sampled from VMC.  Beginning at 
imaginary time zero, the walker population begins to branch and the 
energy lowers exponentially in imaginary time.  Both the finite imaginary 
time step and the finite walker populations are controllable approximations 
to the idealized DMC algorithm (exact in the low timestep and high walker 
population limits).

Through this example, you will familiarize yourself with the following 
topics in statistical analysis and quantum Monte Carlo (QMC):

**Statistics topics:**

* Equilibration period (a.k.a. Markov chain "Burn-in")
* Temporal autocorrelation
* Resampled fits

**QMC topics:**

* DMC equilibration and population dynamics
* DMC timestep extrapolation
* DMC population control bias
* Ground state energy


Running the initial calculations
--------------------------------
The Nexus workflow script ``lih_workflow.py`` performs the following sequence 
of calculations:

1. Hartree-Fock calculation (see ``generate_pyscf``).
2. Conversion of PySCF orbital format to QMCPACK HDF5 file (see ``generate_convert4qmc``).
3. Jastrow optimization via energy minimization with the linear method (see ``opt = generate_qmcpack``).
4. Diffusion Monte Carlo calculation with the optimized Slater-Jastrow trial wavefunction (see the first ``qmc = generate_qmcpack``).
5. DMC with varied timestep for zero time extrapolation.
6. DMC with varied walker populations to demonstrate population control bias.

Take a minute to read through the workflow file and familiarize yourself 
with its contents.  Next, run the workflow script (this may take a few 
minutes depending on the available computational resources):

.. code-block:: bash

  >./lih_workflow.py



A first DMC calculation
-----------------------

In the workflow above, an initial DMC calculation was performed in `runs/LiH/dmc`.  The goal is to get a reliable DMC total energy with a 0.01/Ha timestep.  While this timestep is not converged for total energies, it is often sufficient for energy differences of interest (e.g. molecular binding energies, ionization potentials, formation energies of defects in solids, etc).  

First, a VMC run (series 0, ``dmc.s000.scalar.dat``) was performed to initialize the zero time DMC walker population, which has 1024 walkers. Next, DMC was performed using a larger 0.02/Ha timestep and run for a short time (30 blocks w/ 10 steps each, series 1, ``dmc.s001.scalar.dat``).  The purpose of this short DMC run with a larger timestep is to rapidly equilibrate the DMC walker population (larger timestep leads to faster equilibration).  Finally, DMC is performed with the production 0.01/Ha timestep for a long time to produce the statistical samples of interest (series 2, ``dmc.s002.scalar.dat``).
  


DMC timestep extrapolation
--------------------------


DMC population control bias
---------------------------






LiH molecule: diffusion Monte Carlo with QMCPACK
================================================

In this example, you will gain experience with projector DMC methods.

Through this example, you will familiarize yourself with the following 
topics in statistical analysis and quantum Monte Carlo (QMC):


**Statistics topics:**

* Equilibration period (a.k.a. Markov chain "Burn-in")
* Temporal autocorrelation
* Resampled fits

**QMC topics:**

* Diffusion Monte Carlo
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


DMC timestep extrapolation
--------------------------


DMC population control bias
---------------------------






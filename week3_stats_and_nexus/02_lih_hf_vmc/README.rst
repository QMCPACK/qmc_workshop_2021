LiH molecule: VMC with QMCPACK and statistical analysis
=======================================================

In this example, you will calculate the the Hartree-Fock (HF) estimate of 
the ground state energy of a simple diatomic molecule: LiH.  The HF energy 
and Slater-determinant wavefunction will first be obtained with the PySCF 
code.  Next, QMCPACK will be run using only this single determinant 
wavefunction to reproduce the HF energy, now with statistical noise. 
Through this example, you will familiarize yourself with the following 
topics in statistical analysis and quantum Monte Carlo (QMC):

**Statistics topics:**

* Estimated mean
* Estimated variance and error-bar
* Equilibration period (a.k.a. Markov chain "Burn-in")
* Temporal autocorrelation
* Central limit theorem

**QMC topics:**

* Variational Monte Carlo
* Orbital file format conversion
* Slater-determinant wavefunction
* Acceptance ratio
* Diffusion timestep
* Ground state energy


Running the initial calculations
--------------------------------
The Nexus workflow script ``lih_workflow.py`` performs the following sequence 
of calculations:

1. Hartree-Fock calculation (see ``generate_pyscf``).
2. Conversion of PySCF orbital format to QMCPACK HDF5 file (see ``generate_convert4qmc``).
3. Variational Monte Carlo calculation with the HF Slater determinant (see ``generate_qmcpack``).

Take a minute to read through the workflow file and familiarize yourself 
with its contents.  Next, run the workflow script (this may take a few 
minutes depending on the available computational resources):

.. code-block:: bash

  >./lih_workflow.py

Check the Hartree-Fock energy from PySCF:

.. code-block:: bash

  >cat runs/LiH/hf/scf.out 
  converged SCF energy = -0.749663314779369


Estimating VMC equilibration time
---------------------------------

In QMC, the random walk begins with the electrons placed in arbitrary locations 
centered on the atoms.  This initial configuration is often in a location of 
low probability according to the trial wavefunction, and therefore a number of 
Monte Carlo moves (Metropolis or Markov-chain updates) are needed to enter the 
high probability regions of electronic phase space and produce properly 
weighted statistical samples of the energy and other observables.

This initial transition period is known as the equilibration period, or 
"burn-in".  The energies produced from this initial region will bias the 
estimated mean of the energy, and therefore need to be removed.

VMC energy samples produced during the QMCPACK run are found in ``scalar.dat`` 
files.  We can plot the energy samples (i.e. the trace of the energy time 
series) with the ``qmca`` tool to manually assess the length of the initial
equilibration period and then remove it:

.. code-block:: bash

  >qmca -t -q e -e 0 runs/LiH/vmc_hf/*scalar*

You may notice a region in the early samples that deviates significantly 
from the standard deviation lines marked in red.  Zoom in with the 
magnifying glass to estimate when the energy samples have reached 
equilibrium (fluctuating consistently about the mean).  In this example, 
the equilibration period should last for no more than about 30 samples.


Estimating VMC energy mean, variance, and errorbar
--------------------------------------------------

Now, let's remove the equilibration period to obtain our first estimates 
of the mean energy, the energy variance, and the uncertainty in the 
estimated energy mean (the error-bar):

.. code-block:: bash

  >qmca -q ev -e 30 runs/LiH/vmc_hf/*scalar*
                                LocalEnergy            Variance               ratio 
  runs/LiH/vmc_hf/vmc series 0 -0.748668 +/- 0.004037  0.134660 +/- 0.039404  0.1799

Here the energy mean is approximately -0.7487 Ha, it's uncertainty (error-bar) is 
about 0.004 Ha, and the variance is about 0.13(4) Ha\ :sup:`2`.


Estimating VMC autocorrelation time
-----------------------------------


Obtaining more precise estimates: the Central Limit Theorem
-----------------------------------------------------------



LiH molecule: diffusion Monte Carlo with QMCPACK
================================================

In this example, you will gain experience with projector DMC methods.
DMC is closely related to VMC.  With just the drift-diffusion 
propagator active (no branching), DMC is identical to VMC.  With 
branching, the popluation of walkers is now tied together with 
individual walkers being destroyed or replicated and the entire population 
count fluctuating around an average value.  

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

In the workflow above, an initial DMC calculation was performed in `runs/LiH/dmc`.  The goal is to get a reliable DMC total energy with a 0.01/Ha timestep.  Note that while this timestep is not converged for total energies, it is often sufficient for energy differences of interest (e.g. molecular binding energies, ionization potentials, formation energies of defects in solids, etc), and in those cases timestep extrapolation should instead be performed directly on the energy difference.  

First, a VMC run (series 0, ``dmc.s000.scalar.dat``) was performed to initialize the zero time DMC walker population, which has 1024 walkers. Next, DMC was performed using a larger 0.02/Ha timestep and ran for a short time (30 blocks w/ 10 steps each, series 1, ``dmc.s001.scalar.dat``).  The purpose of this short DMC run with a larger timestep is to rapidly equilibrate the DMC walker population (larger timestep leads to faster equilibration).  Finally, DMC is performed with the production 0.01/Ha timestep for a long time to produce the statistical samples of interest (series 2, ``dmc.s002.scalar.dat``).
  
Take a moment to inspect the fluctuations in the local energy throughout these 
stages via a trace plot:

.. code-block:: bash

   >qmca -t -q e runs/LiH/dmc/*scalar*

All three run section should be visible (VMC: samples 0-199, DMC 1: samples 200-229, DMC 2: samples 230 and beyond).  Use the magnifying glass to zoom in on the region containing the first DMC section that bridges the VMC and second DMC secitons.  In most systems (and/or with a sufficiently large walker population), the DMC local energy will approximately follow an exponentially decreasing curve during the equilibration.  For LiH, the role of correlations is simple (two electrons only) and the trial wavefunction already picks up most of it, resulting in a relatively small energy gap between VMC and DMC and mostly hiding the exponential drop in the energy.

Another important aspect of DMC is the stability of the branching dynamics of the walker population.  This can be monitored by looking at how the walker population (the number of walkers) fluctuates with imaginary time (``dmc.s002.dmc.dat`` file):

.. code-block:: bash

   >qmca -t -q nw runs/LiH/dmc/*s002*dmc*

You should see the walker count fluctuating mildly (to about +/-1%) around its target value of 1024.  Divergent or vanishing walker populations indicate problems with the trial wavefunction or possibly issues with sampling non-local pseudopotentials. Note that these data are plotted with respect to the individual Monte Carlo steps and are not averaged over blocks.

Let's now obtain the DMC energy and compare its value and the autocorrelation time to the ones we calculated previously with VMC:

.. code-block:: bash

   >qmca -e 30 -q e --sac runs/LiH/dmc/*s002*scalar*

   runs/LiH/dmc/dmc series 2  LocalEnergy = -0.788084 +/- 0.000212  6.4

How does the DMC autocorrelation time compare with VMC?  Why? (Hint: you will have to multiply the block autocorrelation time by the number of steps in VMC and DMC, respectively, to compare them directly)

We obtain an energy of -0.7881(2) in DMC vs. -0.7840(2) in VMC, a reduction of about 4 mHa.  However, this value includes timestep error since we have not extrapolated to zero timestep.  Let's do this next.



DMC timestep extrapolation
--------------------------

The timestep extrapolation run was performed in ``runs/LiH/dmc_textrap``.  Here, DMC was run with three successively smaller timesteps (0.04, 0.02, 0.01/Ha) following VMC and the steps per block has been successively increased to partially offset the increased autocorrelation anticipated for the smaller timesteps.

The DMC ground state energy for this system has a weak dependence on timestep:

.. code-block:: bash

   >qmca -e 30 -q e runs/LiH/dmc_textrap/*s00{1,2,3}*scalar*
 
   runs/LiH/dmc_textrap/dmc series 1  LocalEnergy = -0.787784 +/- 0.000258
   runs/LiH/dmc_textrap/dmc series 2  LocalEnergy = -0.787648 +/- 0.000200
   runs/LiH/dmc_textrap/dmc series 3  LocalEnergy = -0.787557 +/- 0.000230

We can quantify the dependence and obtain the zero timestep estimate by 
fitting the data to a line and extrapolating to zero timestep:

.. code-block:: bash

  qmc-fit ts -e 30 -b 8 -t '0.04 0.03 0.01' runs/LiH/dmc_textrap/*s00{1,2,3}*scalar*

  fit function  : linear
  fitted formula: (-0.78747 +/- 0.00022) + (-0.0072 +/- 0.0076)*t
  intercept     : -0.78747 +/- 0.00022  Ha

The extrapolation is performed by resampling the data at each timestep 
(jackknife resampling), making a fit to each resampled mean, and then 
observing the distribution of extrapolated zero time intercepts.  We 
have reblocked the data by a factor of 8 (averaged 8 blocks into single 
new blocks) to remove autocorrelation.  

The final zero timestep value we find is -0.7875(2) Ha, showing that the 
0.01/Ha timestep value underestimated the true value by about 0.6 mHa. 


DMC population control bias
---------------------------

The other controllable approximation in the DMC imaginary time dynamics 
is due to controlling the fluctuations in the walker count (which are 
formally unbounded otherwise).  The induced bias scales like ``1/P``, where 
``P`` is the walker population, and often populations larger than 1000-2000 
walkers are sufficient to control this bias.

Here we will examine the results of a DMC run performed with a smaller 
walker population (256 walkers).  The results are in ``runs/LiH/dmc_pop_256``. 
Compute the total energy and compare it to the first DMC energy from above.
What can you conclude about the magnitude of the bias in the 1024 walker case?

(Note: an important aspect of the LiH system is its low variance.  While 
this makes the system amenable to running on a laptop, it also reduces 
the branching frequency and hence the population control bias relative to 
systems you will see later on in the workshop.)





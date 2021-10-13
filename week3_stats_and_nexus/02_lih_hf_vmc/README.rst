LiH molecule: VMC with QMCPACK and statistical analysis
=======================================================

In this example, you will calculate the Hartree-Fock (HF) estimate of 
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
  runs/LiH/vmc_hf/vmc series 0 -0.747790 +/- 0.012450  0.130273 +/- 0.036354  0.1742

Here the energy mean is approximately -0.748 Ha, it's uncertainty is about 0.01 Ha, and 
the energy variance is about 0.13(4) Ha\ :sup:`2`. 

Is the estimated energy mean consistent with the Hartree-Fock value?  Let's find the 
rough statistical significance by dividing the energy difference by the error bar:

.. code-block:: bash
  
   |-0.747790+0.749663|/0.012 = 0.16

The deviation is about 0.16 sigma.  Values that are actually equal should be expected to 
disagree by more than 1-sigma about 1/3 of the time (68% confidence) and by more than 
2-sigma about 1/20 of the time (95% confidence).  A deviation of greater than 3-sigma 
should always be treated as being (i.e. assumed to be) real.  The deviation we see here 
(0.16 sigma) is consistent with the VMC energy being equal to the deterministic 
Hartree-Fock one.  The answer you see will vary each time you run with a different 
random seed.

As an aside, the last number reported by ``qmca`` above is the variance to energy ratio 
(V/\|E\|) in Ha.  A value larger than about 0.03 Ha suggests a poor quality wavefunction 
in terms of variance.  Later, we will introduce a Jastrow factor to improve the quality 
of the LiH trial wavefunction. 


Estimating VMC autocorrelation time
-----------------------------------

In our estimates of the energy errorbar above, we paid little attention to an important 
aspect: serial auto-correlation of the statistical data.  Auto-correlation arises from 
the close relationship between subsequent steps in the electronic random walk. 
The autocorrelation time can be understood to mean the number of sequential Monte Carlo 
samples that are not statistically independent.

Consider now the results in `runs/LiH/vmc_ac`, where we have run 9 identical VMC 
calculations, apart from differing random number streams, in sequence:

.. code-block:: bash

   >qmca -q e --sac runs/LiH/vmc_ac/*scalar*
    
   runs/LiH/vmc_ac/vmc series 0  LocalEnergy =  -0.783387 +/- 0.004707    3.1 
   runs/LiH/vmc_ac/vmc series 1  LocalEnergy =  -0.782730 +/- 0.004238    2.9 
   runs/LiH/vmc_ac/vmc series 2  LocalEnergy =  -0.769539 +/- 0.008416    8.6 
   runs/LiH/vmc_ac/vmc series 3  LocalEnergy =  -0.767829 +/- 0.009536    8.4 
   runs/LiH/vmc_ac/vmc series 4  LocalEnergy =  -0.785143 +/- 0.006526    6.1 
   runs/LiH/vmc_ac/vmc series 5  LocalEnergy =  -0.790432 +/- 0.003261    1.5 
   runs/LiH/vmc_ac/vmc series 6  LocalEnergy =  -0.787546 +/- 0.005411    4.3 
   runs/LiH/vmc_ac/vmc series 7  LocalEnergy =  -0.782703 +/- 0.005890    2.9 
   runs/LiH/vmc_ac/vmc series 8  LocalEnergy =  -0.792107 +/- 0.007039    2.4 

These runs are using a previously optimized Jastrow factor to obtain a better (lower) 
energy and reduce the variance.
Notice that the estimated errorbar differs by up to a factor of 3 between the runs. 
Each run has the same number of Monte Carlo samples, so how can this be?  The answer 
lies in the estimated autocorrelation time, which is shown in the column on the right. 
The estimated autocorrelation times vary substantially, due to the relatively short 
nature of the runs. Short runs often underestimate the autocorrelation time and 
thus lead to overly optimistic estimates of the statistical errorbar (underestimated 
errorbar).

The answer is to run longer, i.e. with more sequential statistical samples (`blocks` 
in QMCPACK parlance).  In this example, a more precise estimate of the autocorrelation 
can be obtained from the dataset above by joining together all of the data into a single 
set, as follows:

.. code-block:: bash

   >qmca -e 30 -q e --sac -j '0 8' runs/LiH/vmc_ac/*scalar*

   runs/LiH/vmc_ac/vmc series 0  LocalEnergy =  -0.782692 +/- 0.002478    5.1

Try varying this example by increasing the number of blocks provided 
in each VMC input section to confirm whether an autocorrelation time of about 5 
is truly accurate.  Also try increasing the VMC timestep to explore what impact 
it has on the autocorrelation time.  Remember to also change the path, e.g. 
`path='LiH/vmc_ac2'` etc., when rerunning.


Obtaining more precise estimates: the Central Limit Theorem
-----------------------------------------------------------

As you've noticed, the numerical precision of QMC algorithms is limited by 
the size of the statistical errorbar about the mean.  More precise estimates 
can be obtained by generating more statistically independent samples.

The Central Limit Theorem allows us to predict how many samples will be required 
to reach a desired statistical precision.  In general, the size of the errorbar obtained 
will be inversely proportional to the square root of the number of samples. 

In this example, we demonstrate that relationship explicitly by performing 
two VMC runs: the first representing a baseline and the second with 9x more 
samples (and 9x more computational cost).  The relevant data are in `runs/LiH/vmc_clt`:

.. code-block:: bash

   >qmca -e 30 -q e runs/LiH/vmc_clt/*scalar*
   runs/LiH/vmc_clt/vmc_1x  series 0  LocalEnergy =  -0.784283 +/- 0.001517 
   runs/LiH/vmc_clt/vmc_9x  series 0  LocalEnergy =  -0.784239 +/- 0.000476

Notice that the 9x longer run produced an errorbar about 3x smaller (roughly 0.5 mHa 
vs. 1.5 mHa for the baseline run).  How much longer than the baseline would you have 
to run if you wanted an errorbar of 0.2 mHa?  Make a new run based on your estimate 
to confirm.

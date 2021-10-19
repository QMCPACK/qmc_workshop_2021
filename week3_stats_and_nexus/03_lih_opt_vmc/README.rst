LiH molecule: wavefunction optimization with QMCPACK
====================================================

In this example, you will gain experience optimizing parameterized trial 
wavefunctions with VMC methods.  The trial wavefunction in this example 
is of Slater-Jastrow form, with the Jastrow correlation function being the 
target of optimization via minimization of the total energy.  The Jastrow 
factor used here includes electron-electron and electron-ion correlations with 
the correlation functions expanded in a basis of radial B-splines.

The total energy depends non-linearly on the wavefunction parameters (B-spline 
coefficients in this case) and it is optimized via a method in the family 
of linearized general gradient descent algorithms that accounts for stochastic 
sampling (known in the QMC community simply as "the linear method", see Umrigar 
PRL 99 179902 (2007)).  As an iterative method, multiple samplings of the 
trial wavefunction are performed via VMC as the wavefunction parameters are 
updated.  

You will optimize the Slater-Jastrow wavefunction for the LiH molecule over 
several iterations with QMCPACK and then judge the results with a subsequent 
VMC run. Through this example, you will familiarize yourself with the following 
topics in statistical analysis and quantum Monte Carlo (QMC):


**Statistics topics:**

* Statistical significance of energy differences

**QMC topics:**

* Variational Monte Carlo
* Jastrow factors
* Wavefunction optimization
* Ground state energy


Running the initial calculations
--------------------------------
The Nexus workflow script ``lih_workflow.py`` performs the following sequence 
of calculations:

1. Hartree-Fock calculation (see ``generate_pyscf``).
2. Conversion of PySCF orbital format to QMCPACK HDF5 file (see ``generate_convert4qmc``).
3. Jastrow optimization via energy minimization with the linear method (see ``opt = generate_qmcpack``).
4. Variational Monte Carlo calculation with the optimized Slater-Jastrow trial wavefunction (see ``vmc = generate_qmcpack``).

Take a minute to read through the workflow file and familiarize yourself 
with its contents.  Next, run the workflow script (this may take a few 
minutes depending on the available computational resources):

.. code-block:: bash

  >./lih_workflow.py


Form of the Jastrow factor
--------------------------

Here we use a two-body Jastrow factor, including radial correlation functions 
for electron spin pairs (only one up and one down electron in LiH) as well as 
electron-ion terms. The trial correlation functions are explicitly short-ranged 
(zero beyond a cutoff) and include B-spline basis functions over a uniform grid. 
For this example, cutoffs of 6 and 8 Bohr have been selected for the e-H/e-Li 
and e-e terms respectively, with one basis function per 0.5 Bohr.  The trial
Jastrow therefore has 12+12+16 = 40 parameters.  


Judging wavefunction optimization
---------------------------------

In the workflow above, Jastrow optimization was performed in ``runs/LiH/opt``. 
During the optimization, 4 initial iterations were performed allowing larger 
parameter changes, followed by 8 production iterations.  QMCPACK produces 
one ``scalar.dat`` file for each iteration performed during the optimization 
using the parameterized trial function for that respective iteration. 
Inspect the ground state energy and variance through the optimization process:

.. code-block:: bash

   >qmca -e 20 -q ev runs/LiH/opt/*scalar*
    
                               LocalEnergy            Variance               ratio 
   runs/LiH/opt/opt series 0  -0.746956 +/- 0.002803  0.109144 +/- 0.005954  0.1461 
   runs/LiH/opt/opt series 1  -0.776778 +/- 0.001127  0.027871 +/- 0.002182  0.0359 
   runs/LiH/opt/opt series 2  -0.780653 +/- 0.001714  0.019933 +/- 0.001993  0.0255 
   runs/LiH/opt/opt series 3  -0.784852 +/- 0.000834  0.012195 +/- 0.001039  0.0155 
   runs/LiH/opt/opt series 4  -0.782929 +/- 0.000895  0.010264 +/- 0.000547  0.0131 
   runs/LiH/opt/opt series 5  -0.783139 +/- 0.000683  0.009598 +/- 0.000772  0.0123 
   runs/LiH/opt/opt series 6  -0.783096 +/- 0.001144  0.009882 +/- 0.000720  0.0126 
   runs/LiH/opt/opt series 7  -0.784036 +/- 0.000781  0.008994 +/- 0.000433  0.0115 
   runs/LiH/opt/opt series 8  -0.784658 +/- 0.000805  0.010037 +/- 0.001171  0.0128 
   runs/LiH/opt/opt series 9  -0.784699 +/- 0.000731  0.009089 +/- 0.000480  0.0116 
   runs/LiH/opt/opt series 10 -0.782754 +/- 0.000776  0.008703 +/- 0.000474  0.0111 
   runs/LiH/opt/opt series 11 -0.784038 +/- 0.000795  0.008558 +/- 0.000610  0.0109 

The first line of the output (series 0) corresponds to the local energy and variance of 
the system without a Jastrow factor (all Jastrow coefficients were initialized to zero 
in this case), reflecting the quality of the orbitals alone. For pseudopotential systems, 
a variance/energy ratio >0.20 Ha generally indicates there is a problem with the input 
orbitals that needs to be resolved before performing wavefunction optimization.

For the production iterations (4-11), the first thing to check about the resulting 
optimization is again the variance/energy ratio.  For pseudopotential systems, a 
variance/energy ratio <0.03 Ha is consistent with a trial wavefunction of production 
quality, and values lower than 0.01 Ha are rarely obtainable for standard Slater-Jastrow 
wavefunctions. By this metric, all parameterizations obtained for optimizations performed 
in iterations 4-11 are of comparable quality.

So, has the optimization converged and which Jastrow parameterization is the best? 
We can gain some insight into these questions by considering the statistical significance 
of the energy difference between the highest and lowest energies found in iterations 4-11.
The energy difference is:

.. code-block:: bash

  |-0.78275+0.78470| = 0.00195 Ha

The error bar of the energy difference is the square root of the sum of the two individual 
errorbars: 

.. code-block:: bash

  sqrt( 0.00078^2 + 0.00073^2 ) = 0.00107 Ha

And so the energy difference differs from zero by 0.00195/0.00107 = 1.82 sigma.  We see 
this in 1/8 iterations, while on averate a 2 sigma difference is expected 1/20 of the time, 
so there is low confidence that the lowest energy wavefunction is any better than the 
highest energy one in iterations 4-11.  This is consistent with the optimization having 
"plateaued", or in other words, convergence has been reached and any of the Jastrow factors 
obtained in this range may be safely used.  

You can observe the convergence behavior directly by plotting the energy and variance vs. 
iterations (click on the magnifying glass icon and select a rectangular region in the 
plots to zoom in):

.. code-block:: bash

   >qmca -p -e 20 -q ev runs/LiH/opt/*scalar*


Obtaining the VMC ground state energy
-------------------------------------

In the workflow, VMC was performed following the optimization with the Jastrow factor 
selected by Nexus.  In practice, Nexus selects the lowest energy trial wavefunction within 
the range of iterations with reasonable variance/energy ratios.  The results can be found 
in ``runs/LiH/vmc``:

.. code-block:: bash

   >qmca -e 20 -q ev runs/LiH/vmc/*scalar*
 
                               LocalEnergy            Variance               ratio 
   runs/LiH/vmc/vmc series 0  -0.784046 +/- 0.000236  0.009289 +/- 0.000222  0.0118 

How much energy was gained by the Jastrow function relative to Hartree-Fock?  Retry the 
optimization with 4x fewer and 4x more samples (be sure to remember to change the ``path`` 
in ``generate_qmcpack`` for both the optimization and VMC runs).  Do you obtain 
significantly better or worse results, as judged by the subsequent VMC run?






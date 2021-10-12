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

You will optimize the Slater-Jastrow wavefunction for LiH over several 
iterations with QMCPACK and then judge the results with a subsequent VMC run. 
Through this example, you will familiarize yourself with the following topics 
in statistical analysis and quantum Monte Carlo (QMC):


**Statistics topics:**

* Statistical significance of energy differences
* Optimization bias with finite sample sizes

**QMC topics:**

* Variational Monte Carlo
* Wavefunction optimization
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



Estimating VMC energy mean, variance, and errorbar
--------------------------------------------------



Estimating VMC autocorrelation time
-----------------------------------



Obtaining more precise estimates: the Central Limit Theorem
-----------------------------------------------------------


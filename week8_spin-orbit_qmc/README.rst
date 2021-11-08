================================================
Bi ground state multiplet with DIRAC and QMCPACK
================================================

In this example, we give an example of using DIRAC to calculate 
spin-orbit splittings of the 6s\ :sup:`2`\ 6p\ :sup:`3` occupations of the Bi atom. 
We can find the experimental splittings from the `NIST Atomic Spectra Database <https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum=Bi+I&submit=Retrieve+Data&units=1&format=0&output=0&page_size=15&multiplet_ordered=0&average_out=1&conf_out=on&term_out=on&level_out=on&unc_out=1&j_out=on&lande_out=on&perc_out=on&biblio=on&temp=>`_

For the first few states on the NIST page, we notice there are a number of term symbols :sup:`2S+1`\ L\ :sub:`J` for the 6s\ :sup:`2`\ 6p\ :sup:`3` occupation. 
In the abscence of spin-orbit coupling, the various J states averaged to give just :sup:`4`\ S, :sup:`2`\ D, and :sup:`2`\ P, whereas with SOC we obtain the J states are split and we obtain the various splittings, illustrated below.

.. image:: figs/Bi_states.png
  :width: 85%
  
.. contents::

Example 1: Spin-orbit averaged states of Bi with DIRAC
======================================================

To set up a DIRAC calculation, there are two input files needs, the ``*.inp`` file which specifies the type of calculation to be done, and the ``*.mol`` file which
specifies the geomerty, basis sets, effective core potentials (ECPs), etc.

For a thorough decription of DIRAC input/out see `DIRAC <http://www.diracprogram.org/doc/release-21/>`_

*.mol file
----------
Here we will breakdown the *.mol file step by step. A detailed desrciption of the *.mol file can be found `here <http://www.diracprogram.org/doc/release-21/molecule_and_basis/molecule_using_mol.html>`_   
:: 
  INTGRL 
  Bi        
  Bi STU ecp
  C   1         
        83.    1 
  Bi     0.000000           0.00000000        0.00000000
  
Here, the first ``INTGRL`` is required, and the next two lines are simply comments. 
The ``C   1`` specifies that we want cartesian spherical basis sets and only 1 atom.
After that, for each diffent species we list the atomic number and how many of that element we want. 
In this case, we are keeping things simple and only doing an atom at the origin.
::
  LARGE EXPLICIT  4    1    1    1    1            
  f  13  0                 
  798.633           
  95.0023 
  21.2520
  13.2919 
  8.31210
  5.19476
  1.90972
  0.962271
  0.356026
  0.168327
  0.0784  
  0.073265
  0.0297
  f  12  0
  19.2259
  12.0378
  7.53621   
  2.16084
  1.13036       
  0.566778        
  0.4469            
  0.271608
  0.117769              
  0.0743                
  0.049304
  0.0276               
  f  9  0              
  65.0224               
  13.6908               
  7.09591
  2.52090              
  1.34066              
  0.682558
  0.327714              
  0.1306                
  0.0488
  f  2  0                                         
  0.3164
  0.1188

Under each atomic species type, we have to provide a basis set. The ``LARGE EXPLICIT  4    1    1    1    1`` tells us that we are specifying the basis for the large components of the spinors (note that for ECP calculations, we only have the large components. In all-electron calculations, DIRAC can automatically generate an eve-tempered basis for the small components based on the basis provided for the large components. So it is often sufficient to proivide only a LARGE basis. The ``EXPLICIT`` simply means that we are explicitly typing a basis. The ``4`` tells us that we will have 4 different angular momentum basis sets ``s,p,d,f`` in this case. The subsequent ``1`` means that we are writing one set of exponents and coefficients for each shell. 

For each individual angular momentum basis, the expansion starts as ``f   N  0`` and tells us the number of exponents to read, and the 0 means that we will be using an uncontracted basis. For an uncontracted basis, we do not need the coefficients. These can be provided as additional columns if desired (see the link above). 

Lastly, for each atomic species we need to provide an ECP specification. A detailed description of the input can be found `here <http://www.diracprogram.org/doc/release-21/molecule_and_basis/molecule_with_ecp.html>`_ 
::
  ECP 78 5 0
  3
  1 40.00000 5.0
  3 38.50000 200.0
  2 40.00000 -74.796
  2
  2  1.994153  35.755622
  2  0.240286  -0.404113
  4
  2  0.896039  2.688441
  2  0.875463  5.715603
  2  0.262580  -0.171255
  2  0.232846  -0.150845
  2
  2  0.779775  4.060445
  2  0.739216  5.980282
  2
  2  0.987519  -2.646547 
  2  0.959907  -3.373825
  FINISH
 
Here ``ECP 78 5 0`` indicates that this ECP removes 78 core electrons, and have 5 channels (1 local and 4 nonlocal) and 0 spin-orbit channels. For spin-averaged calculations, we do not include the spin-orbit terms (we will add them later). You provide the local channel first, then each subsequent channel in order of increasing angular momentum (i.e. local, s, p, d, f in this case). For each channel, we specify the number of radial gaussian and then the gaussian parameters (n, a, c) where the gaussian is of the form c*r\ :sup:`n-2`\ *exp(-a*r\ :sup:`2`\ ). 
Lastly, after specifying all the basis sets and ECPs for the various atoms, we must conclude the file with ``FINISH``.

For this example, I am using a Stuttgart ECP (can be found `here <http://www.tc.uni-koeln.de/PP/clickpse.en.html>`_) and the corresponding basis set (uncontracted). Note that for Stuttgart ECPs, the potentials are divergent. I have modified the local channel myself to *smooth* the potential which helps with the efficiency of the subsesquent QMC. I will not be covering how to smooth a potential without changing  its propertiess. If you need help with potential, reach out to the QMCPACK developers.

*.inp file
----------

Here I will outline some of the critical parameters for the *.inp file to perform a complete open-shell confiuration interaction (COSCI). To understand the different input options, it is best to read through the various tutorials on the DIRAC page. 
::
  **DIRAC
  .WAVE FUNCTION
  .ANALYZE
  **HAMILTONIAN
  .ECP
  **INTEGRALS
  *READIN
  .UNCONTRACT
  
This indicates that we want to use the ``WAVE FUNCTION`` and ``ANALYZE`` modules which allows us to calculate wave functions and perform some analysis on the states and spinors. 
We specify that we are using ECPs in the ``HAMILTONIAN``. Additionally, I also specify that I want to use uncontracted basis sets (this will override whatever is specified in the *.mol file. In this case, this keyword is redundant since I already specified an uncontracted basis in the *.mol file). 

The actual calculation is specified by the ``**WAVE FUNCTION`` module
::
  **WAVE FUNCTION
  .SCF
  .RESOLVE
  *SCF
  .CLOSED SHELL
  2 0
  .OPEN SHELL
  1
  3/0,6
  .EVCCNV
  1.0d-05
  
We specifiy that we want to do an SCF calulation, which will perform an *average of configurations* SCF calculation. 

.. image:: figs/aoc.png
  :width: 25%
  
which will set up all the possible determinants for the open-shell occupations specified (more on this later). The SCF procedure finds the spinors which minimizes this energy. The individiual states can be obtained by the ``.RESOLVE`` keyword, which diagonalizes the states in the determinant basis, which will result in small CI expansions for the various states.

.. image:: figs/ci.png
  :width: 25%
  
In the ``*SCF`` section, we need to actually specify the occupations we are desired in studying. As mentioned above, for Bi we have the 6s\ :sup:`2`\ 6p\ :sup:`3` occupation. In DIRAC, we have to specify the occupations by the symmetry of the spinors (gerade/even or ungerade/odd). Note that s,d,g, etc are all gerade and p,f,h, etc are all ungerade symmetry. We want to specify the 6s\ :sup:`2` as closed, so we will have 2 electrons closed in the gerade channel and 0 closed in the ungerade channel, hence
::
  .CLOSED
  2 0
  
For the open shells, we have 3 electrons in the p states. We note that there are 6 total occupations for the p states (in the non-spin-orbit case we have p\ :sub:`x`\  , p\ :sub:`y`\ , p\ :sub:`z` each with up and down options. For a spin-orbit case, this would be the j=1/2 (degeneray 2) and j=3/2 (degeneracy 4). Both end up wth 6 total possible states). We want to fix the electrons to be p electrons only, and we do not want to distribute these electrons into any gerade spinors. 
Therefore, we specify
::
  .OPEN SHELL
  1
  3/0,6
  
We only have one active space in this case, however we could increase this and add multiple occupation lines. Additinoally, we could do a larger scale COSCI calculation where we correlate the s electrons as well with the following input
::
  .CLOSED
  0 0
  .OPEN SHELL
  1
  5/2,6
  
For simplicity, we will work with the first input. 

Note that since we have 6 possible spinors for the p elecrons, and we only occupy with 3 electrons, we will have 6choose3 = 20 possible determinants/COSCI states after calling ``.RESOLVE``

Lastly, an important part of the input is the ``**ANALYZE`` module, where we specify some additional printing to the output file. Some of this is **required** for conversion to QMCPACK.
::
  **ANALYZE
  .PRIVEC
  .MULPOP
  *PRIVEC
  .AOLAB
  .VECPRI
  1..oo
  1..oo
  .PRINT
  1
  *MULPOP
  .AOLAB
  .VECPOP
  1..oo
  1..oo
  .PRINT
  1
  
The ``.PRIVEC`` specifies that we want to print the obtained spinors. **THIS IS REQUIRED FOR CONVERSION TO QMCPACK**, otherwise we cannot read the spinor coefficients. In the ``*PRIVEC``, we indiccate that we want to print the spinors (eigenvectors) in the atomic orbital basis (hence, the ``.AOLAB``). The ``.VECPRI`` tells us to print to the output file all of the spinors for each symmetry (gerade, then ungerade). The ``1..oo`` prints all the spinors in that symmetry channel. If we only want to print the first 10 for example, we could just write ``1..10``. The ``.MULPOP`` command is not required, but it is useful to see the mulliken population analysis of the spinors. 

Running DIRAC and understanding the output
------------------------------------------

Running DIRAC is straightforward. Assuming the ``pam-dirac`` script is in your path, you can simply run 
::
  pam-dirac --inp="cosci.inp" --mol="Bi.mol"

Assuming this is successful, we will be able to see the output in the ``cosci_Bi.out`` file.

To see the results of the average of configurations calculations, we can look for the total energy
::
                                   TOTAL ENERGY
                                   ------------

   Electronic energy                        :    -5.2141207112141519

   Other contributions to the total energy
   Nuclear repulsion energy                 :     0.0000000000000000

   Sum of all contributions to the energy
   Total energy                             :    -5.2141207112141519

The energy of *E* = -5.21412 Ha, this is the energy obtained from the E\ :sub:`AOC` expression above.

In order to connvert to QMCPACK, we need to make sure the eigenvectors (spinors) were actually printed. 
::
    **************************************************************************
    ****************************** Vector print ******************************
    **************************************************************************



    Coefficients from DFCOEF
    ------------------------



                                Fermion ircop E1g
                                -----------------


  * Electronic eigenvalue no.  1: -0.6809061437841
  ====================================================
       1  L Bi  1 s             0.0000118634        0.0000000000        0.0000000000        0.0000000000
       2  L Bi  1 s            -0.0002764816        0.0000000000        0.0000000000        0.0000000000
       3  L Bi  1 s             0.0078341692        0.0000000000        0.0000000000        0.0000000000
       4  L Bi  1 s            -0.0357656369        0.0000000000        0.0000000000        0.0000000000
       5  L Bi  1 s             0.0729896399        0.0000000000        0.0000000000        0.0000000000
       6  L Bi  1 s            -0.0698826077        0.0000000000        0.0000000000        0.0000000000
       ...
       
The columns correspond to the real and imaginary parts of the up and down components of the total spinor. The qmcpack converter understands how to handle this. 

Next we want to check if the open-shell states are resolved into the various small CI expansions (COSCI calculation)
::
    *************************************************************************
    ******************** Resolution of open-shell states ********************
    *************************************************************************
      
Assuming we find this, we can search for the results. 
::
 Energy eigenvalues in atomic units

 Level   Rel eigenvalue     Abs eigenvalue      Total Energy    Degeneracy

    1     0.0000000000     -1.750400036742       -5.271133025983 (   4 * )
    2     0.0570123148     -1.693387721973       -5.214120711214 (  10 * )
    3     0.0950205246     -1.655379512127       -5.176112501368 (   6 * )

First thing to note, the individually resolved energies all average to the SCF energy we found above, i.e.  ``(1/20  * (4 * -5.271133 + 10 * -5.214120 + 6 * -5.176112)) = -5.214120 Ha``. Next we can identify the states as the states shown in the first image. From the experimental spetrum, we only have the :sup:`4`\ S\ :sub:`3/2` state which *isn't* j-averaged, so the degeneracy of this state is 4. Note there are both :sup:`2`\ D\ :sub:`3/2` and :sup`2`\ D\ :sub:`5/2` states which get averaged in the absence of spin-orbit, so there are 4+6=10 total degenerate states. Lastly, the :sup:`2`\ P\ :sub:`3/2` and :sup:`2`\ P\ :sub:`1/2` states, which get averaged in the absence of spin-orbit, so there are 4+2 = 6 total states. Therefore, we have reproduced the ordering of the j-averaged experimental spectrum when we neglect SOC. We also note the splittings of 0.057012 Ha and 0.095020 Ha correspond to 1.55137 eV and 2.585625 eV respetively. Compared to the experimental j-averaged spectrum, we have errors of roughly 0.163 eV and 1.050 eV respectively. 

This simple COSCI treatment can be signifiantly improved with QMC for the j-averaged states. However, we will now focus on the SOC calculations and perform QMC calcualtions on the SOC calculations. 


Example 2: Spin-Orbit split states of Bi with DIRAC
===================================================

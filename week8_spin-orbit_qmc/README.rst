Bi ground state multiplet with DIRAC and QMCPACK
====================================================================

In this example, we give an example of using DIRAC to calculate 
spin-orbit splittings of the 6s\ :sup:`2`\ 6p\ :sup:`3` occupations of the Bi atom. 
We can find the experimental splittings from the `NIST Atomic Spectra Database <https://physics.nist.gov/cgi-bin/ASD/energy1.pl?de=0&spectrum=Bi+I&submit=Retrieve+Data&units=1&format=0&output=0&page_size=15&multiplet_ordered=0&average_out=1&conf_out=on&term_out=on&level_out=on&unc_out=1&j_out=on&lande_out=on&perc_out=on&biblio=on&temp=>`_

For the first few states on the NIST page, we notice there are a number of term symbols :sup:`2S+1`\ L\ :sub:`J` for the 6s\ :sup:`2`\ 6p\ :sup:`3` occupation. 
In the abscence of spin-orbit coupling, the various J states averaged to give just :sup:`4`\ S, :sup:`2`\ D, and :sup:`2`\ P, whereas with SOC we obtain the J states are split and we obtain the various splittings, illustrated below.

.. image:: figs/Bi_states.png
  :width: 85%

Example 1: Spin-orbit averaged states of Bi with DIRAC
------------------------------------------------------

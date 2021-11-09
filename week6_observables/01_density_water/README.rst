H2O molecule: Calculating the Density with VMC and DMC 
=======================================================

In this example you will calculate the H2O molecule's charge density with QMCPACK.
Inside this directory, you will find the structure of the molecule in .xyz format (H2O.xyz),
the relevant ccECP pseudopotentials inside the directory ``pseudopotentials``, the PySCF
template file ``scf_template.py``, and the Nexus work flow script ``h2o_workflow.py``.

The Nexus workflow script ``h2o_workflow.py`` performs the following sequence 
of calculations:

1. Hartree-Fock calculation (see ``generate_pyscf``).
2. Conversion of PySCF orbital format to QMCPACK HDF5 file (see ``generate_convert4qmc``).
3. 2-Body Jastrow Optimization of the Salter-Jastrow wave function (see ``generate_qmcpack``).
4. Sequence of VMC and DMC calculations of H2O's charge density (see ``generate_qmcpack``).

After the work flow has successfully completed, you will need to convert the density from
.h5 format to xcrysden (.xsf) format so that it can be easily visualized with a program
such as VESTA. To do this, first determine the equilibration and auto-correlation lengths
with the ``qmca`` tool (see Week 3 workshop materials) for both VMC (series 0) and DMC (series 2)
runs -- note that series 1 was simply used to speed up the imaginary time evolution.
I found that equilibration lengths of 10 and 25 were sufficient for VMC and DMC, respectively.
In addition, I found auto-correlation lengths of around 1 and 3 for VMC and DMC, respectively.

You can now enter the QMC work directory and generate the .xsf files using the ``qdens`` tool, as follows:

.. code-block:: bash

  > cd ./runs/H2O/dmc_J2
  > qdens -f xsf -e 10 -r 1 -i dmc.in.xml --noplot dmc.s000.stat.h5
  > qdens -f xsf -e 25 -r 3 -i dmc.in.xml --noplot dmc.s002.stat.h5

After execution, the following files will be generated:

.. code-block:: bash

  > ls -l *Density* 
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s000.Density_q+err.xsf
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s000.Density_q-err.xsf
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s000.Density_q.xsf
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s002.Density_q+err.xsf
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s002.Density_q-err.xsf
  -rw-rw-r-- 1 qmcuser qmcuser 1890877 Nov  9 08:05 dmc.s002.Density_q.xsf

Now you can launch VESTA and import either the VMC mean ``dmc.s000.Density_q.xsf`` or the DMC mean ``dmc.s002.Density_q.xsf``.
VESTA will allow you to visualize the structure, isosurface of the density, etc.

Lastly, let's look at the QMC oxygen population using integrated angular averages of the density around the oxygen site.
We would like to use the extrapolated estimate for this quantity to achieve an error that is 2nd order. This can be
done by providing ``qdens-radial`` with the VMC .xsf file and the DMC .xsf file. Given these files, the tool will
perform the extrapolation for you:

.. code-block:: bash

   > qdens-radial -p -s O -r 1.1 -c --vmc=dmc.s000.Density_q.xsf dmc.s002.Density_q.xsf

For more information about Nexus and QMCPACK, please consult their respective documentation:

* QMCPACK: https://qmcpack.readthedocs.io/en/develop/
* Nexus: https://nexus-workflows.readthedocs.io/en/latest/

For more information on QMC methods in general (theory and application), 
the 2001 Rev. Mod. Phys. by Foulkes et al. is essential reading:

* https://doi.org/10.1103/RevModPhys.73.33

This lab uses the ``qmca`` and ``qmc-fit`` tools for statistical data analysis.  See their respective documentation for more details:

* qmca: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmca
* qmc-fit: https://qmcpack.readthedocs.io/en/develop/analyzing.html#qmcfit

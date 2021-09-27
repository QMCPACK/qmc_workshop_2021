Nexus Example: Diamond Equation of State with Quantum Espresso
==============================================================

In this example, we give an introduction to Nexus by using it to run a simple 
system (diamond) with Quantum Espresso.  The goal is to calculate the equation 
of state (energy vs. lattice constant) and determine the equilibrium lattice 
constant.  The Nexus script we will use is ``diamond_eos.py`` in the current directory.
Reference data for this example can be found in the ``reference`` directory.

If you have not used Nexus before, we recommend you briefly read the 
*Background* section below.  Otherwise, feel free to proceed directly 
to *Running the Example*.


Background
----------

Each Nexus script has five main sections:

1. Module imports from Nexus (and/or other Python modules).
2. Setting variables to provide information and control Nexus' behavior.
3. Specifying the physical system (diamond in this case).
4. Specifying information for all simulation workflows (PBE calculations with QE here).
5. Execution of the simulation workflows.

These five sections are illustrated below using a simplified version of the ``diamond_eos.py`` as an example:

.. code-block:: python

    # Nexus module imports
    from nexus import settings,job,run_project
    from nexus import generate_physical_system
    from nexus import generate_pwscf
    
    # Setting Nexus variables 
    settings(
        ...
        )
    
    # Physical system information
    system = generate_physical_system(
        ...
        )
    
    # Simulation workflow information
    scf = generate_pwscf(
        ...
        )
    
    # Execute the workflows
    run_project()

Before running the example, we will give a little more information about the 
Nexus functions involved in sections 2-5. 

**settings function**

Provide basic information, such as the location of pseudopotential files 
and details of the local machine (workstation or named supercomputer like 
Summit).  Also provide basic information to control Nexus, such as the 
number of seconds between polling checks on simulation run status.

.. code-block:: python

    settings(
        pseudo_dir = './pseudopotentials', # Directory with pseudo files
        results    = '',     # Do not copy sim results into separate directory 
        sleep      = 3,      # Poll simulation status every 3 seconds
        machine    = 'ws12', # Machine is a 12 core workstation
        )

**generate_physical_system function**

Create an object containing details of the physical system, such as the atomic 
species, and atomic positions. If applicable, also provide effective charges of 
pseudo-atoms, cell axes, tiling matrix, and cell k-point grid.  The description 
of the physical system is made once and is shared between simulations in a 
workflow.  In addition to providing the atomic and cell information explicitly, 
this information can also be loaded directly from an appropriate ``xyz``, 
``xsf``, ``POSCAR``, or ``cif`` file (use ``structure = /path/to/your/file,``).

.. code-block:: python

    # Physical system object is assigned to a local variable named "system"
    system = generate_physical_system(
        # Distances are in Angstrom units
        units    = 'A',
        # Cell axes 
        axes  = [[a/2, a/2,   0],   
                 [  0, a/2, a/2],
                 [a/2,   0, a/2]],
        # Element names
        elem  = ['C','C'],      
        # Element positions (crystal units)
        posu  = [[0.00, 0.00, 0.00],
                 [0.25, 0.25, 0.25]],
        axes     = '''1.785   1.785   0.000
                      0.000   1.785   1.785
                      1.785   0.000   1.785''',
        # Pseudopotential for C has Zeff=4
        C        = 4,
        )

**generate_pwscf function**

Create a simulation object containing details about the simulation run 
directory, input/output file prefix, job submission information, and other 
simulation-specific keywords to generate the input file.

.. code-block:: python

    scf = generate_pwscf(
        identifier   = 'scf',           # Prefix in/out files with "scf"
        path         = 'diamond/scf',   # Run directory location
        job          = ...              # Job details, see "job function" below
        input_type   = 'generic',       # Use standard inputs below
        # All PW inputs are allowed     
        calculation  = 'scf',           # Run an scf calculation
        input_dft    = 'pbe',           # Use pbe functional
        ecutwfc      = 200,             # 200 Ry orbital plane-wave cutoff
        conv_thr     = 1e-8,            # Convergence threshold of 1e-8 Ry
        system       = system,          # Atom/cell information
        pseudos      = ['C.ccECP.upf'], # Pseudopotential files
        kgrid        = (4,4,4),         # 4x4x4 Monkhorst-Pack grid
        kshift       = (0,0,0),         # centered at Gamma
        )

**job function**

Create an object containing job submission information.  On a workstation this 
is primarly the number of cores and threads (mpi tasks will be set to 
#cores/#threads).  On a supercomputer, this also typically includes node count, 
wall time, and environment variable information.  On these machines job 
submission files are automatically created and executed.

.. code-block:: python

    job(cores=12,  # Run on all 12 cores (12 mpi tasks)
        app='pw.x' # Path to PW executable (defaults to pw.x)
        ),

**run_project function**

Execute all simulation runs.  Up to this point, the workflow information has 
been specified (e.g. via ``generate_pwscf``) but no simulation runs have been 
performed.  When this function is executed, all simulation dependencies are 
noted and simulations are executed in the order needed to satisfy all 
dependencies.  Multiple independent simulations will execute simultaneously 
(always true on a supercomputer/cluster, true on a workstation if there are 
sufficient free resources).  When executing the simulation runs, Nexus enters 
a polling loop to monitor simulation progress.  When this function completes, 
all simulation runs will also be complete.

.. code-block:: python

    # Run the simulation workflows specified earlier
    run_project()


Running the Example
-------------------
The script we will use differs from the simple example above in that multiple 
calculations will be performed since our goal is to obtain the equation of 
state (energy vs. lattice constant) curve of diamond.  In ``diamond_eos.py``, 
you will notice a loop over multiple scaling factors for the cell.

First run the Nexus script with the ``status_only`` flag set.  This will show 
the queue of jobs that Nexus is managing, including their current status.

.. code-block:: bash

    >./diamond_eos.py --status_only
    
      ...
      
      cascade status 
        setup, sent_files, submitted, finished, got_output, analyzed, failed 
        000000  0  ------    scf     ./runs/a_3.0345  
        000000  0  ------    scf     ./runs/a_3.2130  
        000000  0  ------    scf     ./runs/a_3.3915  
        000000  0  ------    scf     ./runs/a_3.5700  
        000000  0  ------    scf     ./runs/a_3.7485  
        000000  0  ------    scf     ./runs/a_3.9270  
        000000  0  ------    scf     ./runs/a_4.1055  
        setup, sent_files, submitted, finished, got_output, analyzed, failed 

The QE PBE SCF runs will be performed in the ``./runs/a_*`` directories and 
the input and output files will be prefixed with ``scf`` (scf.in and scf.out).  
The statusflags, represented as ``0`` or ``1`` are described below:

**0**\ 00000  0  ------  **setup**: Input files (have/have not) been written.

0\ **0**\ 0000  0  ------  **sent_files**: Additional files (e.g. pseudopotentials) (have/have not) been copied in locally.

00\ **0**\ 000  0  ------  **submitted**: Job (has/has not) been submitted.

000\ **0**\ 00  0  ------  **finished**: Simulation (is/is not) finished.

0000\ **0**\ 0  0  ------  **got_output**: Output data (has/has not) been copied.

00000\ **0**  0  ------  **analyzed**: Output data (has/has not) been analyzed.

000000  **0**  ------  **failed**: Simulation (has/has not) failed.

000000  0  **------**  **job_id**: Job submission and/or process id of the simulation.

Now run the Nexus script, allowing it to submit and manage the SCF calculation:

.. parsed-literal::

    >./diamond_eos.py

    ``...``  

    starting runs:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    elapsed time 0.0 s  memory 102.13 MB 
      ...
      Entering ./runs/diamond/a_3.5700 0 
        **writing input files**  0 scf       **\# write input file**  
      Entering ./runs/diamond/a_3.5700 0 
        **sending required files**  0 scf    **\# copy in pseudo files**
        **submitting job**  0 scf            **\# submit the job**
      Entering ./runs/diamond/a_3.5700 0 
        Executing:  
          **export OMP_NUM_THREADS=1**       **\# local execution**
          **mpirun -np 12 pw.x -input scf.in** 
  
    **elapsed time 3.0 s**  memory 102.23 MB     **\# single monitoring poll, short run** 
      Entering ./runs/diamond/a_3.5700 0 
        **copying results**  0 scf           **\# copy output files** 
      Entering ./runs/diamond/a_3.5700 0 
        **analyzing**  0 scf                 **\# analyze output data**
  
    **Project finished**                     **\# all simulations finished**


Check the status of the runs.  Each simulation step should have a status of 
``1`` and ``failed`` should have a status of ``0``.  The process id should 
also be populated.

.. code-block:: bash

    >./diamond_eos.py --status_only
  
    ...
    
    cascade status 
      setup, sent_files, submitted, finished, got_output, analyzed, failed 
      111111  0  31916     scf     ./runs/a_3.0345  
      111111  0  31994     scf     ./runs/a_3.2130  
      111111  0  32058     scf     ./runs/a_3.3915  
      111111  0  32120     scf     ./runs/a_3.5700  
      111111  0  32179     scf     ./runs/a_3.7485  
      111111  0  32240     scf     ./runs/a_3.9270  
      111111  0  32300     scf     ./runs/a_4.1055  
      setup, sent_files, submitted, finished, got_output, analyzed, failed 


Each QE run should have completed successfully, e.g. with files like those in 
``./runs/a_3.5700``:

.. parsed-literal::

    >ls -lrt runs/a_3.5700/
    total 224
    -rw-r--r-- 1 j1k users 192747 Jul 29 14:53 C.ccECP.upf     **\# ccECP PP copied locally**  
    -rw-r--r-- 1 j1k users     89 Sep 27 13:35 scf.struct.xyz  **\# atomic structure file**    
    -rw-r--r-- 1 j1k users    264 Sep 27 13:35 scf.struct.xsf  **\# atomic structure file**    
    -rw-r--r-- 1 j1k users    756 Sep 27 13:35 scf.in          **\# QE input file**            
    -rw-r--r-- 1 j1k users      0 Sep 27 13:35 scf.err         **\# stderr output from QE**    
    -rw-r--r-- 1 j1k users  11005 Sep 27 13:35 scf.out         **\# stdout output from QE**    
    drwxr-xr-x 3 j1k users   4096 Sep 27 13:35 pwscf_output    **\# QE outdir**                
    drwxr-xr-x 2 j1k users   4096 Sep 27 13:35 sim_scf         **\# Nexus sim state file**     

Now we can obtain the PBE energy vs. lattice constant for diamond:

.. code-block:: bash

    >grep '! ' runs/a_*/*.out
    runs/a_3.0345/scf.out:!    total energy              =     -22.39012981 Ry
    runs/a_3.2130/scf.out:!    total energy              =     -22.60492242 Ry
    runs/a_3.3915/scf.out:!    total energy              =     -22.71014282 Ry
    runs/a_3.5700/scf.out:!    total energy              =     -22.73944516 Ry
    runs/a_3.7485/scf.out:!    total energy              =     -22.71717281 Ry
    runs/a_3.9270/scf.out:!    total energy              =     -22.66103531 Ry
    runs/a_4.1055/scf.out:!    total energy              =     -22.58424388 Ry

Collect the lattice constants (first column) and total energies (second column) into a file.
Then run the `fit_eos.py` script on the data to perform a simple fit of the data to extract 
the equilibrium lattice constant.  

.. code-block:: bash

   >fit_eos.py Edata.txt

   Equilibrium lattice constant: 3.5687 A

For reference, the equilibrium lattice constant of diamond measured in experiment is 3.567 Angstrom.

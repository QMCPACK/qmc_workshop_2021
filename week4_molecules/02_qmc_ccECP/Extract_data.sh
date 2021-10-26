#!/bin/bash


echo "##Distance        DFT                    DMC">> Data.dat
for i in 0.9 1.0 1.1 1.208 1.3 1.4 1.6 2.0 2.2 2.4 2.6 2.8 3.0 
do 
	y=$(grep "converged SCF energy =" runs/O2/Dist_${i}/SCF/scf.out | sed s/"converged SCF energy ="/""/g)
	z=$(qmca -q e runs/O2/Dist_${i}/dmc/dmc.s001.scalar.dat | sed s/"runs\/O2\/Dist_${i}\/dmc\/dmc  series 1  LocalEnergy           = "/""/g)
        
	echo  "$i        $y  $z" >>Data.dat
done


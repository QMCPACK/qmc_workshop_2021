#!/bin/bash

Output=Data_QMC_Error-Bar
echo "#blocks        Local Energy          Variance              ratio " >> ${Output}
for i in 1 2 3 4 5
do 
	let j=$i*$i*100
	echo -n "$j   ">>${Output}
	y=$(qmca -q ev -e 50 runs/Be2/cc-pvtz/SCAN/dmc_error-bar/dmc_error${i}.s001.scalar.dat  |tail -n1|  sed s/"runs\/Be2\/cc-pvtz\/SCAN\/dmc_error-bar\/dmc_error${i}  series 1 "/""/g)
	echo "$y  " >>${Output}

done


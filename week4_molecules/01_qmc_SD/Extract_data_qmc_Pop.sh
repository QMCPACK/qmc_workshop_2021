#!/bin/bash

Output=Data_QMC_Population
echo "#Population        Local Energy          Variance              ratio " >> ${Output}
for i in 64 128 256 512 1024 2048  
do 
	echo -n "$i   ">>${Output}
	y=$(qmca -q ev runs/Be2/cc-pvtz/SCAN/dmc_pop/dmc_pop${i}.s001.scalar.dat  |tail -n1|  sed s/"runs\/Be2\/cc-pvtz\/SCAN\/dmc_pop\/dmc_pop${i}  series 1 "/""/g)
	echo "$y  " >>${Output}

done


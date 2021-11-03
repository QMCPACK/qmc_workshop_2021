#!/bin/bash


echo "##Trial_WF            LDA                       PBE                       PBE0                     SCAN " >> Data_QMC
for i in cc-pvdz cc-pvtz cc-pvqz 
do 
	echo -n "$i   ">>Data_QMC
	for j in LDA PBE PBE0 SCAN
	do 
		y=$(qmca -q e runs/Be2/$i/$j/dmc/dmc.s001.scalar.dat | sed s/"runs\/Be2\/$i\/$j\/dmc\/dmc  series 1  LocalEnergy           =  "/""/g)
		echo -n "$y  " >>Data_QMC
	done
	echo "">>Data_QMC
done


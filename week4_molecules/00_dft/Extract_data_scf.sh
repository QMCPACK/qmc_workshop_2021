#/bin/bash/

echo "#Method          HF                 LDA                 PBE                PBE0             SCAN" >> Data_SCF
for j in cc-pvdz cc-pvtz cc-pvqz 
do 
	echo -n "$j" >> Data_SCF
	for i in HF LDA PBE PBE0 SCAN
	do  
		y=$(grep "converged SCF energy =" runs/Be2/$j/$i/SCF/scf.out | sed s/"converged SCF energy ="/""/g) 
		echo -n "$y  " >>Data_SCF 
	done
	echo " 0" >> Data_SCF
done 

#set terminal postscript enhanced color eps "Helvetica" 16 
#set ou "Be2-Total_Energy_SCF.eps"
set format y "%6.3f"
set key title "" center
#set key right center
set style histogram clustered gap 2 title textcolor lt -1
set style fill solid border -1
set title "Be_{2} Total Energy as a function of the method and basis-set" 

set bmargin 4
set xlabel offset 0,-1

set xlabel "Basis-set" font "Helvetica, 14"
set ylabel "Total Energy (Ha)" font "Helvetica, 14"




Ref =-29.33897 


plot [-0.5:2.5][-29.350:-28.36]  "Data_SCF" u 2:xticlabels(1) with linespoints ls 1  lc rgb "blue" ti "Hartree-Fock", \
             "Data_SCF" u 3:xticlabels(1) with linespoints ls 1 lc rgb "green" ti "LDA"         , \
             "Data_SCF" u 4:xticlabels(1) with linespoints ls 1 lc rgb "black" ti "PBE"         , \
             "Data_SCF" u 5:xticlabels(1) with linespoints ls 1 lc rgb "pink" ti "PBE0"        , \
             "Data_SCF" u 6:xticlabels(1) with linespoints ls 1 lc rgb "purple" ti "SCAN"         , \
             Ref  w l lc rgb "red" ti " Experimental= -29.33897 Ha"


pause -1	       

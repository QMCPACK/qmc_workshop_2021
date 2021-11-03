#set terminal postscript enhanced color eps "Helvetica" 16 
#set ou "Be2-Total_Energy.eps"
set format y "%6.3f"
set key title "" center
#set key right center
set style histogram clustered gap 2 title textcolor lt -1
set style fill solid border -1
set title "^{3}O_{2} Dissociation Energy" 

set bmargin 4
set xlabel offset 0,-1

set xlabel "Bond Length (A)" font "Helvetica, 14"
set ylabel "Dissociation Energy (Ha)" font "Helvetica, 14"




DFTRef =-15.881540316026
QMCRef =-15.870468
QMCErr=0.000260




plot [0.5:][:]       "Data.dat" u 1:($2-2*DFTRef) w linespoints  lc rgb "blue" ti "DFT"          , \
             "Data.dat" u 1:($3-2*QMCRef):(sqrt($5*$5+QMCErr*QMCErr)) w e  lc rgb "black" ti "DMC(SCAN)" , \
             "Data.dat" u 1:($3-2*QMCRef) w l  lc rgb "black" noti 

pause -1	       

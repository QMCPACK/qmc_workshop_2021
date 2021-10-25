#set terminal postscript enhanced color eps "Helvetica" 16 
#set ou "Walker_population.eps"
set format y "%6.3f"
set key title "" center
#set key right center
set style histogram clustered gap 2 title textcolor lt -1
set style fill solid border -1
set title "DMC Walker population analysis" 

set bmargin 4
set xlabel offset 0,-1

set xlabel "Walkers" font "Helvetica, 14"
set ylabel "Total Energy (Ha)" font "Helvetica, 14"


plot   "Data_QMC_Population" u 1:2:4 w e  lc rgb "blue" noti 

pause -1	       

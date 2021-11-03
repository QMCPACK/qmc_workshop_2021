#set terminal postscript enhanced color eps "Helvetica" 16 
#set ou "Block size.eps"
set format y "%6.3f"
set key title "" center
#set key right center
set style histogram clustered gap 2 title textcolor lt -1
set style fill solid border -1
set title "Error bar reduction" 

set bmargin 4
set xlabel offset 0,-1

set xlabel "SQRT(Nb Ref-Blocks)" font "Helvetica, 14"
set ylabel "Normalized error bar (Ha)" font "Helvetica, 14"

norm=0.002040

ax=2
ay=0.000881
              
plot   "Data_QMC_BLOCKS" u (sqrt($1/100)):(norm/$4) w linespoints  lc rgb "blue" noti, \
             '+'         u (ax):(norm/ay) noti 

pause -1	       

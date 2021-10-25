#set terminal postscript enhanced color eps "Helvetica" 16 
#set ou "Be2-Total_Energy.eps"
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



plot [-0.5:2.5][-29.34:-29.31]       "Data_QMC" u 2:4:xticlabels(1) w e  lc rgb "blue" ti "DMC(LDA)"          , \
             "Data_QMC" u 5:7:xticlabels(1) w e  lc rgb "black" ti "DMC(PBE)"         , \
             "Data_QMC" u 8:10:xticlabels(1) w e lc rgb "pink" ti "DMC(PBE0)"         , \
             "Data_QMC" u 11:13:xticlabels(1) w e lc rgb "purple" ti "DMC(SCAN)"      , \
             "Data_QMC" u 2:xticlabels(1) w l  lc rgb "blue"  ti ""                   , \
             "Data_QMC" u 5:xticlabels(1) w l  lc rgb "black" ti ""         , \
             "Data_QMC" u 8:xticlabels(1) w l lc rgb "pink" ti ""         , \
             "Data_QMC" u 11:xticlabels(1) w l lc rgb "purple" ti ""     , \
             Ref  w l lc rgb "red" ti "Reference = -29.33897 Ha"

pause -1	       

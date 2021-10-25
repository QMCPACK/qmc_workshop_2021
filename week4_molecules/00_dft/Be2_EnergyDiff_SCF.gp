# set terminal pngcairo  transparent enhanced font "arial,10" fontscale 1.0 size 600, 400 
# set output 'histograms.2.png'
set boxwidth 0.9 absolute
set style fill   solid 1.00 border lt -1
set key fixed right top vertical Right noreverse noenhanced autotitle nobox
set style histogram clustered gap 1 title textcolor lt -1
set datafile missing '-'
set style data histograms
set xtics border in scale 0,0 nomirror rotate by -45  autojustify
set xtics  norangelimit 
set xtics   ()
set title "Be_{2} Total Energy as a function of the method and basis-set" 

set xlabel "Basis-set" font "Helvetica, 14"
set ylabel "Energy error to reference (mHa)" font "Helvetica, 14"

#plot 'Data_SCF' using 2:xtic(1) ti col, '' u 3 ti col, '' u 4 ti col, '' u 5 ti col, '' u 6 ti col, '' u 7 ti col
#pause -1

Ref =-29.33897
plot [-0.5:2.5]  "Data_SCF" u ($2-Ref)*1000:xticlabels(1)  ti "Hartree-Fock", \
                 "Data_SCF" u ($4-Ref)*1000:xticlabels(1)  ti "PBE"         , \
                 "Data_SCF" u ($5-Ref)*1000:xticlabels(1) ti "PBE0"        , \
                 "Data_SCF" u ($6-Ref)*1000:xticlabels(1)  ti "SCAN"



pause -1	       

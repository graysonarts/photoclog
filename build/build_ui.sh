#!/bin/sh

cd piui/piui/ui
for n in `ls *.ui`; do
   outfile=`echo $n | sed s/.ui$/.py/`
   pyuic4 -xo $outfile $n 
done

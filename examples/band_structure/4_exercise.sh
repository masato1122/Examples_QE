##
## You can use following commands for exercises.
##
for i in `seq 0 5`; do
    
    ### calculation for integer
    ecut=`expr 20 + 10 \* $i`
    
    ### calculation for double
    ecut=`echo "20. + 10. * $i" | bc -l`
    
    echo " $i : $ecut"

done


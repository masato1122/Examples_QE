
### output file name
ofile=energy.txt
echo "# nk energy[Ry]" > $ofile
for nk in 2 4 6 8; do
     
    ### modified lattice parameter
    sh mkscf.sh $nk
    
    ##mpirun -np 4 pw.x < scf.in > scf_${i}.out
    pw.x < scf.in > scf_${nk}.out
    
    ### output a result
    line=`cat scf_${i}.out | grep energy | grep !`
    data=(`echo "$line" | tr -s '/' ' '`)
    ene=${data[4]}
    echo $nk $ene
    echo $nk $ene >> $ofile
done


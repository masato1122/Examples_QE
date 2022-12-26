
### initial lattice parameter
alat0=10.26310

### output file name
ofile=energy.txt
echo "# num alat[Bohr] energy[Ry]" > $ofile
for i in `seq -5 15`; do
    
    echo "== $i =="
    
    ### modified lattice parameter
    alat=`echo "$alat0 + $i * 0.01" | bc -l`
    sh mkscf.sh $alat
    
    ##mpirun -np 4 pw.x < scf.in > scf_${i}.out
    pw.x < scf.in > scf_${i}.out
    
    ### output a result
    line=`cat scf_${i}.out | grep energy | grep !`
    data=(`echo "$line" | tr -s '/' ' '`)
    ene=${data[4]}
    echo $i $alat $ene
    echo $i $alat $ene >> $ofile
done

python fit.py


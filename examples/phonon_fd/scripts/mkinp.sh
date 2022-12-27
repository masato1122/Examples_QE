
### make an input script
python ../../tools/mk_pwinput.py \
    --filename ../../Si.cif \
    --pseudo_dir ../pseudo \
    --outdir ./out \
    --property scf \
    --reciprocal_density 20 \
    --primitive 0

rm pp.in

echo ""
echo " Modify scf.in and rename Si.in"
echo ""

ph.x < ph_G.in | tee ph_G.out
ph.x < ph_X.in | tee ph_X.out
ph.x < ph.in | tee ph.out
q2r.x < q2r.in | tee q2r.out

matdyn.x < band.in | tee band.out
python ../tools/plot_phband.py --file_band Si.freq

matdyn.x < dos.in | tee dos.out
python ../tools/plot_dos.py -f Si.dos


DEVICE?=5CEBA4F23C7
QSF=de0cv_pins.qsf

%.v: %.py
	python3.8 $^

%.json: %.v
	yosys -p "synth_intel_alm -nobram -nolutram -top toplevel -nodsp; write_json $@" $^

%.rbf: %.json ${QSF}
	nextpnr-mistral --parallel-refine --device ${DEVICE} --json $< --qsf ${QSF} --router router2 --rbf $@

%.prog: %.rbf
	openFPGALoader -b de0 toplevel.rbf

clean:
	rm -f *.json *.rbf *.v

.PRECIOUS: %.json %.rbf %.v

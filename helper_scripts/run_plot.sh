#!/usr/bin/bash
# runs plot cer & log using tsv files from training

TRIAL="$1"
if [ -z "$1" ] ; then
	echo "Error: No trial argument given"
	exit 1
fi

cd ~/ocr_projects/tesstrain

if [ ! -d tsv ] ; then
	echo "Error: No tsv folder found"
	exit 1
elif [ ! -f tsv/iteration_"$TRIAL".tsv -o ! -f tsv/checkpoint_"$TRIAL".tsv -o ! -f tsv/eval_"$TRIAL".tsv -o ! -f tsv/eval_all_"$TRIAL".tsv -o ! -f tsv/sub_"$TRIAL".tsv ] ; then
	echo "Error: Not all required tsv files present in tsv directory"
	exit 1
fi


source .venv/bin/activate

python3 plot_cer.py amh-layer_"$TRIAL".plot_cer.png amh-layer_"$TRIAL" tsv/iteration_"$TRIAL".tsv tsv/checkpoint_"$TRIAL".tsv tsv/eval_all_"$TRIAL".tsv tsv/sub_"$TRIAL".tsv tsv/eval_all_"$TRIAL".tsv

if [ "$?" != 0 ] ; then
	deactivate
	echo "Error in plot_cer"
	exit 1
fi

python3 plot_log.py amh-layer_"$TRIAL".plot_log.png amh-layer_"$TRIAL" tsv/iteration_"$TRIAL".tsv tsv/checkpoint_"$TRIAL".tsv tsv/eval_all_"$TRIAL".tsv tsv/sub_"$TRIAL".tsv

if [ "$?" != 0 ] ; then
	deactivate
	echo "Error in plot_log"
	exit 1
fi

mv amh-layer_"$TRIAL".plot*.png "$d/a"

deactivate


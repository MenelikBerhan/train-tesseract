#!/usr/bin/bash
# runs plot cer & log using tsv files from training

cd ~/ocr_projects/tesstrain

if [ ! -d tsv ] ; then
	echo "Error: No tsv folder found"
	exit 1
elif [ ! -f tsv/iteration_6.tsv -o ! -f tsv/checkpoint_6.tsv -o ! -f tsv/checkpoint_6.tsv -o ! -f tsv/eval_all_6.tsv -o ! -f tsv/sub_6.tsv ] ; then
	echo "Error: Not all required tsv files present in tsv directory"
	exit 1
fi

source .venv/bin/activate

python3 plot_cer.py amh-layer_6.plot_cer.png amh-layer_6 tsv/iteration_6.tsv tsv/checkpoint_6.tsv tsv/eval_all_6.tsv tsv/sub_6.tsv tsv/eval_all_6.tsv

python3 plot_log.py amh-layer_6.plot_log.png amh-layer_6 tsv/iteration_6.tsv tsv/checkpoint_6.tsv tsv/eval_all_6.tsv tsv/sub_6.tsv

mv amh-layer_6.plot*.png "$d/a"

deactivate

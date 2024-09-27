#!/bin/bash
# Script to check if lstmtraining is running & if not start it.
# To be used for a cron job using corntab -e

a="$(pgrep lstmtraining)"
if [ "$?" == 0 ] ; then
	echo "$(date) : Running"
else
	echo "$(date) : Not Running"

	# check if lstmtraining was killed by OOM
	killed_info="$(dmesg -T | grep kill | grep lstmtraining)"

	# restart lstmtraining
	if [ "$?" == 0 ] ; then
		echo "$(date) : Killed by OOM: $killed_info"

		cd /home/menelikberhan/train-tesseract/tesstrain && \
		source ../.venv/bin/activate && \
		lstmtraining \
			--debug_interval 0 \
			--traineddata "../data/amh-scratch/amh-scratch.traineddata" \
			--model_output "../data/amh-scratch/checkpoints/amh-scratch" \
			--train_listfile "../data/amh-scratch/list.train" \
			--eval_listfile "../data/amh-scratch/list.eval" \
			--learning_rate 0.002 \
			--target_error_rate 0.01 \
			--net_spec '[1,48,0,1 Ct3,3,16 Mp3,3 Lfys64 Lfx96 Lrx96 Lfx512 O1c335]' \
			--max_iterations -2 >> ../out_lstmtrain_chron_1 2>&1
	fi
fi



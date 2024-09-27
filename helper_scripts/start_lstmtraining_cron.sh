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
			--traineddata "../data/amh-layer/amh-layer.traineddata" \
			--continue_from "../data/amh/amh-layer.lstm" \
			--model_output "../data/amh-layer/checkpoints/amh-layer" \
			--train_listfile "../data/amh-layer/list.train" \
			--eval_listfile "../data/amh-layer/list.eval" \
			--learning_rate 0.001 \
			--target_error_rate 0.01 \
			--net_spec '[Lfys64 Lfx96 Lrx96 Lfx256 O1c335]' \
			--append_index 2 \
			--max_iterations -2 >> ../out_lstmtrain_chron_8 2>&1
	fi
fi



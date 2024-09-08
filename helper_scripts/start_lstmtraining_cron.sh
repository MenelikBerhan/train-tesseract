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
			--continue_from "../data/amh-layer/checkpoints/amh-layer_checkpoint" \
			--learning_rate 0.001 \
			--model_output "../data/amh-layer/checkpoints/amh-layer" \
			--train_listfile "../data/amh-layer/list.train" \
			--eval_listfile "../data/amh-layer/list.eval" \
			--max_iterations -1 \
			--target_error_rate 0.01 \
			--net_spec '[Lfx256 O1c336]' \
			--append_index 5 \
			--max_image_MB 3200 \
			--net_mode 192 \
			--momentum 0.5  \
			--adam_beta 0.999 >> ../out_lstmtrain_chron_2 2>&1
	fi
fi

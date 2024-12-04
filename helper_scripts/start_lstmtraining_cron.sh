#!/bin/bash
# Script to check if lstmtraining is running & if not start it.
# To be used for a cron job using corntab -e. Example: to check every 30 mins:
#0,30 * * * * ~/train-tesseract/helper_scripts/start_lstmtraining_cron.sh >> ~/train-tesseract/cron.log 2>&1

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

		# delete users crontab (avoid second start incase this fails)
		crontab -r

		# copy last checkpoint as a backup
		cp ~/train-tesseract/data/amh-layer/checkpoints/amh-layer_checkpoint \
			~/train-tesseract/bak/amh-layer_checkpoint-"$(date | tr ' ' '_' | tr ':' '-')"

		cd /home/menelikberhan/train-tesseract/tesstrain && \
		lstmtraining \
			--debug_interval 0 \
			--traineddata "../data/amh-layer/amh-layer.traineddata" \
			--continue_from "../data/amh/amh-layer.lstm" \
			--model_output "../data/amh-layer/checkpoints/amh-layer" \
			--train_listfile "../data/amh-layer/list.train" \
			--learning_rate 0.001 \
			--target_error_rate 0.001 \
			--net_spec '[Lfx192 O1c335]' \
			--append_index 5 \
			--max_iterations 2500000 >> ../out_lstmtrain_chron_23 2>&1
	fi
fi



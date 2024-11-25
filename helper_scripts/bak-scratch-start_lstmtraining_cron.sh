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

		# copy last checkpoint as a backup
                cp ~/train-tesseract/data/amh-layer/checkpoints/amh-layer_checkpoint \
                        ~/train-tesseract/bak/amh-layer_checkpoint-"$(date | tr ' ' '_')"

		cd /home/menelikberhan/train-tesseract/tesstrain && \
		source ../.venv/bin/activate && \
		lstmtraining \
			--debug_interval 0 \
			--traineddata ../data/amh-layer/amh-layer.traineddata \
			--model_output ../data/amh-layer/checkpoints/amh-layer \
			--train_listfile ../data/amh-layer/list.train \
			--eval_listfile ../data/amh-layer/list.eval \
			--learning_rate 0.001 \
			--target_error_rate 0.0001 \
			--net_spec '[1,48,0,1 Ct3,3,16 Mp3,3 Lfys64 Lfx96 Lrx96 Lfx384 O1c335]' \
			--max_iterations -4 >> ../out_lstmtrain_chron_16 2>&1
	fi
fi


# --net_spec [1,36,0,1 Ct3,3,16 Mp3,3 Lfys48 Lfx96 Lrx96 Lfx192 O1c335]

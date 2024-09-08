#!/bin/bash
# Script to check if make is running & if not start it.
# To be used for a cron job using corntab -e

a="$(pgrep make)"
if [ "$?" == 0 ] ; then
	echo "$(date) : Running"
else
	echo "$(date) : Not Running"
	cd /home/menelikberhan/train-tesseract/tesstrain && \
	source ../.venv/bin/activate && \
	OMP_THREAD_LIMIT=1 TESSDATA_PREFIX=../data/tessdata make lists \
	MODEL_NAME=amh-layer START_MODEL=amh DATA_DIR=../data \
	TESSDATA=../data/tessdata LEARNING_RATE=0.0001 \
	RATIO_TRAIN=0.999 EPOCHS=1 >> ../out_create_lstmf_chron 2>&1
fi

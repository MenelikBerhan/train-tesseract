#!/bin/bash
# Script to check if make is running & if not start it.
# To be used for a cron job using corntab -e


a="$(pgrep make)"
if [ "$?" == 0 ] ; then
        echo "$(date) : Running"
else
        echo "$(date) : Not Running"

        # check if `make` was killed by OOM
        killed_info="$(dmesg -T | grep kill | grep make)"

        # restart `make`
        if [ "$?" == 0 ] ; then
                echo "$(date) : Killed by OOM: $killed_info"

		source ../.venv/bin/activate && \

		TESSDATA_PREFIX=../data/tessdata make lists \
		MODEL_NAME=amh-layer START_MODEL=amh \
		DATA_DIR=../data TESSDATA=../data/tessdata \
		EPOCHS=1 >> ../out_perpare_train_data_chron_1 2>&1
	fi
fi

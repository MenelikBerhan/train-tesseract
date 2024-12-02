#!/bin/bash
# Script to check if python -m tesstrain is running & if not start it.
# To be used for a cron job using corntab -e

a=$(pgrep -f "python -m tesstrain" | wc -l )
if [ "$a" == 2 ] ; then
        echo "$(date) : Two Procs Running"
else

        cd /home/menelikberhan/train-tesseract/generate_ground_truth/using-tesstrain/

        echo "$(date) : Starting python -m tesstrain"

        source ../../.venv/bin/activate

        ./run_tesstrain.sh
fi


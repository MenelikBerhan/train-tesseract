#!/usr/bin/bash
# runs lstmeval on batch of best chekpoint|traineddata files
# and generate lstmeval.tsv for plot.cer.py


TRIAL="$1"
CHECKPOINTS_DIR="checkpoints"
#STARTER_TRAINED_DATA="$TRIAL/amh-layer.traineddata"
STARTER_TRAINED_DATA="$TRIAL/amh-scratch.traineddata"
#TRAINEDDATA_DIR="$TRIAL/checkpoint_traineddatas"
TRAINEDDATA_DIR="."
LSTMF_FILES_DIR="eval_files/lstmeval_files_6"
EVAL_CER_DIR="$TRIAL/cer_eval"
FROM_CHECKPOINT="0"
FROM_TRAINED_DATA="1"
GENERATE_EVAL_TSV="1"


if [ -z "$1" ] ; then
	echo "Error: No trial directory path given"
	exit 1
elif [ ! -d "$1" ] ; then
	echo "Error: No directory found at given path $1"
	exit 1
elif [ "$FROM_CHECKPOINT" == "1" -a ! -f "$STARTER_TRAINED_DATA" ] ; then
	echo "Error: No Starter Traineddata in tiral directory $TRIAL"
	exit 1
fi

# create traineddata from checkpoints
if [ "$FROM_CHECKPOINT" == "1" ] ; then
	a_c=$(ls "$CHECKPOINTS_DIR"/*.checkpoint | sort -n )

	for c in $a_c ; do \
	lstmtraining --stop_training \
		--traineddata "$STARTER_TRAINED_DATA" --continue_from "$c" \
		--model_output "$TRAINEDDATA_DIR"/"$(basename -s .checkpoint $c )".traineddata ; done
fi

# run lstmeval on each traineddata
if [ "$FROM_CHECKPOINT" == "1" -o  "$FROM_TRAINED_DATA" == "1" ] ; then

	ls "$LSTMF_FILES_DIR"/*.lstmf > lstmeval_lists/list.eval
	a_t="$(ls $TRAINEDDATA_DIR/*.traineddata | sort -n )"

	for t in $a_t ; do \
		echo "Running lstmeval for $t"

		SUFF="$(basename -s .traineddata $t | cut -d '_' -f2-4)" &&  \
		lstmeval --verbosity=0 --model "$t" \
			--eval_listfile lstmeval_lists/list.eval 2>&1 | \
			grep "^BCER eval" > "$EVAL_CER_DIR"/eval_"$SUFF".txt ; done
fi

# output lstmeval.tsv
if [ "$GENERATE_EVAL_TSV" == "1" ] ; then
	echo -e 'LearningIteration\tTrainingIteration\tEvalCER\tCheckpointCER' > lstmeval_"$TRIAL".tsv
	a_e=$(ls "$EVAL_CER_DIR"/* | sort -nr)

	for f in $a_e ; do \
		iter="$(basename -s .txt $f | cut -d '_' -f2-4)"
		eval=$(egrep -o "[0-9\.]{5,}," "$f")
		echo "$eval" "$iter" | tr ',_' ' '| awk '{print $3"\t"$4"\t"$1"\t"$2}' >> lstmeval_"$TRIAL".tsv ; done

	cp lstmeval_"$TRIAL".tsv "$d/a"
	mv lstmeval_"$TRIAL".tsv "$TRIAL"/tsv

fi

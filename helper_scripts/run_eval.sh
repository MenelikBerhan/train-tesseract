#!/usr/bin/bash

# check if a checkpoint or traineddata file arg is passed
if [ -z "$1" ] ; then
	echo "Error: Missing checkpoint or traineddata file path"
	exit 1
elif [ ! -f "$1" ] ; then
	echo "Error: Given Checkpoint or traineddata file Doesn't Exist!"
	exit 1
fi

# check if a trial directory is passed (to move all results finally)
if [ -z "$2" ] ; then
	echo "Error: Missing trial dirctory path"
	exit 1
elif [ ! -d "$2" ] ; then
	echo "Error: Given Trial Directory Doesn\'t Exist!"
	exit 1
fi

STARTER_TRAINEDDATA="$2/amh-scratch.traineddata"

if [ "$(echo $1 | grep '\.checkpoint$')" ] ; then
	# for checkpoints check if starter traineddata exist in trial directory
	if [ ! -f "$STARTER_TRAINEDDATA" ] ; then
		echo "Error: Starter traineddata Doesn't Exist in Trial Directory"
		exit 1
	fi

	# set model name after removing learning & train iteration, and `.checkpoint` extension
	MODEL="$(basename $1 .checkpoint )"

	# create traineddata from checkpoint
	lstmtraining --stop_training \
		--traineddata "$STARTER_TRAINEDDATA" \
		--continue_from "$1" \
		--model_output "$MODEL".traineddata

	# path to the created traineddata file
	MODEL_PATH="./"

elif [ "$(echo $1 | grep '\.traineddata')" ] ; then
	# set model name after removing `.traineddata extension
	MODEL="$(basename $1 .traineddata)"

	# set path to traineddata file
	MODEL_PATH="$(echo $1 | egrep -o '.*/')"
	if [ "$?" != 0 ] ; then
		MODEL_PATH="./"
	fi
else
	echo "Error: Must Provide a Chekpoint or Traineddata file"
	exit 1
fi

#echo "TEST $MODEL   $MODEL_PATH"

# run tesseract using model on sets of images
tesseract --tessdata-dir "$MODEL_PATH" "tesseract_inputs/in_samples" "$MODEL"_result_samples -l "$MODEL"
tesseract --tessdata-dir "$MODEL_PATH" "tesseract_inputs/in_kidane" "$MODEL"_result_kidane -l "$MODEL"
tesseract --tessdata-dir "$MODEL_PATH" "tesseract_inputs/in_eval_6" "$MODEL"_result_eval_6 -l "$MODEL" --psm 7

if [ "$?" != 0 ] ; then
        exit 1
fi

# ocr result text file names
RES_SAMPLES="$MODEL"_result_samples.txt
RES_KIDANE="$MODEL"_result_kidane.txt
RES_EVAL_6="$MODEL"_result_eval_6.txt

# run lstmeval on lstmf files list of synthetic images from train trial 5
lstmeval --model "$MODEL_PATH/$MODEL".traineddata --eval_listfile lstmeval_lists/list.eval_5 --verbosity 2 >& eval_synth_"$MODEL"_5.log

# run lstmeval on lstmf files list of synthetic images from train trial 6
lstmeval --model "$MODEL_PATH/$MODEL".traineddata --eval_listfile lstmeval_lists/list.eval_6 --verbosity 2 >& eval_synth_"$MODEL"_6.log

# run ocrevalUation to compare ocr results with ground truth files
java -cp ocr-evaluation-tools/ocrevalUAtion-1.3.4-jar-with-dependencies.jar eu.digitisation.Main \
	-gt ground_truths/ground_samples.txt -e utf8  -ocr "$RES_SAMPLES" -e utf8 -o evlU_"$MODEL"_samples.html

java -cp ocr-evaluation-tools/ocrevalUAtion-1.3.4-jar-with-dependencies.jar eu.digitisation.Main \
	-gt ground_truths/ground_kidane.txt -e utf8 -ocr "$RES_KIDANE" -e utf8 -o evlU_"$MODEL"_kidane.html

#java -cp ocr-evaluation-tools/ocrevalUAtion-1.3.4-jar-with-dependencies.jar eu.digitisation.Main \
#	-gt ground_truths/ground_eval_6.txt -e utf8 -ocr "$RES_EVAL_6" -e utf8 -o evlU_"$MODEL"_eval_6.html

# run char & word accuracy, and synctext by comparing groundtruth with ocr results
accuracy ground_truths/ground_samples.txt "$RES_SAMPLES" acc_"$MODEL"_samples.txt
accuracy ground_truths/ground_kidane.txt "$RES_KIDANE" acc_"$MODEL"_kidane.txt
accuracy ground_truths/ground_eval_6.txt "$RES_EVAL_6" acc_"$MODEL"_eval_6.txt

wordacc ground_truths/ground_samples.txt "$RES_SAMPLES" wrd_acc_"$MODEL"_samples.txt
wordacc ground_truths/ground_kidane.txt "$RES_KIDANE" wrd_acc_"$MODEL"_kidane.txt
#wordacc ground_truths/ground_eval_6.txt "$RES_EVAL_6" wrd_acc_"$MODEL"_eval_6.txt

#synctext ground_truths/ground_samples.txt "$RES_SAMPLES" > sync_"$MODEL"_samples.txt
#synctext ground_truths/ground_kidane.txt "$RES_KIDANE" > sync_"$MODEL"_kidane.txt
#synctext ground_truths/ground_eval_6.txt "$RES_EVAL_6" > sync_"$MODEL"_eval_6.txt

# copy results & eval files to windows dir and move to trial folder
cp "$RES_SAMPLES" "$RES_KIDANE" "$RES_EVAL_6" eval_synth_"$MODEL"_5.log eval_synth_"$MODEL"_6.log \
	evlU_"$MODEL"_samples.html evlU_"$MODEL"_kidane.html evlU_"$MODEL"_eval_6.html \
	acc_"$MODEL"_samples.txt acc_"$MODEL"_kidane.txt acc_"$MODEL"_eval_6.txt \
	wrd_acc_"$MODEL"_samples.txt wrd_acc_"$MODEL"_kidane.txt wrd_acc_"$MODEL"_eval_6.txt \
	sync_"$MODEL"_samples.txt sync_"$MODEL"_kidane.txt  sync_"$MODEL"_eval_6.txt \
	"$d"/a

#if [ "$?" != 0 ] ; then
#	exit 1
#fi

mv "$RES_SAMPLES" "$RES_KIDANE" "$RES_EVAL_6" eval_synth_"$MODEL"_5.log eval_synth_"$MODEL"_6.log \
	evlU_"$MODEL"_samples.html evlU_"$MODEL"_kidane.html evlU_"$MODEL"_eval_6.html \
	acc_"$MODEL"_samples.txt acc_"$MODEL"_kidane.txt acc_"$MODEL"_eval_6.txt \
	wrd_acc_"$MODEL"_samples.txt wrd_acc_"$MODEL"_kidane.txt wrd_acc_"$MODEL"_eval_6.txt \
	sync_"$MODEL"_samples.txt sync_"$MODEL"_kidane.txt  sync_"$MODEL"_eval_6.txt \
	"$2"/my_eval

# move created traineddata to trial dir
if [ "$(echo $1 | grep '\.checkpoint$')" ] ; then
	mv "$MODEL".traineddata "$2"/checkpoint_traineddatas
fi

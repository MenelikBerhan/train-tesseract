#!/usr/bin/bash
# run tesseract on batch images using given traineddata path

if [ -z "$1" ] ; then
	echo "Error: No traineddata path argument given"
	exit 1
elif [ ! -f "$1" ] ; then
	echo "Error: No traineddata at given path"
	exit 1
fi

#MODEL_PATH=$(egrep -o ".+/" $1)
MODEL_PATH="$(echo $1 | egrep -o '.*/')"

if [ -z "$MODEL_PATH" ] ; then
	MODEL_PATH="./"
fi

MODEL="$(basename $1 .traineddata)"

#echo "$MODEL_PATH" "$MODEL"
tesseract --tessdata-dir "$MODEL_PATH" tesseract_inputs/civil_code_in "$MODEL"_result_civil_code -l "$MODEL"
tesseract --tessdata-dir "$MODEL_PATH" tesseract_inputs/addis_zemen_in "$MODEL"_result_addiszemen -l "$MODEL"

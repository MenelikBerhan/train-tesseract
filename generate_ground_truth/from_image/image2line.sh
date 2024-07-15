#!/bin/bash

# Source https://github.com/tesseract-ocr/tesstrain/issues/7#issuecomment-419714852

# Creates files needed for tesseract training.
# Takes a scanned image and:
#   * run tesseract with hocr option on it an produce an hocr output,
#   * run hocr tools (hocr-extract-images) to split the hocr output into lines and
#   * +produce a tif image and a text file for each line.
# The ground truth (text file content) needs to be checked/updated manually.

# ---------------------------------------------------------------
# Make sure hocr-tools and rename are installed
#   sudo pip install hocr-tools or sudo apt-get install hocr-tools
#   sudo apt-get install rename

# setup a python venv using python3 -m venv .venv
# ---------------------------------------------------------------

# source dir of images
SOURCE="./images/"

# language
lang=amh

# images extension
set -- "$SOURCE"*.jpg

for img_file; do
    echo -e  "\r\n File: $img_file"
    # run tesseract on image file to produce hocr output
    OMP_THREAD_LIMIT=1 tesseract "${img_file}" "${img_file%.*}"  --psm 6  --oem 1  -l $lang -c page_separator='' hocr

    source .venv/bin/activate
    # # runs hocr-extract-images on the hocr output and create an image and a text file for each line
    PYTHONIOENCODING=UTF-8 hocr-extract-images -b ./images/ -p "${img_file%.*}"-%03d.exp0.tif  "${img_file%.*}".hocr 
    deactivate
done

# rename generated text file from *.txt to *.gt.txt
rename s/exp0.txt/exp0.gt.txt/ ./images/*exp0.txt

echo "Image files converted to tif. Check/Correct the text files for erros before starting training."

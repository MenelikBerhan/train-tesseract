#!/usr/bin/env python3
# source: https://github.com/astutejoe/tesseract_tutorial
# creates a text, image(tif) and box file for each line in a text file
# output to be used as a ground truth for training tesseract

import os
import random
import pathlib
import subprocess

training_text_file = 'training_text/kidane-introduction-clean.txt'

lines = []

with open(training_text_file, 'r') as input_file:
    for line in input_file:
        lines.append(line.strip())

output_directory = 'data/amh-old4-ground-truth'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

random.shuffle(lines)

# list of fonts to use (must be found in --fonts_dir param of text2image)
fonts = (
    'Abyssinica SIL', 'Droid Sans Ethiopic', 'Droid Sans Ethiopic Bold',
    'FreeSerif', 'Noto Sans Ethiopic', 'Noto Sans Ethiopic Bold')

# no of lines to process from txt file (comment out for all)
count = 10
lines = lines[:count]

# input file name without extention
input_file_name = pathlib.Path(training_text_file).stem

for font in fonts:
    # remove space from font name
    font_name = "-".join(font.split())

    # output files (box, text & image) base path for each font
    output_files_base_name = os.path.join(
        output_directory, f'{input_file_name}_{font_name}')

    line_count = 0
    for line in lines:
        # output files (box, text & image) base path for each line
        line_files_base_name = f'{output_files_base_name}_{line_count}'

        line_training_text = f'{line_files_base_name}.gt.txt'
        with open(line_training_text, 'w') as output_file:
            output_file.writelines([line])

        subprocess.run([
            'text2image',
            f'--font={font}',
            '--fonts_dir=../fonts',
            f'--text={line_training_text}',
            f'--outputbase={line_files_base_name}',
            '--max_pages=1',
            '--strip_unrenderable_words',
            '--leading=0',
            '--xsize=1200',     # change xsize & ysize based on line length
            '--ysize=80',       # +  to minimize margin spaces around text
            '--char_spacing=0',
            '--exposure=0',
            '--unicharset_file=langdata/amh.unicharset',
            '--margin=0'
        ])

        line_count += 1

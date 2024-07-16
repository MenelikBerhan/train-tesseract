#!/usr/bin/env python3
# source: https://github.com/astutejoe/tesseract_tutorial
# creates a text, image(tif) and box file for each line in a text file
# output to be used as a ground truth for training tesseract

from datetime import datetime
import os
import pathlib
import random
import subprocess

from glob import iglob

OVERWRITE_FILES = True
training_text_file = './combined_80_chars_line.txt'

output_directory = './amh-old-ground-truth'

output_dir_path = pathlib.Path(output_directory)

if not output_dir_path.is_dir():
    os.mkdir(output_directory)
else:
    # move to backup folder
    if list(iglob(output_dir_path.joinpath('*.txt').as_posix())) and\
            not OVERWRITE_FILES:
        t = datetime.now().strftime('%b-%d-%H:%M:%S')
        move_to = pathlib.Path(f'./bak-ground-truth-{t}')
        os.renames(output_directory, move_to)
        os.mkdir(output_directory)
        print(f'Moved old files to: "{move_to}"')
    else:
        # confirm overwrite
        overwrite = input(
            f'About To OVERWRITE files in"{output_dir_path}"\nYes(Y) | No(N): ')
        if not overwrite in ['Yes', 'Y']:
            exit(1)
        print(f'Overwriting files in "{output_dir_path}"')

lines = []

with open(training_text_file, 'r') as input_file:
    for line in input_file:
        lines.append(line.strip())

rand = random.Random(0)
rand.shuffle(lines)

# list of fonts to use (must be found in --fonts_dir param of text2image)
# to install fonts: copy to `/usr/share/fonts` and `fc-cache -fv`
# to list all available fonts: `fc-list : family style | sort`
fonts = (
    # from okfonts of lstmdata/amh (except droid sans)
    'Abyssinica SIL', 'FreeSerif',
    'Noto Sans Ethiopic', 'Noto Sans Ethiopic Bold',
    # from washera fonts
    'Ethiopia Jiret', 'Ethiopic WashRa Bold, Bold', 'Ethiopic Wookianos',
    'Ethiopic Zelan', 'Ethiopic Tint',
    # from legally-free-geez-fonts-v1_0_0
    'A0 Addis Abeba Unicode', 'Ethiopic Dire Dawa',
)
"""
# omitted fonts (don't support all Ethiopic chars [esp. geez no.s]
# or allowed non-Ethiopic like brackets)

# from okfonts of lstmdata/amh (except droid sans)
'Droid Sans Ethiopic'

# from washera fonts
'Ethiopic Fantuwua',    # very similar to 'Ethiopic Wookianos'

# from legally-free-geez-fonts-v1_0_0
"ahabesha'stypewriter", # geez no.s, brackets
'Chiret',               # geez no.s, brackets
'Geez Handwriting', 'Geez Handwriting Bold',    # geez no.s
'Shiromeda',    # similar to 'a0-aa-unicode' & chars like `<<`
"""
# no of lines to process from txt file (comment out for all)
count = 1000
lines = lines[:count]

# input file name without extention
input_file_name = pathlib.Path(training_text_file).stem

# TODO: check if first loopin ove lines then fonts have difference
for font in fonts:
    # remove space and comma from font name
    font_name = "-".join([w.strip(',') for w in font.split()])

    # output files (box, text & image) base path for each font
    output_files_base_name = os.path.join(
        output_directory, f'{input_file_name}_{font_name}')

    line_count = 0
    for line in lines:
        # output files (box, text & image) base path for each line
        line_files_base_name = f'{output_files_base_name}_{line_count}'

        # write line to txt file
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
            '--leading=32',      # Inter-line space (in pixels) default:12
            '--xsize=3200',     # change xsize & ysize based on line length
            '--ysize=480',       # +  to minimize margin spaces around text
            '--char_spacing=0.2',  # Inter-character space in ems def:0
            '--exposure=0',
            '--unicharset_file=unicharset_files/Ethiopic.unicharset',
            # '--margin=0',
        ])

        line_count += 1

        # subprocess.run([
        #     'text2image',
        #     '--max_pages=1',
        #     '--strip_unrenderable_words',
        #     '--leading=32',
        #     '--xsize=3600',
        #     '--ysize=480',
        #     '--char_spacing=1.0',
        #     '--exposure=0',
        #     '--unicharset_file=langdata/eng.unicharset'
        # ])

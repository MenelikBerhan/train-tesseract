#!/usr/bin/env python3
"""
Combines all sub group txt files into one training text by shuffling lines.
"""

import os
import random
from glob import iglob

from constants import LINE_LENGTH


output_root_dir = "."
output_file_name = "amh-layer.training_txt"

# contains one txt file for each subgroup
input_root_dir = "./combined_txts"


# if output dir doesn't exist create one
if not os.path.isdir(output_root_dir):
    os.mkdir(output_root_dir)
else:
    # ask for confirmation
    response = input(f"Output dir {output_root_dir} exist. Continue? Y/N: ")
    if response != "Y":
        exit(1)

# set output file path
output_file_path = os.path.join(output_root_dir, output_file_name)

# check if output file already exists
if os.path.exists(output_file_path):
    response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
    if response != "Y":
        exit(1)

all_wrds = []
# to match all files in input dir
pathname = os.path.join(input_root_dir, "*")

# collect all words from each sub group in a list
for txt_file_path in iglob(pathname):

    # skip if not file path (dir)
    if not os.path.isfile(txt_file_path):
        continue

    with open(txt_file_path) as txt_file:
        for line in txt_file:
            # skip empty/space lines
            line = line.strip()
            if line == "":
                continue

            all_wrds.extend(line.split())


# shuffle words
random.Random(23).shuffle(all_wrds)

all_wrds_len = len(all_wrds)
wrd_index = 0  # current word index in list

# write to output file trimming line to max LINE_LENGTH chars
with open(output_file_path, "w") as output_file:
    while wrd_index < all_wrds_len:
        line = ""
        # concat words into line of LINE_LENGTH
        while len(line) + len(all_wrds[wrd_index]) < LINE_LENGTH:
            line += all_wrds[wrd_index] + " "
            wrd_index += 1
            if not wrd_index < all_wrds_len:
                break

        # write to output file
        if not line.isspace():
            output_file.write(line.strip() + "\n")

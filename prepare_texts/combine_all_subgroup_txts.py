#!/usr/bin/env python3
"""
Combines all sub group txt files into one training text by shuffling lines.
"""

import os
import random
from glob import iglob


output_root_dir = "./combined_txts"
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


all_lines = []
# to match all files in input dir
pathname = os.path.join(input_root_dir, "*")

# collect all lines from each sub group in a list
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

            all_lines.append(line)

# shuffle lines
random.Random(23).shuffle(all_lines)

# set output file path
output_file_path = os.path.join(output_root_dir, output_file_name)

# check if output file already exists
if os.path.exists(output_file_path):
    response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
    if response != "Y":
        exit(1)

# write to output file, adding newline aftr each line
with open(output_file_path, "w") as output_file:
    output_file.write("\n".join(all_lines))

#!/usr/bin/env python3
"""
Combines text files for dictionaries & word lists subgroups.
After filtering words using a treshold frequency, shuffles and
writes a maximum LINE_LENGTH lines to output file.
"""

import os
import re
from glob import iglob

# from pathlib import Path
import random

from constants import LINE_LENGTH, puncs_to_strip_for_freq


input_root_dir = "./cleaned_texts"
output_root_dir = "./combined_txts"

output_file_name = "dictionaries_and_word_lists"

# dirs in input root dir
input_sub_groups = {
    "word_lists",
    "dictionary_and_linguistic_books",
}

# if output dir doesn't exist create one
if not os.path.isdir(output_root_dir):
    os.mkdir(output_root_dir)
else:
    # ask for confirmation
    response = input(f"Output dir {output_root_dir} exist. Continue? Y/N: ")
    if response != "Y":
        exit(1)

all_wrds_dict = {}  # to store wrd freq. used to filter words
all_wrds = []  # to store words

# flter words based on freq, and store in list
for sub_grp in input_sub_groups:
    sub_grp = sub_grp.strip("/")  # for path.join

    # to match all txt file in sub group
    pathname = os.path.join(input_root_dir, sub_grp, "**", "*.txt")

    for txt_file_path in iglob(pathname, recursive=True):
        with open(txt_file_path) as txt_file:
            lines = txt_file.readlines()
            for line in lines:
                # strip unwanted non-Ethiopic puncs from each word
                wrds = [w.strip("()./-") for w in line.split()]

                # loop over each word
                for w in wrds:
                    # remove `-` used to show multiple forms of root words
                    if w.startswith("ተን-") and w.count("-") == 1:
                        w = w.replace("-", "")

                    # skip repetitive bible quotes used in dictionaries
                    if re.search(r"[\u1200-\u1368]{2,3}[\u1369-\u137c]{1,2}", w):
                        continue

                    # skip words with puncs that makes words unusable
                    if re.search(r"[\.\(\)\-\[\]]", w):
                        continue

                    # remove words with pecuilar Ethiopic lettern & no. comb
                    if re.search(r"(ድ|ተ|ገ|ቁ)[\u1369-\u137C]+", w):
                        continue

                    # replace Ethiopic no.s prefix with common form
                    if re.search(r"^ባ[\u1369-\u137C0-9]+", w):
                        w = "በ" + w[1:]
                    if re.search(r"^ካ[\u1369-\u137C0-9]+", w):
                        w = "ከ" + w[1:]

                    w_dict = w.strip("".join(puncs_to_strip_for_freq))

                    # for single char words, use max of 2 of each form (2*2<5)
                    if len(w_dict) == 1:
                        all_wrds_dict[w_dict] = all_wrds_dict.get(w_dict, 0) + 2

                    # for abbreviations, use only one of each form (1*4<5)
                    elif re.search(r"[\u1200-\u135a]+/[\u1200-\u135a]+", w_dict):
                        all_wrds_dict[w_dict] = all_wrds_dict.get(w_dict, 0) + 4

                    # for Ethiopic no.s with letter prefix & suffix, store one of each form
                    elif re.search(
                        r"^(ለ|ክ|በ|የ)?[\u1369-\u137C0-9]+(ኛ|ው|ት|ቱ|ና|ም|ሩ|ኝ|ኙ|ድ|ዱ)*",
                        w_dict,
                    ):
                        all_wrds_dict[w_dict] = all_wrds_dict.get(w_dict, 0) + 4

                    # for the rest store at most 4 of each form (4*1<5)
                    else:
                        all_wrds_dict[w_dict] = all_wrds_dict.get(w_dict, 0) + 1

                    # if word is below freq threshold add to list
                    if all_wrds_dict[w_dict] < 5:
                        all_wrds.append(w)

# shuffle words
random.Random(23).shuffle(all_wrds)

# set output file path
output_file_path = os.path.join(output_root_dir, output_file_name)

# check if output file already exists
if os.path.exists(output_file_path):
    response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
    if response != "Y":
        exit(1)

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

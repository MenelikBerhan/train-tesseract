#!/usr/bin/env python3
"""
Combines text files by sub groups. After wrapping lines to LINE_LENGTH
shuffles lines before writing to output file for the subgroup.
"""

import os
import re
from glob import iglob

from constants import LINE_LENGTH


output_root_dir = "./combined_txts"
input_root_dir = "./cleaned_texts"

# dirs in input root dir
input_sub_groups = {
    "articles",
    "books/religious_amh/",
    "enh_corpus_by_year",
}

# if output dir doesn't exist create one
if not os.path.isdir(output_root_dir):
    os.mkdir(output_root_dir)
else:
    # ask for confirmation
    response = input(f"Output dir {output_root_dir} exist. Continue? Y/N: ")
    if response != "Y":
        exit(1)

# combine texts by subgroup
for sub_grp in input_sub_groups:
    sub_grp = sub_grp.strip("/")  # for path.join

    # to match all txt file in sub group
    pathname = os.path.join(input_root_dir, sub_grp, "**", "*.txt")

    # collect all words for each sub group in a list (w/o shuffling)
    sub_group_words: "list[str]" = []
    for txt_file_path in iglob(pathname, recursive=True):
        with open(txt_file_path) as txt_file:
            lines = txt_file.readlines()
            for line in lines:
                line = line.strip()

                # avoid newspaper time stamp footers
                if sub_grp in {"articles", "enh_corpus_by_year"} and re.search(
                    r"^ከ[^0-9]{,20}[0-9]{1,2} ቀን [0-9]{4}$", line
                ):
                    continue
                sub_group_words.extend(line.split())

    sub_group_wrds_len = len(sub_group_words)

    # set output file path
    output_file_name = re.sub(r"\/", "_", sub_grp)
    output_file_path = os.path.join(output_root_dir, output_file_name)

    # check if output file already exists
    if os.path.exists(output_file_path):
        response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
        if response != "Y":
            exit(1)

    sub_group_wrds_len = len(sub_group_words)
    wrd_index = 0  # current word index in list

    # write to output file, wrapping line to max LINE_LENGTH chars
    with open(output_file_path, "w") as output_file:
        while wrd_index < sub_group_wrds_len:
            line = ""
            # concat words into line of LINE_LENGTH
            while len(line) + len(sub_group_words[wrd_index]) < LINE_LENGTH:
                line += sub_group_words[wrd_index] + " "
                wrd_index += 1
                if not wrd_index < sub_group_wrds_len:
                    break

            # write to output file
            if not line.isspace():
                output_file.write(line.strip() + "\n")

#!/usr/bin/env python3
"""
Combines text files
"""

import os
import re
from glob import iglob

# from pathlib import Path
import random

from constants import LINE_LENGTH


output_root_dir = "./combined_txts"
input_root_dir = "./cleaned_texts"

# dirs in input root dir
input_sub_groups = {
    "word_lists",
    "dictionary_and_linguistic_books",
    "articles",
    "books/religious_amh/",
    "books/religious_geez/",
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

    # collect all words for each sub group in a list
    sub_group_words: "list[str]" = []
    for txt_file_path in iglob(pathname, recursive=True):
        with open(txt_file_path) as txt_file:
            for line in txt_file:
                sub_group_words.extend(line.split())

    sub_group_words_wrds_len = len(sub_group_words)

    # random shuffle words for word list files
    if sub_grp == "word_lists":
        new_sub_group_words = []
        i = 0
        # if open paren is at start of word, try to find closing paren
        while i < sub_group_words_wrds_len:
            w = sub_group_words[i]
            # concat atmost 5 words until close paren is found
            if sub_group_words[i].startswith("("):
                curr_index = i
                while i < sub_group_words_wrds_len and not w.endswith(")"):
                    i += 1
                    w += " " + sub_group_words[i]
                    if i - curr_index > 5:
                        w = sub_group_words[curr_index]
                        i = curr_index
                        break
            new_sub_group_words.append(w)
            i += 1
        sub_group_words = new_sub_group_words
        random.Random(23).shuffle(sub_group_words)
        sub_group_words_wrds_len = len(sub_group_words)

    # set output file path
    output_file_name = re.sub(r"\/", "_", sub_grp)
    output_file_path = os.path.join(output_root_dir, output_file_name)

    wrd_index = 0  # current word index in list

    # check if output file already exists
    if os.path.exists(output_file_path):
        response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
        if response != "Y":
            exit(1)

    with open(output_file_path, "w") as output_file:
        while wrd_index < sub_group_words_wrds_len:
            line = ""
            # concat words into line of LINE_LENGTH
            while len(line) + len(sub_group_words[wrd_index]) < LINE_LENGTH:
                line += sub_group_words[wrd_index] + " "
                wrd_index += 1
                if not wrd_index < sub_group_words_wrds_len:
                    break

            # write to output file
            if not line.isspace():
                output_file.write(line.strip() + "\n")

#!/usr/bin/env python3
"""
Combines text files by sub groups. After wrapping lines to LINE_LENGTH
shuffles lines before writing to output file for the subgroup.
"""

import os
import re
from glob import iglob

from constants import LINE_LENGTH, puncs_to_strip_for_freq


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

wrds_freq_rel_amh_dict: "dict[str, int]" = {}


def filter_religious_amh(line_wrds: "list[str]"):
    """Filters list of words by removing excessively repeated
    sub_group specific words."""
    # strip unwanted non-Ethiopic puncs from each word
    wrds = [w.strip("()./-") for w in line_wrds]
    filtered_wrds = []
    # loop over each word
    for w in wrds:

        # avoid bible chapter quotes
        if re.search(
            r"[\u1369-\u137D]+[\u1200-\u135a\.]+|[\u1200-\u135a\.]+[\u1369-\u137D]+", w
        ):
            continue

        # replace Ethiopic 100-199 representations (no 1 before 100)
        w = re.sub(r"፩፻", "፻", w)

        w_dict = w.strip("".join(puncs_to_strip_for_freq))

        # freq for single chars
        if len(w_dict) == 1:
            wrds_freq_rel_amh_dict[w_dict] = wrds_freq_rel_amh_dict.get(w_dict, 0) + 4

        # for ethiopic and arabic numbers
        elif all([c in range(0x1369, 0x137D) or c in range(0, 10) for c in w]):
            wrds_freq_rel_amh_dict[w_dict] = wrds_freq_rel_amh_dict.get(w_dict, 0) + 4

        else:
            wrds_freq_rel_amh_dict[w_dict] = wrds_freq_rel_amh_dict.get(w_dict, 0) + 1

        # if word is below freq threshold add to list
        if wrds_freq_rel_amh_dict[w_dict] < 10:
            filtered_wrds.append(w)

    return filtered_wrds


wrds_freq_enh_dict: "dict[str, int]" = {}


def filter_enh_corpus(line_wrds: "list[str]"):
    """Filters list of words by removing excessively repeated
    sub_group specific words."""

    filtered_wrds = []
    # loop over each word
    for w in line_wrds:

        w_dict = w.strip("".join(puncs_to_strip_for_freq))

        # for arabic numbers
        if re.search(r"[0-9]", w_dict):
            wrds_freq_enh_dict[w_dict] = wrds_freq_enh_dict.get(w_dict, 0) + 10

        # freq for single chars
        elif len(w_dict) == 1:
            wrds_freq_enh_dict[w_dict] = wrds_freq_enh_dict.get(w_dict, 0) + 40

        else:
            wrds_freq_enh_dict[w_dict] = wrds_freq_enh_dict.get(w_dict, 0) + 1

        # if word is below freq threshold add to list
        if wrds_freq_enh_dict[w_dict] < 101:
            filtered_wrds.append(w)

    return filtered_wrds


wrds_freq_articles: "dict[str, int]" = {}


def filter_articles(line_wrds: "list[str]"):
    """Filters list of words by removing excessively repeated
    sub_group specific words."""

    filtered_wrds = []
    # loop over each word
    for w in line_wrds:

        # skip excessively repeated year tags
        if re.search(r"1998|2002", w):
            continue

        w_dict = w.strip("".join(puncs_to_strip_for_freq))

        # for arabic numbers
        if re.search(r"[0-9]", w_dict):
            wrds_freq_articles[w_dict] = wrds_freq_articles.get(w_dict, 0) + 10

        # freq for single chars
        elif len(w_dict) == 1:
            wrds_freq_articles[w_dict] = wrds_freq_articles.get(w_dict, 0) + 40

        else:
            wrds_freq_articles[w_dict] = wrds_freq_articles.get(w_dict, 0) + 1

        # if word is below freq threshold add to list
        if wrds_freq_articles[w_dict] < 101:
            filtered_wrds.append(w)

    return filtered_wrds


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

                # split line into list of words
                line_wrds = line.split()

                # filter words for religiou amh subgroup
                if "religious_amh" in sub_grp:
                    line_wrds = filter_religious_amh(line_wrds)

                # filter words for articles subgroup
                if sub_grp == "articles":
                    line_wrds = filter_articles(line_wrds)

                # filter words for enh_corpus_by_year subgroup
                if sub_grp == "enh_corpus_by_year":
                    line_wrds = filter_enh_corpus(line_wrds)

                sub_group_words.extend(line_wrds)

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

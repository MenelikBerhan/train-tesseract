#!/usr/bin/env python3
"""
Generate aggreagate information about Cleaned txt files
"""

import json
import os
from glob import iglob
from pathlib import Path
from statistics import mean

from constants import LINE_LENGTH

# output file to write info to
info_ouput_file = "./cleaned_txt_files_info.txt"

# root dir of cleaned txts (contains dirs only)
cleaned_txts_root_dir = "./cleaned_texts/"

# names used as keys for info
info_names = [
    "total_size",
    "total_no_of_files",
    "total_no_of_wrds",
    "total_len_of_wrds",
    "avg_len_of_wrds",
    "no_of_trimmed_lines",
]

# use list of dirs in root dir as groups of txts
group_path = os.path.join(cleaned_txts_root_dir, "*", "")
group_dirs = list(iglob(group_path, recursive=False))

if len(group_dirs) == 0:
    print(f'No files in given directory: {cleaned_txts_root_dir}')
    exit(1)

# dict to store info about each group and its sub groups
info_dict: "dict[str, dict[str, dict[str, float|int]]]" = {}
"""{'group_path': {sub_group_path: {'info_name': 'value'}}}"""

for group_dir in group_dirs:
    # to match sub dirs
    sub_group_path = group_dir + "/*/"
    sub_group_dirs = list(iglob(sub_group_path, recursive=False))

    if len(sub_group_dirs) == 0:  # no sub groups
        sub_group_dirs.append(group_dir)

    group_dict: "dict[str, dict[str, float|int]]" = {}
    """{sub_group_path: {'info_name': 'value'}}"""
    for sub_group_dir in sub_group_dirs:
        sub_group_dict = {}
        # all txt files in sub group dir
        pathname = os.path.join(sub_group_dir, "**", "*.txt")

        total_size, total_no_of_files, total_no_of_wrds, total_len_of_wrds = 0, 0, 0, 0

        for file_path in iglob(pathname, recursive=True):
            total_size += os.stat(file_path).st_size / 1024 / 1024
            total_no_of_files += 1
            with open(file_path) as txt_file:
                for line in txt_file:
                    wrds = line.split()
                    total_no_of_wrds += len(wrds)
                    total_len_of_wrds += sum([len(w) for w in wrds])

        avg_len_of_wrds = round(total_len_of_wrds / total_no_of_wrds, 2)
        sub_group_dict["total_no_of_files"] = total_no_of_files
        sub_group_dict["total_size"] = round(total_size, 3)
        sub_group_dict["total_no_of_wrds"] = total_no_of_wrds
        sub_group_dict["total_len_of_wrds"] = total_len_of_wrds
        sub_group_dict["avg_len_of_wrds"] = avg_len_of_wrds

        # approximate estimation (one space aftr each wrd)
        no_of_wrds_per_line = LINE_LENGTH // (avg_len_of_wrds + 1)
        sub_group_dict["no_of_trimmed_lines"] = round(
            total_no_of_wrds / no_of_wrds_per_line
        )

        # add sub group dict to group dict
        group_dict[sub_group_dir] = sub_group_dict

    # add group dict to info dict
    info_dict[group_dir] = group_dict

# summary of info for each group (summed/averaged over sub groups)
group_summary_dict = {}
"""{'group_path': {'info_name': 'value'}}"""
for g, sg_dict in info_dict.items():
    g_dict = {}
    sub_groups = sg_dict.keys()
    for info_name in info_names:
        if info_name == "avg_len_of_wrds":
            g_dict[info_name] = round(
                mean([sg_dict[sg][info_name] for sg in sub_groups]), 3
            )
        else:
            g_dict[info_name] = round(
                sum([sg_dict[sg][info_name] for sg in sub_groups]), 3
            )

    group_summary_dict[g] = g_dict


# summary info for all files (summed/averaged over groups)
summary_dict = {}
"""{'info_name': 'value'}"""
for k in info_names:
    if k == "avg_len_of_wrds":
        summary_dict[k] = round(mean([g[k] for g in group_summary_dict.values()]), 3)
    else:
        summary_dict[k] = round(sum([g[k] for g in group_summary_dict.values()]), 3)

# add no chars per line to output file name
output_file_path = Path(info_ouput_file)
output_file_path = output_file_path.with_name(
    output_file_path.stem + f"_{LINE_LENGTH}_chars_line" + output_file_path.suffix
)

# write to output file
with open(output_file_path, "w") as file:
    json.dump("ALL FILES SUMMARY", file)
    json.dump(summary_dict, file, indent=2)
    json.dump("GROUP SUMMARY", file)
    json.dump(group_summary_dict, file, indent=2)
    json.dump("SUB-GROUPS SUMMARY", file)
    json.dump(info_dict, file, indent=2)

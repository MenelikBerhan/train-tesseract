#!/usr/bin/env python3
"""
For Droid Sans Ethiopic Font (Doesn't render allowed non-Ethiopic chars.)
Combines all sub group txt files into one training text by shuffling lines.
"""

import os
import random
import re
from glob import iglob

from constants import LINE_LENGTH, eth_unicode_range_letters
from utils import convert_to_eth_num

OVERWRITE = True

output_root_dir = "."
output_file_name = "amh-layer.training_txt-droid"

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
if not OVERWRITE and os.path.exists(output_file_path):
    response = input(f"File {output_file_path} Exists. Overwrite? Y/N: ")
    if response != "Y":
        exit(1)

all_wrds: "list[str]" = []
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

# add some Ethiopic chars as single words
add_chrs_dict = {
    "ሗ": 30,
    "ጷ": 100,
    "ጱ": 50,
    "ዧ": 100,
    "ኧ": 100,
    "ቯ": 100,
    "ቩ": 100,
    "ሧ": 100,
    "ሗ": 100,
    "፡": 50000,
    "።": 10000,
    "፣": 2000,
    "፤": 3000,
    "፥": 3000,
    "፦": 2000,
}

for ch in add_chrs_dict:
    all_wrds.extend([ch] * add_chrs_dict[ch])

# add Ethiopic no.s as single words and 'ቊ' before random 250 no.s
to_add_nums = random.Random().sample(range(1, 100), 50)
to_add_nums.extend(random.Random().sample(range(100, 400), 100))
to_add_nums.extend(random.Random().sample(range(400, 1000), 100))
for n in range(1, 10000):
    eth_num = convert_to_eth_num(n)
    if 2500 >= n >= 40:
        # lacking in source texts: '፵፶፷፸፹፺'
        if int(str(n)[-2]) in range(4, 10):
            all_wrds.extend([eth_num] * 2)
        # for ambigious pairs: '፮፮','፰፷','፺ን'
        if ("6" in str(n) and "7" in str(n)) or (str(n)[-2] in "689"):
            all_wrds.extend([eth_num] * 2)
    else:
        all_wrds.extend([eth_num])

    # for 'ቊ'
    if n in to_add_nums:
        all_wrds.extend(["ቊ" + eth_num])

# to add 500 '፼'
nums = random.Random().sample(range(10000, 1000000), 400)
nums.extend(random.Random().sample(range(1000000, 100000000), 100))
for n in nums:
    all_wrds.extend([convert_to_eth_num(n)])


# add ethiopic puncs to d/t random words
end_quotes_dict = {
    "፡": 150000,
    "።": 70000,
    "፣": 20000,
    "፤": 15000,
    "፥": 15000,
    "፦": 10000,
}
for q, k in end_quotes_dict.items():
    to_add_indicies = random.Random().sample(range(0, len(all_wrds)), k)
    for i in to_add_indicies:
        w = all_wrds[i]
        if all([ord(c) in eth_unicode_range_letters for c in w]):
            all_wrds[i] = w + q

# filter out allowed non-Ethiopic chars (not rendered by Droid Sans Font)
non_eth_ptrn = r"[\|\*\%\/\!\?\+\=\<\>\-\.\,\:0-9\"\'\“\”\«\»\‹\›\(\)\[\]]"
filter_funcn = lambda w: not re.search(non_eth_ptrn, w)
filtered_wrds = filter(filter_funcn, all_wrds)

all_wrds = list(filtered_wrds)

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

#!/usr/bin/env python3
"""
Combines text files after shuffling words
"""
import os

from glob import iglob
from pathlib import Path
from random import shuffle

from constants import LINE_LENGTH

input_root_dir = './cleaned_texts'
input_sub_groups = {    # sub dirs in root dir (no / at start)
    'word_lists', 'dictionary_and_linguistic_books', 'articles',
    'books/religious_amh/', 'books/religious_geez/', 'enh_corpus_by_year',
}

ouput_file_path = './combined_w_corpus_80_l.txt'

# add no chars per line to output file path
ouput_file_path = Path(ouput_file_path)
ouput_file_path = ouput_file_path.with_name(
    ouput_file_path.stem +
    f'_{LINE_LENGTH}_chars_line' + ouput_file_path.suffix
)

# make sure output file doesn't exist
assert not ouput_file_path.exists(), \
    f'Output file "{ouput_file_path}" already Exists!'

# add all words in input files into one list
all_words = []

for sub_grp in input_sub_groups:
    sub_grp = sub_grp.strip('/')    # for path.join
    # to match all txt file in sub group
    pathname = os.path.join(input_root_dir, sub_grp, '**', '*.txt')

    for txt_file_path in iglob(pathname, recursive=True):
        with open(txt_file_path) as txt_file:
            for line in txt_file:
                all_words.extend(line.split())

# random shuffle words
shuffle(all_words)
all_wrds_len = len(all_words)


wrd_index = 0       # current word index in list
with open(ouput_file_path, 'x') as output_file:
    while wrd_index < all_wrds_len:
        line = ''
        while len(line) + len(all_words[wrd_index]) < LINE_LENGTH:
            line += all_words[wrd_index] + ' '
            wrd_index += 1
            if not wrd_index < all_wrds_len:
                break
        if not line.isspace():
            output_file.write(line.strip() + '\n')

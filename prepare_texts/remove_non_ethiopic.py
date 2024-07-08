#!/usr/bin/env python3
"""
Removes non Ethiopic Script characters from txt files
"""
import os
import re
from glob import iglob


pathname = os.path.join('../training_texts/', '**', '*.txt')

allowed_non_eth_chars ={
    '/','\\', '~', '|', '!', '?', '$', '*', '^',
    ' ','\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '-', '+', '=', '<', '>',
    '.', ',', ':', ';', '#',  '%', '_',
    '"', "'", '‘', '’', '“', '”', '«', '»', 
    '(', ')', '[', ']', '{', '}'}

def remove_non_ethiopic(match):
    char = match.group()
    if not (char in allowed_non_eth_chars or
            (ord(char) not in range(0x135d, 0x1360) and     # combining marks(not needed)
            0x1200 <= ord(char) <= 0x137F)):     # ethiopic unicode
        return ''
    return char

for file_path in iglob(pathname, recursive=True):
    input_dir, output_file_name = os.path.split(file_path)

    # create sub directories in './cleaned_texts'
    output_sub_dir = input_dir[len('../training_texts/'):]
    output_dir = os.path.join('./cleaned_texts', output_sub_dir)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, 'w') as output_file:
        with open(file_path) as input_file:
            # read file content as list of lines
            for line in input_file.readlines():
                # skip if line is space or empty
                if line.isspace() or not line:
                    continue
                # split line by space b/n words
                line_wrds = line.split()

                # check each letter in each word
                cleaned_line_wrds = [
                    re.sub('.', remove_non_ethiopic, wrd)
                    for wrd in line_wrds
                ]

                # join non empty strings into one line
                final_line = " ".join(
                    [wrd for wrd in cleaned_line_wrds if wrd])

                # skip if resulting line is space or empty 
                if final_line.isspace() or not final_line: continue

                output_file.write(final_line + '\n')

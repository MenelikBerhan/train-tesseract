#!/usr/bin/env python3
"""
Removes non Ethiopic Script characters from txt files
"""
import os
import re
from glob import iglob

from utils import remove_non_ethiopic


# TODO: to inclue chars like <> (occurs multiple times in source)
# TODO: Check for space after punctuation
# TODO: Check if line is all punc
# TODO: Continous . in table of contents

input_root_dir = '../training_texts/'
output_root_dir = './cleaned_texts'
overwrite_output_file = True

# if input root dir doesn't exist raise exception
if not os.path.isdir(input_root_dir):
    raise FileNotFoundError(
        f"Input Root Dir '{input_root_dir}' Does Not Exist!"
    )


def get_output_file_path(input_file_path: str):
    """
    For given input file path, creates sub dirs in output root
    directory as needed abd return output file path.

    Raises FileExists Error if a file already exists at output file path.
    """
    input_file_dir, input_file_name = os.path.split(input_file_path)
    # get sub directroy path by removing input root dir from input file dir
    output_sub_dir = input_file_dir[len(input_root_dir):]

    # remove leading '/' from output_sub_dir so that when joining
    # with output root dir, path.join don't ignore ouput root dir
    output_sub_dir.strip('/')
    output_dir = os.path.join(output_root_dir, output_sub_dir)

    # create output directory if it doesn't exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)     # creates parents as needed

    # set output file path using same input file names
    output_file_path = os.path.join(output_dir, input_file_name)

    # if output file already exists raise exception
    if not overwrite_output_file and os.path.isfile(output_file_path):
        raise FileExistsError(
            f"Output File '{output_file_path}' already Exists!"
        )

    return output_file_path


# pattern to match all txt files in input_root_dir & sub directories
pathname = os.path.join(input_root_dir, '**', '*.txt')

# loop over each input file path
for input_file_path in iglob(pathname, recursive=True):
    # get output file path
    output_file_path = get_output_file_path(input_file_path)

    with open(input_file_path) as input_file:
        with open(output_file_path, 'w') as output_file:
            # read file content & loop over lines
            for line in input_file.readlines():
                # skip if line is space or empty
                if line.isspace() or line == '':
                    continue

                # remove chars that are not allowed
                cleaned_line = re.sub(r'.', remove_non_ethiopic, line)

                # split line by space b/n words (to fix spacing)
                cleaned_line_wrds = cleaned_line.split()

                # join words into one line
                final_line = " ".join(cleaned_line_wrds)

                # skip if resulting line is space or empty
                if final_line.isspace() or final_line == '':
                    continue

                # append newline at the end & write line to output file
                output_file.write(final_line + '\n')

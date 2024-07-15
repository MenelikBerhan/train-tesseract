#!/usr/bin/env python3
"""
Writes each line of text files to a separate txt file.

To be used after OCR'ing an image, writing output to txt file
& verifying each line. Output files will be used for training
along with corresponding .tif images gnerated using `./image2line.sh`
 """

# list of file names with verified text content to be split into lines
# file names must contain only one `-`, and ends with `-output.txt`
file_names = ['math_book_Page_1-output.txt',
              'math_book_Page_2-output.txt', 'math_book_Page_3-output.txt']

# directory of the above input files
input_dir = './texts'

# directory of output text files
out_dir = 'data/amh-math-ground-truth'

for file_name in file_names:
    with open(
            '{}/{}'.format(input_dir, file_name),
            'r', encoding='utf-8') as file:

        # match corresponding line image file name.
        # eg of image name - `k_Page_1-001.exp0.tif`
        out_base = file_name.split('-')[0] + '-0{}.exp0.gt.txt'

        line_no = 0
        for line in file:
            line_no += 1
            # add leading zero to output file name
            out_name = out_base.format(
                '0' + str(line_no) if line_no < 10 else line_no)

            with open(
                '{}/{}'.format(out_dir, out_name),
                    'x', encoding='utf-8') as out:
                out.write(line.strip('\n'))  # remove newline at end

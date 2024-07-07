#!/usr/bin/env python3
"""
Convert html and xml files to plain text files
"""
import os
from glob import iglob

import html2text

# initialize convertor
text_maker = html2text.HTML2Text()

# set options
text_maker.unicode_snob = True      # Use Unicode characters
text_maker.ignore_images = True
text_maker.ignore_tables = True     # Ignore table-related tags while keeping rows
text_maker.ignore_links = True      # avoid hrefs
text_maker.ignore_emphasis = True
text_maker.body_width = 78        # Wrap long lines at position. 0 for no wrapping.
# Use a single line break after a block element. Requires body width setting to be 0.
# SINGLE_LINE_BREAK = False

# M-oM-;M-? at the start of a file (UTF-8 byte order mark).
utf_bom = bytearray.fromhex('ef bb bf').decode()
strip_chars = utf_bom + '\n  #'     # '#' added for headings


def convert_to_txt(convertor: html2text.HTML2Text, html_file_path: str):
    """Convert html/xml to plain text file and save in same location"""
    with open(html_file_path, encoding='utf-8') as html_file:
        txt = convertor.handle(html_file.read())
        # print(txt.strip(strip_chars))

         # get path root except '.html/xml' extension
        output_file_root = os.path.splitext(html_file_path)[0]
        # use '.txt' extension for output file
        output_file = output_file_root + '.txt'
        with open(output_file, 'w') as file:
            # strip unwanted chars & write to txt file
            file.write(txt.strip(strip_chars))


pathname = os.path.join('../training_texts', '**', '*.html')

for html_file in iglob(pathname, recursive=True):
    convert_to_txt(text_maker, html_file)
    os.remove(html_file)

text_maker.close()

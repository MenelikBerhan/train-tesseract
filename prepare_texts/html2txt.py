#!/usr/bin/env python3
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
# text_maker.body_width = 78        # Wrap long lines at position. 0 for no wrapping.
# Use a single line break after a block element. Requires body width setting to be 0.
# SINGLE_LINE_BREAK = False

# M-oM-;M-? at the start of a file (UTF-8 byte order mark).
utf_bom = bytearray.fromhex('ef bb bf').decode()
strip_chars = utf_bom + '\n  #'     # '#' added for headings


def convert_to_txt(convertor: html2text.HTML2Text, html_file_path: str):
    with open(html_file_path, encoding='utf-8') as html_file:
        txt = convertor.handle(html_file.read())
        print(txt.strip(strip_chars))     
    convertor.close()

pathname = os.path.join('./by_year', '*', '*.html')

files_by_year = {}
years = ['1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002']

#!/usr/bin/env python3
import os
from glob import iglob

import pypandoc


pathname = os.path.join('../training_texts/books/Bible', '**', '*.docx')

for docx_file_path in iglob(pathname, recursive=True):
    # get path root except '.docx' extension
    output_file_root = os.path.splitext(docx_file_path)[0]
    # use '.txt' extension for output file
    output_file = output_file_root + '.txt'

    # write output to plain text file
    pypandoc.convert_file(docx_file_path, 'plain', outputfile=output_file,
                          extra_args=['--columns=78'])
    
    # remove orginal docx file if not needed
    os.remove(docx_file_path)

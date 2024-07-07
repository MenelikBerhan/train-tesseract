#!/usr/bin/env python3
import os
from glob import iglob

import pandas as pd


pathname = os.path.join('../training_texts', '**', '*.xlsx')

for xlsx_file_path in iglob(pathname, recursive=True):
    # get path root except '.xlsx' extension
    output_file_root = os.path.splitext(xlsx_file_path)[0]
    # use '.txt' extension for output file
    output_file = output_file_root + '.txt'

    # write output to plain text file
    with open(output_file, 'w') as file:
        # dict of sheet_name: pd.Dataframe key
        df_dict = pd.read_excel(xlsx_file_path, sheet_name=None, na_filter=False)

        # write each sheet to same plain text file
        for name, df in df_dict.items():
            text = df.to_string(None, index=False, na_rep='', line_width=78)

            # remove leading and trailing spaces
            file.write("\n".join(
                [
                    line.strip() for line in text.split('\n') if not line.isspace()
                    ])
                )
    
    # remove orginal xlsx file if not needed
    # os.remove(xlsx_file_path)

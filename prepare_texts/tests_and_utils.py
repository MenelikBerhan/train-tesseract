#!/usr/bin/env python3
"""
Testing Ground for cleaning txt files
"""
import os
import re
from glob import iglob

# pathname = os.path.join('../training_texts/books', '**', '*.txt')
pathname = './bible_amh.txt'
allowed_non_eth_chars = {'/','\\', '~', '|', '!', '?',
 '$', '*', '^', ' ','\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
 '-', '+', '=', '<', '>', '≤', '≥',
 '.', ',', ':', ';', '#',  '%', '_',
 '"', "'", '‘', '’', '“', '”', '«', '»', 
 '(', ')', '[', ']', '{', '}'}

num_trans_dict = {'0': '0', '1': '፩', '2': '፪', '3': '፫', '4': '፬', '5': '፭', '6': '፮', '7': '፯', '8': '፰', '9': '፱', '10': '፲', '11': '፲፩', '12': '፲፪', '13': '፲፫', '14': '፲፬', '15': '፲፭', '16': '፲፮', '17': '፲፯', '18': '፲፰', '19': '፲፱', '20': '፳', '21': '፳፩', '22': '፳፪', '23': '፳፫', '24': '፳፬', '25': '፳፭', '26': '፳፮', '27': '፳፯', '28': '፳፰', '29': '፳፱', '30': '፴', '31': '፴፩', '32': '፴፪', '33': '፴፫', '34': '፴፬', '35': '፴፭', '36': '፴፮', '37': '፴፯', '38': '፴፰', '39': '፴፱', '40': '፵', '41': '፵፩', '42': '፵፪', '43': '፵፫', '44': '፵፬', '45': '፵፭', '46': '፵፮', '47': '፵፯', '48': '፵፰', '49': '፵፱', '50': '፶', '51': '፶፩', '52': '፶፪', '53': '፶፫', '54': '፶፬', '55': '፶፭', '56': '፶፮', '57': '፶፯', '58': '፶፰', '59': '፶፱', '60': '፷', '61': '፷፩', '62': '፷፪', '63': '፷፫', '64': '፷፬', '65': '፷፭', '66': '፷፮', '67': '፷፯', '68': '፷፰', '69': '፷፱', '70': '፸', '71': '፸፩', '72': '፸፪', '73': '፸፫', '74': '፸፬', '75': '፸፭', '76': '፸፮', '77': '፸፯', '78': '፸፰', '79': '፸፱', '80': '፹', '81': '፹፩', '82': '፹፪', '83': '፹፫', '84': '፹፬', '85': '፹፭', '86': '፹፮', '87': '፹፯', '88': '፹፰', '89': '፹፱', '90': '፺', '91': '፺፩', '92': '፺፪', '93': '፺፫', '94': '፺፬', '95': '፺፭', '96': '፺፮', '97': '፺፯', '98': '፺፰', '99': '፺፱'}

def remove_non_ethiopic(match):
    char = match.group()
    if not ( char in allowed_non_eth_chars or
            0x1200 <= ord(char) <= 0x137F):
        return ''
    if char in {'፡', '።', '፥', '፤', '፧', '፦', '፣'}:
        return char + ' '
    return char

for file_path in iglob(pathname, recursive=True):
    output_file_name = os.path.basename(file_path)
    output_file_path = os.path.join('./cleaned_texts', output_file_name)

    with open(output_file_path, 'w') as output_file:
        # with open(file_path) as input_file:
        #     # read file content as list of lines
        #     for line in input_file.readlines():
        #         if line.isspace():
        #             continue
        #         line_wrds = line.split()
        #         cleaned_line_wrds = [
        #             re.sub('.', remove_non_ethiopic, wrd)
        #             for wrd in line_wrds
        #         ]

        def change_num(wrd: str):
            if len(wrd) in [1, 2] and wrd.isdecimal():
                return num_trans_dict[wrd]
            if len(wrd) in [2, 3] and wrd[-1] in {'፡', '።', '፧', '፥', '፤', '፦', '፣'} and wrd[:-1].isdecimal():
                return num_trans_dict[wrd[:-1]] + wrd[-1]
            
            if wrd == '_' * 14: return ''

            return wrd

        #         output_file.write(" ".join(cleaned_line_wrds) + '\n')
        with open(file_path) as input_file:
            # read file content as list of lines
            for line in input_file.readlines():
                if line.isspace():
                    continue
                cleaned_line = re.sub('.', remove_non_ethiopic, line)
                line_wrds = cleaned_line.split()
                cleaned_line_wrds = map(change_num, line_wrds)

                final_line = " ".join(cleaned_line_wrds).strip('_')
                if final_line == '://..':
                    final_line = ''

                output_file.write(final_line + '\n')


# {'/','\\', '~', '|', '!', '?',
#  '$', '*', '^', ' ','\n',  
#  '-', '+', '=', '<', '>', '≤', '≥',
#  '.', ',', ':', ';', '#',  '%', '_',
#  '"', "'", '‘', '’', '“', '”', '«', '»', 
#  '(', ')', '[', ']', '{', '}'}

# Ethiopic Range: 1200–137F
# Ethiopic Supplement Range: 1380–139F
# Ethiopic Extended Range: 2D80–2DDF
# Ethiopic Extended-A Range: AB00–AB2F
# Ethiopic Extended-B Range: 1E7E0–1E7FF

# punctuations & symbols
# U+2014 EM DASH —
# U+2013 En Dash –
# U+2039/a Single Angle Quotation Marks '‹' & '›'
# U+00ab/bb  Double Angle Quotation Marks '«' & '»'
# U+2018/9 left & right Single Quotation Mark '‘' & '’'
# U+2018/9 left & right Double  Quotation Mark '“' & '”'
# U+2022 Bullet '•'
# U+00B7 Middle Dot ·
# U+00D7 Multiplication Sign '×'
# U+2212 Minus Sign '−'
# U+0060 Grave Accent '`'
# U+2190-93 Arrows '←', '↑', '→', '↓',
# &

""" Punctuation
1360 ፠ ETHIOPIC SECTION MARK
1361 ፡ ETHIOPIC WORDSPACE
1362 ። ETHIOPIC FULL STOP
1363 ፣ ETHIOPIC COMMA
1364 ፤ ETHIOPIC SEMICOLON
1365 ፥ ETHIOPIC COLON
1366 ፦ ETHIOPIC PREFACE COLON
1367 ፧ ETHIOPIC QUESTION MARK
1368 ፨ ETHIOPIC PARAGRAPH SEPARATOR

Digits
1369 ፩ ETHIOPIC DIGIT ONE
136A ፪ ETHIOPIC DIGIT TWO
136B ፫ ETHIOPIC DIGIT THREE
136C ፬ ETHIOPIC DIGIT FOUR
136D ፭ ETHIOPIC DIGIT FIVE
136E ፮ ETHIOPIC DIGIT SIX
136F ፯ ETHIOPIC DIGIT SEVEN
1370 ፰ ETHIOPIC DIGIT EIGHT
1371 ፱ ETHIOPIC DIGIT NINE
Numbers
1372 ፲ ETHIOPIC NUMBER TEN
1373 ፳ ETHIOPIC NUMBER TWENTY
1374 ፴ ETHIOPIC NUMBER THIRTY
1375 ፵ ETHIOPIC NUMBER FORTY
1376 ፶ ETHIOPIC NUMBER FIFTY
1377 ፷ ETHIOPIC NUMBER SIXTY
1378 ፸ ETHIOPIC NUMBER SEVENTY
1379 ፹ ETHIOPIC NUMBER EIGHTY
137A ፺ ETHIOPIC NUMBER NINETY
137B ፻ ETHIOPIC NUMBER HUNDRED
137C ፼ ETHIOPIC NUMBER TEN THOUSAND """
# d = {0: '', 1:'፩', 2:'፪', 3:'፫', 4:'፬', 5:'፭', 6:'፮', 7:'፯', 8:'፰', 9:'፱'}
# dn = {1: '፲', 2:'፳', 3:'፴', 4:'፵', 5:'፶', 6:'፷', 7:'፸', 8:'፹', 9:'፺'}
# trans_num = {}
# for n in range(1,100):
#     if n < 10:
#         trans_num[str(n)] = d[n]
#     else:
#         trans_num[str(n)] = dn[n // 10] + d[n % 10]
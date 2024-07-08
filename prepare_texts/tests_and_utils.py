#!/usr/bin/env python3
"""
Testing Ground for cleaning txt files
"""
import os
import re
from glob import iglob

# pathname = os.path.join('../training_texts/books', '**', '*.txt')
pathname = './bible_amh.txt'
allowed_non_eth_chars = {
    '/','\\', '~', '|', '!', '?', '$', '*', '^',
    ' ','\n', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '-', '+', '=', '<', '>',
    '.', ',', ':', ';', '#',  '%', '_',
    '"', "'", '‘', '’', '“', '”', '«', '»', 
    '(', ')', '[', ']', '{', '}'}

d1 = {0: '', 1:'፩', 2:'፪', 3:'፫', 4:'፬', 5:'፭', 6:'፮', 7:'፯', 8:'፰', 9:'፱'}
d10 = {0: '', 1: '፲', 2:'፳', 3:'፴', 4:'፵', 5:'፶', 6:'፷', 7:'፸', 8:'፹', 9:'፺', 10: '፻', 1000: '፼'}

def remove_non_ethiopic(match):
    char = match.group()
    if(len(char) != 1): print(char)
    if not (char in allowed_non_eth_chars or
            (ord(char) not in range(0x135d, 0x1360) and     # combining marks(not needed)
            0x1200 <= ord(char) <= 0x137F)):     # ethiopic unicode
        return ''
    if char in {'፡', '።', '፥', '፤', '፧', '፦', '፣'}:
        return char + ' '
    return char

for file_path in iglob(pathname, recursive=True):
    output_file_name = os.path.basename(file_path)
    output_file_path = os.path.join('./cleaned_texts', output_file_name)

    with open(output_file_path, 'w') as output_file:

        def convert_num(match: re.Match):
            num = match.group()
            if num == '0' or len(num) > 3: return num
            num = int(num)

            h, t, o = num // 100, (num%100) // 10, (num%100) % 10
            geez_num = d1[h] + '፻' if h else '' + d10[t] + d1[o]
            return geez_num

        def change_num(wrd: str):
            if wrd == '_' * 14: return ''

            return re.sub('[\d]+', convert_num, wrd)            

        with open(file_path, encoding='utf-8') as input_file:
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

                if final_line == '(ክለሳ.፩.20020507)': continue
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
# &, '≤', '≥',

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

""" 135D $ ETHIOPIC COMBINING GEMINATION AND VOWEL LENGTH MARK
• Basketo
135E $ ETHIOPIC COMBINING VOWEL LENGTH MARK
• Basketo
135F $፟ ETHIOPIC COMBINING GEMINATION MARK """

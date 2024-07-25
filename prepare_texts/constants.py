#!/usr/bin/env python3
"""
Contains information and common variables related to
Ethiopic Characters & Cleaning Texts
"""

allowed_non_eth_chars = {
    # minus, en & em dashes (rep: minus-hiphen(-))
    '−', '–', '—',
    # dots (rep: . [for '…'])
    '…', '•',
    # to maintain spacing (removed when splitting line)
    ' ', '\n', '\t',
    # general uses (rep: as is)
    '~', '|', '$', '*', '^', '#',  '%', '/', '\\', '!', '?',
    '+', '=', '<', '>', '-', '_', '.', ',', ':', ';',
    # arabic nums (rep: as is)
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # quotes (rep: " and ')
    '"', "'", '‘', '’', '“', '”', '«', '»', '‹', '›', '`',
    # brackets (rep: as is)
    '(', ')', '[', ']', '{', '}'
}

eth_puncs = {'፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨'}
eth_digits = {0: '', 1: '፩', 2: '፪', 3: '፫', 4: '፬',
              5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱'}
eth_nums = {0: '', 1: '፲', 2: '፳', 3: '፴', 4: '፵', 5: '፶',
            6: '፷', 7: '፸', 8: '፹', 9: '፺', 10: '፻', 1000: '፼'}

# ethiopic characters unicode value ranges
eth_unicode_range_all = range(0x1200, 0x137d)
"range of unicode values (in hexadecimal) for all Ethiopic characters"
eth_unicode_range_letters = range(0x1200, 0x135b)
"range of unicode values (in hexadecimal) for Ethiopic letters"
eth_unicode_range_marks = range(0x135d, 0x1360)  # Combining marks- not needed
"range of unicode values for Ethiopic Combining mark characters"
eth_unicode_range_punc = range(0x1360, 0x1369)
"range of unicode values for Ethiopic Punctuation marks."
eth_unicode_range_num = range(0x1369, 0x137d)
"range of unicode values for all Ethiopic numbers"

enclosure_start_list = ['(', '[', '{', '‘', '“', '‹',
                        '<', '`', '"', '\'', '/', '|', ',']
"list of start enclosures that exist only before junk content"

enclosure_end_list = [')', ']', '}', '’', '”', '›',
                      '>', '`', '"', '\'', '/', '|', ',']
"list of end enclosures that exist only after junk content"

same_enclosure_list = ['`', '"', '\'', '/', '|',]
"list of enclosures with identical form at start and end"

# patterns to match enc starts, junk content and enc ends.
junk_enclosure_start_ptrns = [r'\(', r'\[', r'\{', r'‘', r'“', r'‹',
                              r'<', r'`', r'"', r'\'', r'/', r'\|']
"list of patterns to match enclosure before junk content."

junk_enclosure_end_ptrns = [r'\)', r'\]', r'\}', r'’', r'”', r'›',
                            r'>', r'`', r'"', r'\'', r'/', r'\|']
"list of patterns to match enclosure after junk content."

junk_content_ptrn = r'[\-\[’|\\−«:_–\^፨።—፦"“,*`;፡፧=…$፤%•{?›፥<! \t~”\]>}‘፣/፠‹+.\'#»]*'
"pattern to match junk content b/n enclosure start and end."

sentense_end_enclosures = [')', ']', '}', '’', '”',
                           '›', '>', '`', '"', '\'', '/']
"list of chars valid to be placed after Ethiopic sentence end `።` "

# characters to strip from start & end of line (before writing to output file)
strip_frm_start_and_end = '$/<‘~:^\'\t’«>› (|?;-]_−{\n“=)•`,[—»…*#\\"–.}+%‹!”'
"string containing chars to strip from start and end of line."

strip_chars_ptrn = r'[$/<‘~:\^\'\t’«>› \(\|\?;\-\]_−\{\n“=\)•`,\[—»…*#\\"–.\}+%‹!”]'
"""pattern to match characters to strip from line start and end"""

# characters not to strip from start & end if there is adjacent Ethiopic char
to_keep_start = {'brackets': ['(', '[', '/'],
                 'quotes': ['“', '«', '‹', '"', "'"], 'others': ['.', '-']}
"dict containing list of chars to keep at start of line."

to_keep_end = {'brackets': [')', ']', '/'],
               'quotes': ['”', '»', '›', '"', "'"],
               'others': ['?', '!', '-', '.', '%']}
"dict containing list of chars to keep at end of line."

# unique lines repeated excessively and to be skipped
lines_to_skip = {'ሰለ እዚህ ዜና ዋርካ ስር በአማርኛ ይወያዩ !'}
"""set of lines to be skipped, because of excessive repetition."""

# no. of chars in a line (used for combining cleaned txt files)
LINE_LENGTH = 80

"""no. of chars in a single line to be used for training"""

"""
# Candidates of non-ethiopic chars to allow

'&', '@',

# Unicode values for Ethiopic
Ethiopic Range: 1200–137F
Ethiopic Supplement Range: 1380–139F
Ethiopic Extended Range: 2D80–2DDF
Ethiopic Extended-A Range: AB00–AB2F
Ethiopic Extended-B Range: 1E7E0–1E7FF

##  punctuations & symbols
U+2014 EM DASH —
U+2013 En Dash –
U+2039/a Single Angle Quotation Marks '‹' & '›'
U+00ab/bb  Double Angle Quotation Marks '«' & '»'
U+2018/9 left & right Single Quotation Mark '‘' & '’'
U+2018/9 left & right Double Quotation Mark '“' & '”'
U+2022 Bullet '•'
U+00B7 Middle Dot ·
U+00D7 Multiplication Sign '×'
U+2212 Minus Sign '−'
U+0060 Grave Accent '`'
U+2190-93 Arrows '←', '↑', '→', '↓',

―               HORIZONTAL BAR
₊               SUBSCRIPT PLUS SIGN
⁻               SUPERSCRIPT MINUS
–               EN DASH
−               MINUS SIGN
⁺               SUPERSCRIPT PLUS SIGN
‐               HYPHEN
—               EM DASH
‑               NON-BREAKING HYPHEN
₋               SUBSCRIPT MINUS
‒               FIGURE DASH
"""

"""
# Punctuation
1360 ፠ ETHIOPIC SECTION MARK
1361 ፡ ETHIOPIC WORDSPACE
1362 ። ETHIOPIC FULL STOP
1363 ፣ ETHIOPIC COMMA
1364 ፤ ETHIOPIC SEMICOLON
1365 ፥ ETHIOPIC COLON
1366 ፦ ETHIOPIC PREFACE COLON
1367 ፧ ETHIOPIC QUESTION MARK
1368 ፨ ETHIOPIC PARAGRAPH SEPARATOR

# Digits
1369 ፩ ETHIOPIC DIGIT ONE
136A ፪ ETHIOPIC DIGIT TWO
136B ፫ ETHIOPIC DIGIT THREE
136C ፬ ETHIOPIC DIGIT FOUR
136D ፭ ETHIOPIC DIGIT FIVE
136E ፮ ETHIOPIC DIGIT SIX
136F ፯ ETHIOPIC DIGIT SEVEN
1370 ፰ ETHIOPIC DIGIT EIGHT
1371 ፱ ETHIOPIC DIGIT NINE

# Numbers
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
137C ፼ ETHIOPIC NUMBER TEN THOUSAND

# Combination Marks(Not allowed)
135D $ ETHIOPIC COMBINING GEMINATION AND VOWEL LENGTH MARK
• Basketo
135E $ ETHIOPIC COMBINING VOWEL LENGTH MARK
• Basketo
135F $፟ ETHIOPIC COMBINING GEMINATION MARK
"""

#!/usr/bin/env python3
"""
Contains information and common variables related to
Ethiopic Characters & Cleaning Texts
"""

allowed_non_eth_chars = {
    # to maintain spacing (removed when splitting line)
    " ",
    "\n",
    "\t",
    # general uses (rep: as is)
    "|",
    "*",
    # "#",
    "%",
    "/",
    "!",
    "?",
    "+",
    "=",
    "<",
    ">",
    "-",
    ".",
    ",",
    ":",
    # ";",
    # arabic nums (rep: as is)
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    # quotes (rep: " and ')
    '"',
    "'",
    "“",
    "”",
    "«",
    "»",
    "‹",
    "›",
    # brackets (rep: as is)
    "(",
    ")",
    "[",
    "]",
}
"""allowed non Ethiopic characters"""

allowed_non_eth_avoid = {
    # to maintain spacing (removed when splitting line)
    " ",
    "\n",
    "\t",
    # general uses (rep: as is)
    "|",
    "*",
    "#",
    # quotes (rep: " and ')
    '"',
    "'",
    "“",
    "”",
    "«",
    "»",
    "‹",
    "›",
    # brackets (rep: as is)
    "(",
    ")",
    "[",
    "]",
}
"""allowed non Ethiopic chars which can't be sole members of a single word"""

eth_puncs = {"፠", "፡", "።", "፣", "፤", "፥", "፦", "፧", "፨"}
eth_digits = {
    0: "",
    1: "፩",
    2: "፪",
    3: "፫",
    4: "፬",
    5: "፭",
    6: "፮",
    7: "፯",
    8: "፰",
    9: "፱",
}
eth_nums = {
    0: "",
    1: "፲",
    2: "፳",
    3: "፴",
    4: "፵",
    5: "፶",
    6: "፷",
    7: "፸",
    8: "፹",
    9: "፺",
    10: "፻",
    1000: "፼",
}

eth_letters_avoid = {
    0x1207,
    0x1247,
    0x1249,  # reserved
    # 0x124A,  # 'ቊ' as in 'ቊጥር'
    0x124C,
    0x124D,  # 'ቍ'
    0x124E,  # reserved
    0x124F,  # reserved
    0x1250,
    0x1251,
    0x1252,
    0x1253,
    0x1254,
    0x1255,
    0x1256,
    0x1257,  # reserved
    0x1258,
    0x1259,  # reserved
    0x125A,
    0x125B,
    0x125C,
    0x125D,
    0x125E,  # reserved
    0x125F,  # reserved
    0x1287,
    0x1289,  # reserved
    0x128A,
    0x128C,
    0x128D,
    0x128E,  # reserved
    0x128F,  # reserved
    0x12AF,
    0x12B1,  # reserved
    0x12B2,
    0x12B4,
    0x12B5,
    0x12B6,  # reserved
    0x12B7,  # reserved
    0x12BF,  # reserved
    0x12C1,  # reserved
    0x12C2,
    0x12C4,
    0x12C5,
    0x12C6,  # reserved
    0x12C7,  # reserved
    0x12CF,
    0x12D7,  # reserved
    0x12EF,
    0x12F8,
    0x12F9,
    0x12FA,
    0x12FB,
    0x12FC,
    0x12FD,
    0x12FE,
    0x12FF,
    0x130F,
    0x1311,  # reserved
    0x1312,
    0x1314,
    0x1315,
    0x1316,  # reserved
    0x1317,  # reserved
    0x1318,
    0x1319,
    0x131A,
    0x131B,
    0x131C,
    0x131D,
    0x131E,
    0x131F,
    0x1347,
    0x1357,
    0x1358,
    0x1359,
    0x135A,
    0x135B,  # doesn't exist
    0x135C,  # doesn't exist
}
"""less frequent Ethiopic letters to be avoided"""

# 3 comb marks & '፠', '፧', '፨' [TO BE ADDED? 0x1366 (፦)]
eth_puncs_avoid = {0x135D, 0x135E, 0x135F, 0x1360, 0x1367, 0x1368}
"""less frequent Ethiopic punctuations to be avoided"""

eth_avoid = eth_letters_avoid.union(eth_puncs_avoid)
"""less frequent Ethiopic chars to be avoided"""

# ethiopic characters unicode value ranges
eth_unicode_range_all = range(0x1200, 0x137D)
"range of unicode values (in hexadecimal) for all Ethiopic characters"
eth_unicode_range_letters = range(0x1200, 0x135B)
"range of unicode values (in hexadecimal) for Ethiopic letters"
eth_unicode_range_marks = range(0x135D, 0x1360)  # Combining marks- not needed
"range of unicode values for Ethiopic Combining mark characters"
eth_unicode_range_punc = range(0x1360, 0x1369)
"range of unicode values for Ethiopic Punctuation marks."
eth_unicode_range_num = range(0x1369, 0x137D)
"range of unicode values for all Ethiopic numbers"

enclosure_start_list = ["(", "[", "{", "‘", "“", "‹", "<", "`", '"', "'", "/", "|", ","]
"list of start enclosures that exist only before junk content"

enclosure_end_list = [")", "]", "}", "’", "”", "›", ">", "`", '"', "'", "/", "|", ","]
"list of end enclosures that exist only after junk content"

same_enclosure_list = [
    "`",
    '"',
    "'",
    "/",
    "|",
]
"list of enclosures with identical form at start and end"

# patterns to match enc starts, junk content and enc ends.
junk_enclosure_start_ptrns = [
    r"\(",
    r"\[",
    r"\{",
    r"‘",
    r"“",
    r"‹",
    r"<",
    r"`",
    r'"',
    r"\'",
    r"/",
    r"\|",
]
"list of patterns to match enclosure before junk content."

junk_enclosure_end_ptrns = [
    r"\)",
    r"\]",
    r"\}",
    r"’",
    r"”",
    r"›",
    r">",
    r"`",
    r'"',
    r"\'",
    r"/",
    r"\|",
]
"list of patterns to match enclosure after junk content."

junk_content_ptrn = r'[\-\[’|\\−«:_–\^፨።—፦"“,*`;፡፧=…$፤%•{?›፥<! \t~”\]>}‘፣/፠‹+.\'#»]*'
"pattern to match junk content b/n enclosure start and end."

sentense_end_enclosures = [")", "]", "}", "’", "”", "›", ">", "`", '"', "'", "/"]
"list of chars valid to be placed after Ethiopic sentence end `።` "

# characters to strip from start & end of line (before writing to output file)
strip_frm_start_and_end = "$/<‘~:^'\t’«>› (|?;-]_−{\n“=)•`,[—»…*#\\\"–.}+%‹!”"
"string containing chars to strip from start and end of line."

strip_chars_ptrn = r'[$/<‘~:\^\'\t’«>› \(\|\?;\-\]_−\{\n“=\)•`,\[—»…*#\\"–.\}+%‹!”]'
"""pattern to match characters to strip from line start and end"""

# characters not to strip from start & end if there is adjacent Ethiopic char
to_keep_start = {
    "brackets": ["(", "[", "/"],
    "quotes": ["“", "«", "‹", '"', "'"],
    "others": [".", "-"],
}
"dict containing list of chars to keep at start of line."

to_keep_end = {
    "brackets": [")", "]", "/"],
    "quotes": ["”", "»", "›", '"', "'"],
    "others": ["?", "!", "-", ".", "%"],
}
"dict containing list of chars to keep at end of line."

# unique lines repeated excessively and to be skipped
lines_to_skip = {"ሰለ እዚህ ዜና ዋርካ ስር በአማርኛ ይወያዩ !"}
"""set of lines to be skipped, because of excessive repetition."""

# no. of chars in a line (used for combining cleaned txt files)
LINE_LENGTH = 75

# puncs from wrd before updating freqency
puncs_to_strip_for_freq = {
    "፠",
    "፡",
    "።",
    "፣",
    "፤",
    "፥",
    "፦",
    "፧",
    "፨",
    "|",
    "*",
    "#",
    "%",
    "/",
    "!",
    "?",
    "+",
    "=",
    "<",
    ">",
    "-",
    ".",
    ",",
    ":",
    ";",
    '"',
    "'",
    "“",
    "”",
    "«",
    "»",
    "‹",
    "›",
    "(",
    ")",
    "[",
    "]",
}
"""puncs to be stripped bfr updating word freq dict"""

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

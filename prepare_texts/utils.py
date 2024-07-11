#!/usr/bin/env python3
"""
Utilities for preparing & cleaning txt files
"""
import re


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
    # parentheses (rep: as is)
    '(', ')', '[', ']', '{', '}'
}

eth_puncs = {'፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨'}

eth_digits = {0: '', 1: '፩', 2: '፪', 3: '፫', 4: '፬',
              5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱'}

eth_nums = {0: '', 1: '፲', 2: '፳', 3: '፴', 4: '፵', 5: '፶',
            6: '፷', 7: '፸', 8: '፹', 9: '፺', 10: '፻', 1000: '፼'}


def remove_non_ethiopic_helper(match: re.Match):
    """
    Checks if a matched single char is an allowed character.
    If allowed returns itself, else returns an empty string.

    Raises: ValueError if more than one char is in match group.
    """
    # get matched char and if its not single raise Exception
    char = match.group()
    if len(char) != 1:
        raise ValueError(f"Multiple chars in match: '{char}'")

    # if char is not either ethiopic or allowed return empty
    if not (
        char in allowed_non_eth_chars or
        # ethiopic unicode except combining marks(not needed)
        (ord(char) not in range(0x135d, 0x1360) and
            0x1200 <= ord(char) <= 0x137F)
    ):
        return ''
    # else return char it self
    return char


def remove_non_ethiopic(line: str):
    """
    Removes non Ethiopic characters (except some allowed ones)
    from line and return the cleaned line.
    """
    return re.sub(r'.', remove_non_ethiopic_helper, line)


def is_all_allowed_non_ethiopic(line: str):
    """
    Returns True if line is empty or all chars in line are allowed
    non Ethiopic chars. To be used before writing cleaned text to output.

    Reason: No need for a line that does not contain any Ethiopic char.
    """
    return all([char in allowed_non_eth_chars for char in line])


def remove_extra_dots(match: re.Match):
    """
    Removes repetitions of `.` and `…` from match,
    and adds spacing at start and end when needed.
    """
    # get matched group
    dots: str = match.group()
    # start, dot & end of match group
    start, dot, end = dots[0], dots[1], dots[-1]
    # if there is a char (other than space) before or after dots, add space
    r_start = '' if start in ['.', '…'] else (
        start + ' ' if not start.isspace() else start)
    r_end = '' if end in ['.', '…'] else (
        ' ' + end if not end.isspace() else end)

    # use three `.` or one `…`
    r_dot = dot * 3 if dot == '.' else dot
    return r_start + r_dot + r_end


def clean_line(line: str):
    """
    Cleans line by:
        - removing epetitions of `.` (if > 3) and `…` (if > 1)
        - adding or removing space b/n words & punctuations as needed.

    Returns: list of words in the cleaned line.
    """
    # matches repetiton of dots with optional one char at start & end
    pattern = r'(.?(\.{4,}|…{2,}).?)'
    # replace dots
    line = re.sub(pattern, remove_extra_dots, line)

    # split line by space b/n words (to fix spacing)
    cleaned_line_wrds = line.split()

    # TODO: add space after punctuations in long words(len()>15)
    return cleaned_line_wrds


def convert_num(match: re.Match):
    num = match.group()
    if num == '0' or len(num) > 3:
        return num
    num = int(num)

    h, t, o = num // 100, (num % 100) // 10, (num % 100) % 10
    geez_num = eth_digits[h] + \
        '፻' if h else '' + eth_nums[t] + eth_digits[o]
    return geez_num


def change_num(wrd: str):
    if wrd == '_' * 14:
        return ''

    return re.sub(r'[\d]+', convert_num, wrd)


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

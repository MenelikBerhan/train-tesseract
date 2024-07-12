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


def line_is_all_punc(line: str):
    """
    Returns True if line is empty or all chars in line are allowed
    non Ethiopic chars or Ethiopic punctuations. To be used before
    writing cleaned text to output.

    Reason: No need for a line that does not contain any Ethiopic letter.
    """
    return all([
        char in allowed_non_eth_chars.union(eth_puncs) for char in line]
    )


def remove_repetitive_punctuations(match: re.Match):
    """
    Removes repetitions of `.`, `_` and `…` from match,
    and adds spacing at start and end when needed.
    """
    repeating_chars = ['.', '…', '_']
    # get matched group of repetitive punctuations
    puncs: str = match.group()
    # start, puctuation (.|_|…) & end of match group
    start, punc, end = puncs[0], puncs[1], puncs[-1]

    # if there is a char (other than space) before or after puncs, add space
    cleaned_start = '' if start in repeating_chars else (
        start + ' ' if not start.isspace() else start)
    cleaned_end = '' if end in repeating_chars else (
        ' ' + end if not end.isspace() else end)

    # use three `._` or one `…`
    cleaned_punc = punc if punc == '…' else punc * 3
    return cleaned_start + cleaned_punc + cleaned_end


def add_space_after_char(match: re.Match):
    """
    Adds a space after Ethiopic punctuation characters,
    between `]` & `[` and `)` & `()`.
    """
    before_space_chars = eth_puncs.union({']', ')'})
    # get matched chars
    chars = match.group()
    if len(chars) != 2:
        raise ValueError('Length of Match not Equal to Two!')
    if chars[0] not in before_space_chars:
        raise ValueError('Incorrect char at Start of Match!')

    # add space & return
    return chars[0] + ' ' + chars[1]


def substitue_punctuations(match: re.Match):
    """
    Replaces incorrectly represented Ethiopic punctuations with proper one.
    Example: replaces `፡፡` with `።`, `፡-` with `፦` & `፤-` with `፤ `.
    """
    punc_dict = {'፡፡': '።', '፡-': '፦', '፤-': '፤ '}
    # get matched chars
    chars = match.group()
    if len(chars) != 2:
        raise ValueError('Length of Match not Equal to Two!')
    if chars not in punc_dict:
        raise ValueError('Incorrect characters Matched!')
    return punc_dict[chars]


def add_space_bfr_paren(match: re.Match):
    """
    Adds a space before opening parenthesis.
    """
    chars = match.group()
    # atleast 6 = 2 eth chars + open paren + 3 chars bfr close
    if len(chars) < 6:
        raise ValueError('Length of Match Less than Six!')
    i_paren = chars.find('(')
    if i_paren == -1:
        raise ValueError('No open Parenthesis in Match!')

    return chars[: i_paren] + ' ' + chars[i_paren:]


def clean_line(line: str):
    """
    Cleans line by:
        - removing undesired characters at start & end of line,
            which are mostly remnants of lists & tables in source text.
        - substituting improper punctuations with correct one, 
            for example replace `፡፡` with `።`, `፡-` with `፦`.
        - removing repetitions of `.|_` (if > 3) and `…` (if > 1),
            which exist mostly in table of contents of source text.
        - adding or removing space b/n words & punctuations as needed.

    Returns: list of words in the cleaned line.
    """
    # strip undesired chars from start & end of line
    # spaces added to strip chars if only space occurs b/n them
    chars_to_strip = '+|, \t\n'
    line = line.strip(chars_to_strip)

    # TODO: space before opening parens
    # TODO: space surrounded |

    # match `፡፡`, `፡-` & `፤-` and replace with `።`, `፦` & `፤ `
    # NOTE: `፤-` is a peculiar case for DTW-All-Chapters.txt
    to_replace_punc_ptrn = r'(፡፡|፡-|፤-)'
    line = re.sub(to_replace_punc_ptrn, substitue_punctuations, line)

    # match ethiopic punc chars not followed by space (except those before closing parens),
    # closing paren directly followed by opening paren `][`, `)(`
    lack_space_ptrn = r'([፣፦፥፧፡፤፠።፨](?!\)|\])\S|\]\[|\)\()'
    # add space after first char in match
    line = re.sub(lack_space_ptrn, add_space_after_char, line)

    # matches repetition of (.|_|…) with optional one char at start & end
    # TODO: add other repetitive chars to remove here
    repeat_pattern = r'(.?([\._]{4,}|…{2,}).?)'
    # replace repetitions of punctuations
    line = re.sub(repeat_pattern, remove_repetitive_punctuations, line)

    # matches PARENTHESIS () with empty, space or only punc characters.
    # remnant of removed non-allowed non-Ethiopic chars
    junk_paren_ptrn = r'\([-\[’|\\−«:_–^፨።—፦"“,*`;፡፧=…$፤%•\{?›፥<! \t~”\]>\}‘፣/፠‹+.\'#»]*\)'
    # replace junk paren with empty string
    line = re.sub(junk_paren_ptrn, '', line)

    # match 2 or more ethiopic chars followed by a parenthesis containing
    # atleast 3 characters. (Peculiar to Dictionaries)
    no_space_paren = r'[\u1200-\u135a]{2,}\([^\)]{3,}'
    line = re.sub(no_space_paren, add_space_bfr_paren, line)

    # TODO: CHECK IF LINE IS ALL PUNCTUATIONS (including Ethiopic)

    # split line by space b/n words (to fix spacing)
    cleaned_line_wrds = line.split()

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

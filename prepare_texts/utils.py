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
    # brackets (rep: as is)
    '(', ')', '[', ']', '{', '}'
}

eth_puncs = {'፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨'}

eth_digits = {0: '', 1: '፩', 2: '፪', 3: '፫', 4: '፬',
              5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱'}

eth_nums = {0: '', 1: '፲', 2: '፳', 3: '፴', 4: '፵', 5: '፶',
            6: '፷', 7: '፸', 8: '፹', 9: '፺', 10: '፻', 1000: '፼'}

# all junk enclosures list with same index for matching start-end pair
enclosure_start_list = [
    '(', '[', '{', '‘', '“', '‹', '<', '`', '"', '\'', '/', '|', ',']
enclosure_end_list = [')', ']', '}', '’', '”',
                      '›', '>', '`', '"', '\'', '/', '|', ',']
# start and end enclosures are the same
same_enclosure_list = ['`', '"', '\'', '/', '|',]

junk_enclosure_start_ptrns = [
    r'\(', r'\[', r'\{', r'‘', r'“', r'‹', r'<', r'`', r'"', r'\'', r'/', r'\|']
junk_enclosure_end_ptrns = [r'\)', r'\]', r'\}', r'’', r'”',
                            r'›', r'>', r'`', r'"', r'\'', r'/', r'\|']
junk_content_ptrn = r'[\-\[’|\\−«:_–\^፨።—፦"“,*`;፡፧=…$፤%•{?›፥<! \t~”\]>}‘፣/፠‹+.\'#»]*'


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
            0x1200 <= ord(char) <= 0x137c)
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
    between `]` & `[`, and `)` & `(`.
    """
    before_space_chars = eth_puncs.union({']', ')'})
    # get matched chars
    chars = match.group()
    if len(chars) != 2:
        raise ValueError('Length of Match not Equal to Two!')
    if chars[0] not in before_space_chars:
        raise ValueError('Incorrect char at Start of Match!')

    # TODO: for some eth punc chars like `።`, check if nxt char
    # is closing bracket or quote and if so, don't add space
    # if chars[0] == '።' and chars[1] in enclosure_end_list:
    #     return chars

    # add space & return
    return chars[0] + ' ' + chars[1]


def substitue_correct_punctuations(match: re.Match):
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
    Adds a space before an opening parenthesis. Used to fix
    lack of space b/n a word and it's synonym/alternate in dicts.

    match must contain 3 Ethiopic chars, an open parenthesis,
    then at least three chars that are not a closing paren.
    """
    chars = match.group()
    # atleast 6 = 2 eth chars + open paren + 3 chars bfr close
    assert len(chars) >= 6, 'Length of Match Less than Six!'
    # an
    i_paren = chars.find('(')
    assert i_paren == -1, 'No open Parenthesis in Match!'

    return chars[: i_paren] + ' ' + chars[i_paren:]


def remove_junk_helper(match: 're.Match[str]'):
    """
    Removes matched junk content along with (but not always)
    its enclosures.

    Enclosure is marked by start and end characters. `match` contains
    an optional char at start before enc but always contain one char
    at the end making enc. end second to last.

    NOTE:
        - To identify junk enclosure, make sure match has at least
        one non enclosure char at end. This way the second to last char
        can always be used to identify the correct enclosure.

        - if the char before enc. start & after enc. end is non space
        it won't be removed.

        - for same enclosure types, if a char prev to start enc or nxt to
        end enc is not a space, the start or end enc. along with the adjacent
        char are not removed. This is so to avoid removing match b/n end and
        start, e.g.: "/ማየት/, / . ^/'/እዩት/" will be "/ማየት/ /እዩት/".
    """
    # TODO: check if no content b/n enc. start & enc. end
    matched_junk = match.group()
    # start and end of matched junk
    j_start, j_end = matched_junk[0], matched_junk[-1]

    # find junc enclosure start using the enclosure end index.
    # second to last in match is always end enclosure.
    i_enclosure_end = enclosure_end_list.index(matched_junk[-2])
    enclosure_end = enclosure_end_list[i_enclosure_end]
    enclosure_start = enclosure_start_list[i_enclosure_end]

    same_enclosure = enclosure_start in same_enclosure_list

    if same_enclosure:
        assert enclosure_end in same_enclosure_list, \
            f"MIS MATCH IN SAME ENCLOSURE{enclosure_start + '  :  ' + enclosure_end}"

    # find substitution end
    if same_enclosure:
        # dont remove enc. end and nxt char if non space at end
        sub_end = '' if j_end.isspace() else enclosure_end + j_end
    else:
        # dont remove the char after enc. end (last) if its non space
        sub_end = '' if j_end.isspace() else j_end

    sub_start = ''
    # if there is a char before enc. start find sub start
    if j_start != enclosure_start:
        if same_enclosure:
            # dont remove enc. and adjacent char if non space at start or end
            sub_start = '' if j_start.isspace() else j_start + enclosure_start
        else:
            # dont remove start and end chars if they are non space
            sub_start = '' if j_start.isspace() else j_start

    # return by adding space in middle not to concat separate words
    return sub_start + ' ' + sub_end


def remove_junk_in_enclosures(line: str):
    """
    Removes unwanted characters found b/n enclosing chars like brackets and
    quotes. Mostly they are result of removing non Ethiopic chars.
    """
    # to make sure at least one char exist after end enclosure
    # see remove_junk_helper
    if line and not line[-1].isspace():
        line += ' '
    # loop over each enclosures
    for i in range(len(junk_enclosure_start_ptrns)):
        # pattern to match junk with an optional char at start and end
        pattern = r'(.|\n)?' + junk_enclosure_start_ptrns[i] +\
            junk_content_ptrn + junk_enclosure_end_ptrns[i] +\
            r'(.|\n)?'

        # replace junk and assign back to line
        line = re.sub(pattern, remove_junk_helper, line)

    return line


def clean_line(line: str):
    """
    Cleans line by:
        - removing undesired characters at start & end of line,
            which are mostly remnants of lists & tables in source text.
        - substituting improper punctuations with correct one, 
            for example replace `፡፡` with `።`, `፡-` with `፦`.
        - removing undesired remnants of removing non Ethiopic,
            by using chars like brackets and quotes as a delimiter.
        - removing repetitions of `.|_` (if > 3) and `…` (if > 1),
            which exist mostly in table of contents of source text.
        - adding or removing space b/n words & punctuations as needed.

    Returns: list of words in the cleaned line.
    """
    # TODO: add other junk enclosures like (.)
    # TODO: add other repetitive chars to remove (-=?)
    # TODO: non semantic punctuations at start & end (+.-=,|) aftr space
    # TODO: space surrounded |, '([])' used in KBT,
    # TODO: specific puncs repeated excessively in big files and fiction books
    # ... chars like <<, () [], in files like (DTW, KBT) & ones in books/misc
    # ... year and dates limited to newspaper articles source time (1990-8)
    # TODO: common articles repeated in d/t newspapers around same time

    # strip undesired chars from start & end of line
    # spaces added to strip chars if only space occurs b/n them
    chars_to_strip = '+|, \t\n'
    line = line.strip(chars_to_strip)

    # match `፡፡`, `፡-` & `፤-` and replace with `።`, `፦` & `፤ `
    # NOTE: `፤-` is a peculiar case for DTW-All-Chapters.txt
    to_replace_punc_ptrn = r'(፡፡|፡-|፤-)'
    line = re.sub(to_replace_punc_ptrn, substitue_correct_punctuations, line)

    # match ethiopic punc chars not followed by space (except those before
    # closing brackets) and closing brackets directly followed by opening
    # brackets `][`, `)(`. (The latter peculiar to some dicts. [Kidnae?])
    lack_space_ptrn = r'([፣፦፥፧፡፤፠።፨](?!\)|\])\S|\]\[|\)\()'
    # add space after first char in match
    line = re.sub(lack_space_ptrn, add_space_after_char, line)

    # matches repetition of (.|_|…) with optional one char at start & end
    repeat_pattern = r'(.?([\._]{4,}|…{2,}).?)'
    # replace repetitions of punctuations
    line = re.sub(repeat_pattern, remove_repetitive_punctuations, line)

    # match 2 or more ethiopic chars followed by an open parenthesis and
    # atleast other 3 characters. (Peculiar to Dictionaries)
    no_space_bfr_paren = r'[\u1200-\u135a]{2,}\([^\)]{3,}'
    line = re.sub(no_space_bfr_paren, add_space_bfr_paren, line)

    # remove unwanted content (junk) enclosed by chars like brackets & quotes,
    # which exist mostly because non Ethopic chars were removed previously
    line = remove_junk_in_enclosures(line)

    # TODO: CHECK IF LINE IS ALL PUNCTUATIONS HERE (including Ethiopic)

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

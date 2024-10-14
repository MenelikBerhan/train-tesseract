#!/usr/bin/env python3
"""
Utilities for preparing & cleaning txt files
"""

import re

from constants import (
    allowed_non_eth_avoid,
    allowed_non_eth_chars,
    enclosure_end_list,
    enclosure_start_list,
    eth_avoid,
    eth_puncs,
    eth_unicode_range_all,
    eth_unicode_range_marks,
    junk_content_ptrn,
    junk_enclosure_end_ptrns,
    junk_enclosure_start_ptrns,
    lines_to_skip,
    same_enclosure_list,
    sentense_end_enclosures,
    strip_chars_ptrn,
    strip_frm_start_and_end,
    to_keep_end,
    to_keep_start,
)


def line_is_to_be_skipped(line: str):
    """
    Returns `True` if line is one of special case lines to be skipped.

    These lines are excessively repeated in some specific sources,
    like adverts in newspapers.
    """
    return line in lines_to_skip


def replace_non_frequent_eth(match: re.Match):
    """
    Replaces non requent Ethiopic char with a substitute (frequent) char.
    """
    replace_dict = {
        "ጕ": "ጉ",
        "ኵ": "ኩ",
        "ዅ": "ኹ",
        "ኍ": "ኁ",
        "፧": "?",
        "፠": " ",
        "፨": " ",
    }
    # get matched char & return substitute
    char = match.group()
    assert len(char) == 1 and char in replace_dict

    return replace_dict[char]


def remove_word_with_unwanted_chars(match: re.Match):
    """
    Remove word if it contains non allowed, less frequent Ethiopic or
    non Ethiopic chars that don't have a substitute.
    """
    word = match.group()

    # if all chars in word are some section of allowed non eth
    if all([c in allowed_non_eth_avoid for c in word]):
        return ""

    # if any char in word is a char to be avoided
    for c in word:
        if not (
            c in allowed_non_eth_chars
            or (ord(c) not in eth_avoid and ord(c) in eth_unicode_range_all)
        ):
            return ""

    # pecuilar to enh_corpus files
    word = re.sub(r"[0-9]{3};", "", word)
    return word


def clean_non_frequent(line: str):
    """
    Cleans line by removing or substituting Ethiopic chars which are not
    frequently used, and most non-Ethiopic chars which don't have semantic
    meaning or are rarely used.
    """
    # remove Ethiopic accent_marks
    eth_accent_marks = r"[\u135d-\u135f]"
    line = re.sub(eth_accent_marks, "", line)

    # replace minus, en & em dashes with minus-hiphen (-)
    line = re.sub(r"[\−\–\—]", "-", line)

    # replace non frequent ethiopic chars with related forms
    line = re.sub(r"[ጕኵዅኍ፧፠፨]", replace_non_frequent_eth, line)

    # remove words that conotain non frequent chars to avoid
    line = re.sub(r"\S+", remove_word_with_unwanted_chars, line)
    return line


def line_is_all_punc(line: str):
    """
    Returns True if line is empty, or all chars in line are allowed
    non Ethiopic chars or Ethiopic punctuations. To be used before
    writing cleaned text to output.

    Reason: No need for a line that does not contain any Ethiopic letter.
    """
    return all([char in allowed_non_eth_chars.union(eth_puncs) for char in line])


def remove_repetitive_punctuations(match: re.Match):
    """
    Removes repetitions of `.`, `_` and `…` from match,
    and adds spacing at start and end when needed.
    """
    repeating_chars = [".", "…", "_"]
    # get matched group of repetitive punctuations
    puncs: str = match.group()
    # start, puctuation (.|_|…) & end of match group
    start, punc, end = puncs[0], puncs[1], puncs[-1]

    # if there is a char (other than space) before or after puncs, add space
    cleaned_start = (
        ""
        if start in repeating_chars
        else (start + " " if not start.isspace() else start)
    )
    cleaned_end = (
        "" if end in repeating_chars else (" " + end if not end.isspace() else end)
    )

    # use three `._` or one `…`
    cleaned_punc = punc if punc == "…" else punc * 3
    return cleaned_start + cleaned_punc + cleaned_end


def add_space_after_char(match: re.Match):
    """
    Adds a space after punctuation characters,
    and between `]` & `[`, and `)` & `(`. (b/n brackets for dicts)
    """
    before_space_chars = eth_puncs.union({";", "]", ")"})
    # get matched chars
    chars = match.group()
    assert len(chars) == 2, "Length of Match not Equal to Two!"
    assert chars[0] in before_space_chars, "Incorrect char at Start of Match!"

    # is like closing bracket or quote and if so, don't add space
    if chars[0] == "።" and chars[1] in sentense_end_enclosures:
        return chars

    # add space & return
    return chars[0] + " " + chars[1]


def substitue_correct_punctuations(match: re.Match):
    """
    Replaces incorrectly represented Ethiopic punctuations with proper one.
    Example: replaces `፡፡` with `።`, `፡-` with `፦` & `፤-` with `፤ `.
    """
    punc_dict = {"፡፡": "።", "፡፡": "።", "፡-": "፦", "፤-": "፤ "}  # noqa: F601
    # get matched chars
    chars = match.group()
    assert len(chars) == 2, "Length of Match not Equal to Two!"
    assert chars in punc_dict, "Incorrect characters Matched!"

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
    assert len(chars) >= 6, "Length of Match Less than Six!"
    # an
    i_paren = chars.find("(")
    assert i_paren != -1, "No open Parenthesis in Match!"

    return chars[:i_paren] + " " + chars[i_paren:]


def remove_junk_helper(match: "re.Match[str]"):
    """
    Removes matched junk content along with (but not always)
    its enclosures.

    Enclosure is marked by start and end characters. `match` contains
    an optional char at start before enc but always contain one char
    at the end, making enc. end always second to last.

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
        assert (
            enclosure_end in same_enclosure_list
        ), f"MIS MATCH IN SAME ENCLOSURE{enclosure_start + '  :  ' + enclosure_end}"

    # find substitution end
    if same_enclosure:
        # dont remove enc. end and nxt char if non space at end
        sub_end = "" if j_end.isspace() else enclosure_end + j_end
    else:
        # dont remove the char after enc. end (last) if its non space
        sub_end = "" if j_end.isspace() else j_end

    sub_start = ""
    # if there is a char before enc. start find sub start
    if j_start != enclosure_start:
        if same_enclosure:
            # dont remove enc. and adjacent char if non space at start or end
            sub_start = "" if j_start.isspace() else j_start + enclosure_start
        else:
            # dont remove start and end chars if they are non space
            sub_start = "" if j_start.isspace() else j_start

    # return by adding space in middle not to concat separate words
    return sub_start + " " + sub_end


def remove_junk_in_enclosures(line: str):
    """
    Removes unwanted characters found b/n enclosing chars like brackets and
    quotes. Mostly they are result of removing non Ethiopic chars previously.
    """
    # to make sure at least one char exist after end enclosure
    # see remove_junk_helper
    if line and not line[-1].isspace():
        line += " "
    # loop over each enclosures
    for i in range(len(junk_enclosure_start_ptrns)):
        # pattern to match junk with an optional char at start and end
        pattern = (
            r"(.|\n)?"
            + junk_enclosure_start_ptrns[i]
            + junk_content_ptrn
            + junk_enclosure_end_ptrns[i]
            + r"(.|\n)?"
        )

        # replace junk and assign back to line
        line = re.sub(pattern, remove_junk_helper, line)

    return line


def clean_strt_and_end(match: "re.Match[str]"):
    """
    Removes characters in `match` except ones that have semantic meaning.
    To be used just before writing cleaned line to output file.

    `match` contains at least three chars that are in `strip_frm_start_and_end`
    matched either from start or end of line or the whole line.

    If the whole line is matched, returns an empty string.

    If not the whole line, `match` has a char not in `strip_frm_start_and_end`
    at its end for line start match, or at its start for line end match. This
    char is called `anchor` and will not be removed.

    If `anchor` char is Ethiopic (including no.s & puncs) or Arabic number:
        - the first adjacent char in `match` will not be removed if it is in
    `to_keep_start` for line start match, or `to_keep_end` for line end match.

        - in addition, for line end match only, certain combination of adjacent
    chars are not removed to maintain semantics. eg `??, ?!, !?, !!, !!!, ...,`

        - finally for both line start & end matches, one quote and one bracket
    , in any order, will not be removed if they exist after or before anchor
    or kept adjacent chars.
    """
    matched_chars = match.group()
    # find if match is from line start or end or both (the whole line)
    match_is_at_start = matched_chars[-1] not in strip_frm_start_and_end
    match_is_at_end = matched_chars[0] not in strip_frm_start_and_end

    # return empty string if the whole line is matched
    if not match_is_at_start and not match_is_at_end:
        return ""
    match_len = len(matched_chars)

    assert match_len >= 4, f'MATCH "{matched_chars}" LENGTH LESS THAN FOUR'
    assert not (match_is_at_start and match_is_at_end), "MATCH CANT BE FROM STRT & END"

    anchor_char = matched_chars[-1] if match_is_at_start else matched_chars[0]
    anchor_is_ethiopic = (
        ord(anchor_char) in eth_unicode_range_all
        and ord(anchor_char) not in eth_unicode_range_marks
    )
    anchor_is_arabic_num = ord(anchor_char) in range(48, 58)
    to_keep = anchor_char

    if match_is_at_start:  # removing chars from line start
        if anchor_is_ethiopic or anchor_is_arabic_num:
            # start index to check for quotes and/or brackets.
            brkt_quote_i = -2

            if matched_chars[-2] in to_keep_start["others"]:
                if matched_chars[-2] == "-":
                    to_keep = matched_chars[-2] + to_keep
                    # no quote or bracket bfr `-`
                    brkt_quote_i = None
                elif matched_chars[-4:-1] == "...":
                    to_keep = matched_chars[-4:-1] + to_keep
                    brkt_quote_i = -5 if match_len > 4 else None

            # check if quotes and brackets exist before anchor
            # and other adjacent chars.
            if brkt_quote_i is not None:
                i = brkt_quote_i
                if matched_chars[i] in to_keep_start["brackets"]:
                    to_keep = matched_chars[i] + to_keep
                    if (
                        match_len > abs(i)
                        and matched_chars[i - 1] in to_keep_start["quotes"]
                    ):
                        to_keep = matched_chars[i - 1] + to_keep
                elif matched_chars[i] in to_keep_start["quotes"]:
                    to_keep = matched_chars[i] + to_keep
                    if (
                        match_len > abs(i)
                        and matched_chars[i - 1] in to_keep_start["brackets"]
                    ):
                        to_keep = matched_chars[i - 1] + to_keep

    else:  # removing chars from line end
        if anchor_is_ethiopic or anchor_is_arabic_num:
            # start index to check for quotes and/or brackets.
            brkt_quote_i = 1

            if matched_chars[1] in to_keep_end["others"]:
                other_char = matched_chars[1]
                if anchor_is_arabic_num and other_char == "%":
                    to_keep = to_keep + other_char
                    brkt_quote_i = 2
                if other_char == "-":
                    to_keep = to_keep + other_char
                    brkt_quote_i = 2
                elif other_char == ".":
                    if matched_chars[1:4] == "...":
                        to_keep = to_keep + matched_chars[1:4]
                        brkt_quote_i = 4
                    else:
                        to_keep = to_keep + other_char
                        brkt_quote_i = 2
                elif other_char in ["?", "!"]:
                    if matched_chars[1:3] in ["??", "?!", "!?", "!!"]:
                        to_keep = to_keep + matched_chars[1:3]
                        brkt_quote_i = 3
                    elif matched_chars[1:4] == "!!!":
                        to_keep = to_keep + matched_chars[1:4]
                        brkt_quote_i = 4
                    else:
                        to_keep = to_keep + other_char
                        brkt_quote_i = 2

            # check if quotes and brackets exist after anchor
            # and other adjacent chars.
            if brkt_quote_i < match_len:
                i = brkt_quote_i
                if matched_chars[i] in to_keep_end["brackets"]:
                    to_keep = to_keep + matched_chars[i]
                    if (
                        i + 1 < match_len
                        and matched_chars[i + 1] in to_keep_end["quotes"]
                    ):
                        to_keep = to_keep + matched_chars[i + 1]
                elif matched_chars[i] in to_keep_end["quotes"]:
                    to_keep = to_keep + matched_chars[i]
                    if (
                        i + 1 < match_len
                        and matched_chars[i + 1] in to_keep_end["brackets"]
                    ):
                        to_keep = to_keep + matched_chars[i + 1]

    return to_keep


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
    # TODO: add other repetitive chars to remove (-=?)
    # TODO: space surrounded |, '([])' used in KBT,
    # TODO: specific puncs repeated excessively in big files and fiction books
    # ...+ chars like <<, () [], in files like (DTW, KBT) & ones in books/misc,
    # ...+ year and dates limited to newspaper articles source time (1990-8).
    # TODO: common articles repeated in d/t newspapers around same time

    # strip undesired chars from start & end of line
    # spaces added to strip chars if only space occurs b/n them
    chars_to_strip = "+|, \t\n"
    line = line.strip(chars_to_strip)

    # match `፡፡|፡፡`, `፡-` & `፤-` and replace with `።`, `፦` & `፤ `
    # NOTE: `፤-` is a peculiar case for DTW-All-Chapters.txt
    to_replace_punc_ptrn = r"(፡፡|፡፡|፡-|፤-)"
    line = re.sub(to_replace_punc_ptrn, substitue_correct_punctuations, line)

    # match punc chars not followed by space (except those before
    # closing brackets) and closing brackets directly followed by opening
    # brackets `][`, `)(`. NOTE: The latter peculiar to some dicts. [Kidnae?])
    lack_space_ptrn = r"([፣፦፥፧፡፤፠።፨;](?!\)|\])\S|\]\[|\)\()"
    # add space after first char in match
    line = re.sub(lack_space_ptrn, add_space_after_char, line)

    # matches repetition of (.|_|…) with optional one char at start & end
    repeat_pattern = r"(.?([\._]{4,}|…{2,}).?)"
    # replace repetitions of punctuations
    line = re.sub(repeat_pattern, remove_repetitive_punctuations, line)

    # match 2 or more ethiopic chars followed by an open parenthesis and
    # atleast other 3 characters. NOTE: (Peculiar to Dictionaries)
    no_space_bfr_paren = r"[\u1200-\u135a]{2,}\([^\)]{3,}"
    line = re.sub(no_space_bfr_paren, add_space_bfr_paren, line)

    # remove unwanted content (junk) enclosed by chars like brackets & quotes,
    # NOTE: mostly because non Ethopic chars were removed previously
    line = remove_junk_in_enclosures(line)

    # patter to match at least three chars to be striped from line start &
    # end, along with one other optional char
    strip_pattern = (
        r"(^" + strip_chars_ptrn + r"{3,}.?|.?" + strip_chars_ptrn + r"{3,}$)"
    )
    # clean line by removing unwanted chars from line start & end
    line = re.sub(strip_pattern, clean_strt_and_end, line)

    # if line is to be skipped return empty string
    if line_is_to_be_skipped(line):
        return ""
    # split line by space b/n words (to fix spacing)
    cleaned_line_wrds = line.split()

    return cleaned_line_wrds


# def convert_num(match: re.Match):
#     num = match.group()
#     if num == '0' or len(num) > 3:
#         return num
#     num = int(num)

#     h, t, o = num // 100, (num % 100) // 10, (num % 100) % 10
#     geez_num = eth_digits[h] + \
#         '፻' if h else '' + eth_nums[t] + eth_digits[o]
#     return geez_num


# def change_num(wrd: str):
#     if wrd == '_' * 14:
#         return ''

#     return re.sub(r'[\d]+', convert_num, wrd)

#!/usr/bin/env python3
# autopep8: off
# fmt: off
"""
Testing Ground for cleaning txt files
"""
import unicodedata as udta
from pprint import pprint
import os
import re
from glob import iglob

from utils import remove_junk_in_enclosures


allowed_non_eth_charsss = {
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
    # '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # quotes (rep: " and ')
    '"', "'", '‘', '’', '“', '”', '«', '»', '‹', '›', '`',
    # parentheses (rep: as is)
    '(', ')', '[', ']', '{', '}',
    '፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨',
}
eth_puncs = {'፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨'}
ALERT = 'ሰለ እዚህ ዜና ዋርካ ስር በአማርኛ ይወያዩ !' # repeated advert in newspaper (1997,8)
out_path = './test-strt-end-clean.txt'
c = 0
# r'^[$/<‘~:^'\t’«>› (|?;-\]_−{\n“=)•`,[—»…*#\\"–.}+%‹!”]{3,}'
# (^[0-9]{1,4}: [$/<‘~:^'\t’«>› (|?;\-\]_−{\n“=)•`,[—»…*#\\"–.}+%‹!”]{3,}.?|.?[$/<‘~:^'\t’«>› (|?;\-\]_−{\n“=)•`,[—»…*#\\"–.}+%‹!”]{3,}$)

eth_unicode_range_all = range(0x1200, 0x137d)
eth_unicode_range_letters = range(0x1200, 0x135b)
eth_unicode_range_marks = range(0x135d, 0x1360)   # Combining marks- not needed
eth_unicode_range_punc = range(0x1360, 0x1369)
eth_unicode_range_num = range(0x1369, 0x137d)

remove_frm_start_and_end = '$/<‘~:^\'\t’«>› (|?;-]_−{\n“=)•`,[—»…*#\\"–.}+%‹!”'
to_keep_start = {'brackets': ['(', '[', '/'], 'quotes': ['“', '«', '‹', '"', "'"], 'others': ['.', '-']}
to_keep_end = {'brackets': [')', ']', '/'], 'quotes': ['”', '»', '›', '"', "'"], 'others': ['?', '!', '-', '.', '%']}
def clean_strt_and_end(match: 're.Match[str]'):
    """
    ALWAYS DO NOT remove last char of m (for start match) or first char of m
    (for end match) if its not in remove_frm_start_and_end.

    if last char of m (for start match) or first char of m (for end match)
    is ethiopic (including no.s & puncs) or arabic num, DO NOT remove
    adjacent char if it is in dont_remove_start or dont_remove_end.
    TODO: In addition DO NOT remove next char if it is a quote or bracket char in dont_remove_start
    or dont_remove_end unless the prev. one is also a quote or bracket or `-` for end.
    e.g. '+ ]"(ግ?"/ .' will be '""ግ?>"', 'ሀ።» -' will be '"ሀ።»'
    ALSO FOR END: ??, ?!, !?, !! or !!! , ግ..., (ተደ.አ.)
    FOR START: ...ግ
    for arabic num at start of end match: CONSIDER (70%)
    """
    matched_chars = match.group()
    # print(f'MATCH: "{matched_chars}"')
    # find if match is from line start or end or both (the whole line)
    match_is_at_start = matched_chars[-1] not in remove_frm_start_and_end
    match_is_at_end = matched_chars[0] not in remove_frm_start_and_end
    # print(f'START: {match_is_at_start}, END: {match_is_at_end}')
    if not match_is_at_start and not match_is_at_end:   # remove the whole line 
        return ''
    match_len = len(matched_chars)
    assert match_len >= 4, f'MATCH "{matched_chars}" LENGTH LESS THAN FOUR'

    if match_is_at_start:   # removing chars from line start
        anchor_char = matched_chars[-1]
        anchor_is_ethiopic = ord(anchor_char) in eth_unicode_range_all and\
        ord(anchor_char) not in eth_unicode_range_marks
        anchor_is_arabic_num = ord(anchor_char) in range(48, 58)
        to_keep = anchor_char
        if anchor_is_ethiopic or anchor_is_arabic_num:
            if matched_chars[-2] in to_keep_start['brackets']:
                to_keep = matched_chars[-2] + to_keep
                if matched_chars[-3] in to_keep_start['quotes']:
                    to_keep = matched_chars[-3] + to_keep
            elif matched_chars[-2] in to_keep_start['quotes']:
                to_keep = matched_chars[-2] + to_keep
                if matched_chars[-3] in to_keep_start['brackets']:
                    to_keep = matched_chars[-3] + to_keep
            elif matched_chars[-2] in to_keep_start['others']:
                if matched_chars[-2] == '-':
                    to_keep = matched_chars[-2] + to_keep
                elif matched_chars[-4: -1] == '...':
                    to_keep = matched_chars[-4: -1] + to_keep
                    if match_len > 4:
                        if matched_chars[-5] in to_keep_start['brackets']:
                            to_keep = matched_chars[-5] + to_keep
                            if match_len > 5 and matched_chars[-6] in to_keep_start['quotes']:
                                to_keep = matched_chars[-6] + to_keep
                        elif matched_chars[-5] in to_keep_start['quotes']:
                            to_keep = matched_chars[-5] + to_keep
                            if match_len > 5 and matched_chars[-6] in to_keep_start['brackets']:
                                to_keep = matched_chars[-6] + to_keep

    else:                   # removing chars from line end
        anchor_char = matched_chars[0]
        anchor_is_ethiopic = ord(anchor_char) in eth_unicode_range_all and\
        ord(anchor_char) not in eth_unicode_range_marks
        anchor_is_arabic_num = ord(anchor_char) in range(48, 58)
        to_keep = anchor_char
        if anchor_is_ethiopic or anchor_is_arabic_num:
            # print('ANCHOR ETHIOPIC')
            if matched_chars[1] in to_keep_end['brackets']:
                to_keep = to_keep + matched_chars[1]
                if matched_chars[2] in to_keep_end['quotes']:
                    to_keep = to_keep + matched_chars[2]
            elif matched_chars[1] in to_keep_end['quotes']:
                to_keep = to_keep + matched_chars[1]
                if matched_chars[2] in to_keep_end['brackets']:
                    to_keep = to_keep + matched_chars[2]
            elif matched_chars[1] in to_keep_end['others']:
                bracket_or_quote_index = 0
                if anchor_is_arabic_num and matched_chars[1] == '%':
                    to_keep = to_keep + matched_chars[1]
                    bracket_or_quote_index = 2
                if matched_chars[1] == '-':
                    to_keep = to_keep + matched_chars[1]
                    bracket_or_quote_index = 2
                elif matched_chars[1] == '.':
                    if matched_chars[1: 4] == '...':
                        to_keep = to_keep + matched_chars[1: 4]
                        bracket_or_quote_index = 4
                    else:
                        to_keep = to_keep + matched_chars[1]
                        bracket_or_quote_index = 2
                elif matched_chars[1] in ['?', '!']:
                    if matched_chars[1: 3] in ['??', '?!', '!?', '!!']:
                        to_keep = to_keep + matched_chars[1: 3]
                        bracket_or_quote_index = 3
                    elif matched_chars[1: 4] == '!!!':
                        to_keep = to_keep + matched_chars[1: 4]
                        bracket_or_quote_index = 4
                    else:
                        to_keep = to_keep + matched_chars[1]
                        bracket_or_quote_index = 2
                if bracket_or_quote_index < match_len :
                    i = bracket_or_quote_index
                    if matched_chars[i] in to_keep_end['brackets']:
                        to_keep = to_keep + matched_chars[i]
                        if i + 1 < match_len and matched_chars[i + 1] in to_keep_end['quotes']:
                            to_keep = to_keep + matched_chars[i + 1]
                    elif matched_chars[i] in to_keep_end['quotes']:
                        to_keep = to_keep + matched_chars[i]
                        if i + 1 < match_len and matched_chars[i + 1] in to_keep_end['brackets']:
                            to_keep = to_keep + matched_chars[i + 1]

    return to_keep

if __name__ == '__main__':
    pathname = os.path.join('./cleaned_texts/', '**', '*.txt')
    prob_files: 'dict[str, list[tuple[int, str, str]]]' = {}
    for file_path in iglob(pathname, recursive=True):
        with open(file_path) as in_file:
            l = 0
            for line in in_file.readlines():
                l += 1
                if line.isspace() or line == '':
                    continue
                # remove = r'[፤$/<‘፣~:\^\'\t’«>›።7 \(\|\?;0\-\]_−፥\{፧\n“=\)•138`፠5,\[—»…9፦፡*#\\2"–.\}፨+6%‹4!”]'
                # remove = r'[$/<‘~:\^\'\t’«>› \(\|\?;\-\]_−\{\n“=\)•`,\[—»…*#\\"–.\}+%‹!”]'
                remove = r'[$/<‘~:\^\'\t’«>› \(\|\?;\-\]_−\{\n“=\)•`,\[—»…*#\\"–.\}+%‹!”]'
                start_p = r'(^' + remove + r'{3,}.?|.?' + remove + r'{3,}$)'
                # strip_chars = '፤$/<‘፣~:^\'\t’«>›።7 (|?;0-]_−፥{፧\n“=)•138`፠5,[—»…9፦፡*#\\2"–.}፨+6%‹4!”'
                if re.search(start_p, line) != None:
                    try:
                        cleaned_line = re.sub(start_p, clean_strt_and_end, line)
                    except Exception as e:
                        print(f'IN: {file_path}')
                        print(e.args)
                    if file_path in prob_files:
                        if len(prob_files[file_path]) > 3000:
                            print(f"Break too Much in file: {file_path}")
                            break
                        prob_files[file_path].append((l, line, cleaned_line))
                    else:
                        prob_files[file_path] = [(l, line, cleaned_line)]

    print(len(prob_files))
    k = list(prob_files.keys())
    k.sort(key=lambda x: len(prob_files[x]), reverse=True)
    with open(out_path, 'w') as file:
        for f in k:
            to_write = f'{f} ({len(prob_files[f])} Lines)\n'
            for line_info in prob_files[f]:
                to_write += f'{line_info[0]}: "{line_info[1].strip()}":\n"{line_info[2].strip()}"\n'
            file.write(to_write + '\n')


""" d1 = {0: '', 1: '፩', 2: '፪', 3: '፫', 4: '፬',
      5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱'}
d10 = {0: '', 1: '፲', 2: '፳', 3: '፴', 4: '፵', 5: '፶',
       6: '፷', 7: '፸', 8: '፹', 9: '፺', 10: '፻', 1000: '፼'}


def convert_num(match: re.Match):
    num = match.group()
    if num == '0' or len(num) > 3:
        return num
    num = int(num)

    h, t, o = num // 100, (num % 100) // 10, (num % 100) % 10
    geez_num = d1[h] + '፻' if h else '' + d10[t] + d1[o]
    return geez_num


def change_num(wrd: str):
    if wrd == '_' * 14:
        return ''

    return re.sub(r'[\\d]+', convert_num, wrd) """


""" non_eth = 
{'\t': 460761, ' ': 11651387, '\n': 1363773, '+': 81808, '(': 76207, ')': 75008, '[': 47212, ']': 47211, '.': 169331, '?': 30563, ',': 29071, '-': 914717, 'i': 201939, 'n': 189739, 'f': 50869, 't': 218210, 'v': 28565, 'e': 330542, ':': 2846, '1': 76349, '2': 41922, '3': 23739, '4': 19722, '5': 22693, '6': 16096, '7': 16798, '8': 17967, '9': 63127, '0': 47858, '/': 57557, '"': 18943, 'r': 168584, 'o': 181529, 'c': 71133, 'h': 121728, 'k': 22478, 's': 147486, '∸': 1, '…': 22426, 'N': 4485, 'm': 80625, 'a': 255654, 'p': 45779, 'u': 80474, 'd': 96018, 'C': 9286, 'O': 8011, 'M': 18721, 'B': 21058, 'I': 8756, 'E': 9911, 'D': 9893, 'G': 15286, 'R': 4022, 'A': 24678, 'g': 60018, 'l': 122390, 'y': 46366, 'Z': 2603, 'b': 51903, 'T': 19047, 'w': 37418, 'H': 5994, 'j': 6787, 'S': 16819, 'L': 4329, 'F': 5426, '–': 317, 'P': 6151, 'x': 4454, 'U': 3512, 'V': 714, 'Q': 750, '&': 677, 'K': 13997, 'z': 6735, '%': 637, 'q': 6453, 'J': 2051, 'W': 6510, 'X': 92, 'Y': 2835, '»': 47906, '«': 50827, '!': 16299, '*': 4653, '=': 22683, '”': 1796, ';': 1490, '|': 62246, '‘': 4523, '’': 12424, '_': 3402, '፟': 16095, '“': 2168, '¡': 11, 'ⷅ': 4, 'ⷀ': 1, '<': 3384, '>': 3979, '\\': 2861, 'ֹ': 1, '`': 961, '}': 53, '#': 4731, "'": 11213, '\ufeff': 414, '×': 2, '\xad': 186, '⁵': 1, 'ᎄ': 3, 'ᎀ': 3, '›': 3000, 'ÿ': 21, '{': 3, 'é': 1752, 'Ç': 1, 'É': 26, 'Ş': 32, 'π': 1, '^': 203, '$': 85, '‹': 3105, '\x93': 3, '\x97': 5, '@': 112,
   '\x91': 2, 'Ꭵ': 8, 'à': 204, 'ï': 4, '—': 33, '\x07': 338, '\x02': 32, '\xa0': 23, '~': 34, 'ᎃ': 3, 'ⷘ': 3, 'ⶥ': 2, '−': 194, 'ⷛ': 3, 'ⷜ': 1, 'ⶭ': 2, 'ⶈ': 3, 'ⶨ': 2, 'ⷝ': 2, 'ⷃ': 10, 'ⶅ': 3, 'ⷋ': 2, 'ⶖ': 1, 'ⶆ': 2, 'ⷎ': 2, 'ⷈ': 2, 'ⶀ': 2, 'ä': 26832, 'Ĭ': 1, 'ė': 2, 'ĕ': 5, 'ă': 1, 'ż': 1, 'ā': 695, 'ē': 4970, 'ⶋ': 1, 'ⷞ': 1, 'ⷄ': 1, '№': 2, '¬': 7, 'ⷌ': 1, '\x13': 12, '\x14': 12, '\x15': 12, '\x92': 8, 'ⶁ': 1, 'è': 101, '᎑': 1, '᎒': 28, '᎔': 1, '᎖': 1, '᎕': 2, '᎗': 1, '᎙': 1, '䀠': 1, 'Ȉ': 1, '劥': 1, '动': 1, 'ͤ': 1, 'ⷁ': 1, 'ⷍ': 1, 'ᎆ': 2, '\uf020': 1, '‚': 4, '•': 31, '\uf0a7': 2, 'ò': 106, '\x06': 1, '\x03': 3, '\x01': 3, 'í': 4, 'Ꮅ': 4, 'ì': 5, 'ᎅ': 1, 'ë': 1, '\x9d': 17, 'õ': 17, '¢': 6, '£': 5, 'å': 1, '¸': 1, 'Ó': 1, '¤': 3, '¼': 1, 'Ð': 1, 'Í': 1, 'ã': 1, '¨': 1, '³': 1, '§': 1, 'Ë': 1, 'Ꮃ': 4, 'Ꮄ': 1, 'ⶂ': 1, 'ᎁ': 2, 'ý': 2, 'Ꭴ': 1, 'Ꮆ': 1, 'Ꮁ': 1, 'Ꮥ': 1, 'ú': 1, 'ê': 6, '�': 1, 'α': 1, '˃': 1, '≥': 1, 'š': 1642, 'ž': 110, 'ñ': 2429, '\u206d': 2, 'έ': 1, 'ɛ': 1, 'ɫ': 1, 'Ω': 1, 'β': 1, '≁': 4, '→': 14, '↓': 2, '⇢': 6, '⃗': 2, '↑': 6, 'ə': 2900, 'ğ': 406, '̣': 3364, 'č': 2225, '̃': 61, 'ǵ': 6, 'ǧ': 2, 'Ä': 96, 'ň': 82, 'ʷ': 170, 'Ā': 2624, 'Š': 275, 'Č': 204, 'Ň': 3, 'ī': 5835, 'ş': 5, 'ţ': 6, 'ŝ': 10, 'ĝ': 2, 'ć': 2, 'ń': 4, 'á': 6, 'ś': 2, 'Ţ': 2, 'Ğ': 1, 'ḏ': 42, 'û': 5, 'Ī': 232, 'ù': 42, 'Ē': 151, '̱': 1, 'â': 25, 'ü': 1, 'ô': 20, 'î': 6, 'ó': 1, '̄': 1, 'ḩ': 2, 'ū': 1, 'ẖ': 6, 'Ḏ': 3} """

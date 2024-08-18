#!/usr/bin/env python3
# autopep8: off
# fmt: off
"""
Testing Ground for cleaning txt files
"""
import json
from math import floor
import os
import re
from glob import iglob
from pprint import pprint

non_eth_chars = {
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

allowed_non_eth_chars = {
    # minus, en & em dashes (rep: minus-hiphen(-))
    # '−', '–', '—',
    # dots (rep: . [for '…'])
    # '…', '•',
    # to maintain spacing (removed when splitting line)
    ' ', '\n', '\t',
    # general uses (rep: as is)
    # '~', '|', '$', '*', '^', '#', 
    '%', '/', '!', '?',
    '+', '=', '<', '>', '-', '.', ',', ':', 
    # ';',
    # arabic nums (rep: as is)
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # quotes (rep: " and ')
    '"', "'", 
    '«', '»',
    # '‹', '›', '`', '‘', '’', '“', '”', 
    # brackets (rep: as is)
    '(', ')', 
    # '[', ']', '{', '}'
}


# ethiopic characters unicode value ranges
eth_unicode_range_all = range(0x1200, 0x137d)
"range of unicode values (in hexadecimal) for all Ethiopic characters"

wa_and_waa = {0x1217, 0x1248, 0x124B, 0x1288, 0x128B, 0x12B0, 0x12B3, 0x12C0,
     0x12C3, 0x12F7, 0x1310, 0x1313, }
eth_letters_avoid = {
    0x1247, 0x124A, 0x124C, 0x124D, 0x1250, 0x1251, 0x1252, 0x1253,
    0x1254, 0x1255, 0x1256, 0x1258, 0x125A, 0x125B, 0x125C, 0x125D,
    0x1287, 0x128A, 0x128C, 0x128D, 0x12AF, 0x12B2, 0x12B4, 0x12B5,
    0x12C2, 0x12C4, 0x12C5, 0x12CF, 0x12EF, 0x12F8, 0x12F9, 0x12FA,
    0x12FB, 0x12FC, 0x12FD, 0x12FE, 0x12FF, 0x130F, 0x1312, 0x1314,
    0x1315, 0x1318, 0x1319, 0x131A, 0x131B, 0x131C, 0x131D, 0x131E,
    0x131F, 0x1347, 0x1358, 0x1359, 0x135A}

# 0x1366 (፦)
eth_puncs_avoid = {0x135d, 0x135e, 0x135f, 0x1360, 0x1367, 0x1368}  # 3 comb marks & '፠', '፧', '፨'
# output file to write info to
info_ouput_file = './txt_info_all.txt'

# root dir of  txts (contains dirs only)
txts_root_dir = './cleaned_texts/'

# use list of dirs in root dir as groups of txts
group_path = os.path.join(txts_root_dir, '*', '')
group_dirs = list(iglob(group_path, recursive=False))

# dict to store info about each group and its sub groups
info_dict: 'dict[str, dict[str,  dict[str, dict[str, list[str]]]]]' = {}
"""{'group_path': {sub_group_path: {file: {'char': list['words']}}}}"""


for group_dir in group_dirs:

    # to match sub dirs
    sub_group_path = group_dir + '/*/'
    sub_group_dirs = list(iglob(sub_group_path, recursive=False))

    if len(sub_group_dirs) == 0:    # no sub groups
        sub_group_dirs.append(group_dir)

    group_dict: 'dict[str,  dict[str, dict[str, list[str]]]]' = {}
    """{sub_group_path: {file: {'char': list['words']}}}"""
    for sub_group_dir in sub_group_dirs:
        sub_group_dict: 'dict[str, dict[str, list[str]]]' = {}
        # all txt files in sub group dir
        pathname = os.path.join(sub_group_dir, '**', '*.txt')

        for file_path in iglob(pathname, recursive=True):
            file_dict: 'dict[str, list[str]]' = {}
            """{file: {'char': list['words']}}"""
            with open(file_path) as in_file:
                for line in in_file:
                    if line.isspace() or line == '':
                        continue
                    words = line.split()
                    for w in words:
                        # if not any([ord(c) in eth_unicode_range_all for c in w]):
                        #     continue
                        for c in w:
                            # if not (ord(c) in eth_unicode_range_all or c in non_eth_chars):
                            #     continue
                            if (c in allowed_non_eth_chars) or\
                                (ord(c) in eth_unicode_range_all and not (ord(c) in eth_puncs_avoid or ord(c) in eth_letters_avoid)):
                                continue
                            if c not in file_dict:
                                file_dict[c] = []
                            file_dict[c].append(w)

            if file_dict == {}: continue
            sub_group_dict[file_path] = file_dict

        group_dict[sub_group_dir] = sub_group_dict

    info_dict[group_dir] = group_dict

# write to output file
with open(info_ouput_file, 'w') as file:
    json.dump(info_dict, file, indent=2, ensure_ascii=False)

input_sub_groups = {    # sub dirs in root dir (no / at start)
'word_lists', 'dictionary_and_linguistic_books', 'articles',
'books/religious_amh/', 'books/religious_geez/', 'enh_corpus_by_year',
}
# with open('./txt_test_info.txt') as file:
#     info = json.load(file)
out = {}
out['word_lists'] = info_dict["./cleaned_texts/word_lists/"]
out['dictionaries'] = info_dict["./cleaned_texts/dictionary_and_linguistic_books/"]
out['articles'] = info_dict["./cleaned_texts/articles/"]
out['books/religious_amh/'] = info_dict["./cleaned_texts/books/"]["./cleaned_texts/books/religious_amh/"]
out['books/religious_geez/'] = info_dict["./cleaned_texts/books/"]["./cleaned_texts/books/religious_geez/"]
out['enh_corpus'] = info_dict["./cleaned_texts/enh_corpus_by_year/"]

with open('./selected_info_all.txt', 'w') as file:
    json.dump(out, file, indent=2, ensure_ascii=False)

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

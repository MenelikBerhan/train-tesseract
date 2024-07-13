#!/usr/bin/env python3
# autopep8: off
"""
Testing Ground for cleaning txt files
"""
import unicodedata as udta
from pprint import pprint
import os
import re
from glob import iglob


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
    # '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # quotes (rep: " and ')
    '"', "'", '‘', '’', '“', '”', '«', '»', '‹', '›', '`',
    # parentheses (rep: as is)
    '(', ')', '[', ']', '{', '}'
}
eth_puncs = {'፠', '፡', '።', '፣', '፤', '፥', '፦', '፧', '፨'}
same_encl = ['`', '"', '\'', '/', '|',]
start_encl = ['(', '[', '{', '‘', '“', '‹', '<', '`', '"', '\'', '/', '|', ',']
end_encl = [')', ']', '}', '’', '”', '›', '>', '`', '"', '\'', '/', '|', ',']

def sub_e(match):
    m: str = match.group()
    # print(f'Match: "{m}"')
    s, e = m[0], m[-1]
    s_enclosure = start_encl[end_encl.index(m[-2])]
    # if s in start_encl:      # matched at start of line
    if s == s_enclosure:      # matched at start of line
        # s_enclosure = m[0]
        if s_enclosure in same_encl:
            r_e = '' if e.isspace() else s_enclosure + e
        else:
            r_e = '' if e.isspace() else e
        return ' ' + r_e
    else:   # inside line
        # s_enclosure = m[1]
        if s_enclosure in same_encl:
            r_s = '' if s.isspace() else s + s_enclosure
            r_e = '' if e.isspace() else s_enclosure + e
        else:
            r_s = '' if s.isspace() else s
            r_e = '' if e.isspace() else e

        return r_s + ' ' + r_e


out_path = './test-empty-paren-clean.txt'
c = 0
pathname = os.path.join('./cleaned_texts/', '**', '*.txt')
prob_files: 'dict[str, list[tuple]]' = {}
for file_path in iglob(pathname, recursive=True):
    with open(file_path) as in_file:
        l = 0
        for line in in_file.readlines():
            l += 1
            if line.isspace() or line == '':
                continue
            same = [r'`', r'"', r'\'', r'/', r'\|',]
            start = [r'\(', r'\[', r'\{', r'‘', r'“', r'‹', r'<', r'`', r'"', r'\'', r'/', r'\|']
            end = [r'\)', r'\]', r'\}', r'’', r'”', r'›', r'>', r'`', r'"', r'\'', r'/', r'\|']
            # wrds = line.split()
            m = r'[\-\[’|\\−«:_–\^፨።—፦"“,*`;፡፧=…$፤%•{?›፥<! \t~”\]>}‘፣/፠‹+.\'#»]*'
            for i in range(len(start)):
                p = r'(.|\n)?' + start[i] + m + end[i] + r'(.|\n)?'
                if re.search(p, line) != None:
                    s = re.sub(p, sub_e, line) # type: ignore
                    if file_path in prob_files:
                        prob_files[file_path].append((l, line, s))
                    else:
                        prob_files[file_path] = [(l, line, s)]
                    line = s

def add_s(match: re.Match):
    m: str = match.group()
    print(m, match.groupdict())
    i = m.find('(')
    return m[:i] + ' ' + m[i:]

print(len(prob_files))
k = list(prob_files.keys())
k.sort(key=lambda x: len(prob_files[x]), reverse=True)
with open(out_path, 'w') as file:
    for f in k:
        # print(f'{f}: {prob_files[f]}')
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

#!/usr/bin/env python3
"""
Testing Ground for cleaning txt files
"""
import os
import re
from glob import iglob


allowed_non_eth_chars = {
    ' ', '\n', '\t',
    '~', '|', '$', '*', '^', '#',  '%',
    '/', '\\', '!', '?',
    '-', '+', '=', '<', '>',
    '.', ',', ':', ';',  '_',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',    # arabic nums
    '"', "'", '‘', '’', '“', '”', '«', '»',         # quotes
    '(', ')', '[', ']', '{', '}'                    # parenthesis
}

line = 'ውቤ .... 55'
pattern = r'[\.]{4,}'


def replace(match: re.Match):
    print(match)
    m = match.group()
    print(m)
    return 'Q'


res = re.sub(pattern, replace, line)
print(res)


# d1 = {0: '', 1: '፩', 2: '፪', 3: '፫', 4: '፬',
#       5: '፭', 6: '፮', 7: '፯', 8: '፰', 9: '፱'}
# d10 = {0: '', 1: '፲', 2: '፳', 3: '፴', 4: '፵', 5: '፶',
#        6: '፷', 7: '፸', 8: '፹', 9: '፺', 10: '፻', 1000: '፼'}


# def convert_num(match: re.Match):
#     num = match.group()
#     if num == '0' or len(num) > 3:
#         return num
#     num = int(num)

#     h, t, o = num // 100, (num % 100) // 10, (num % 100) % 10
#     geez_num = d1[h] + '፻' if h else '' + d10[t] + d1[o]
#     return geez_num


# def change_num(wrd: str):
#     if wrd == '_' * 14:
#         return ''

#     return re.sub(r'[\d]+', convert_num, wrd)

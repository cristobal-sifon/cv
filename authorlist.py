#!/usr/bin/env python
# -*- coding: utf-8 -*-
from numpy import arange
import sys

if len(sys.argv) < 2:
  print('  Usage: ./authorlist.py <authorlist_filename>')
  exit()

# missing:
#  -replace special characters (e.g., é) with latex format (e.g., \'e)

file = open(sys.argv[1])

# words that should not be capitalized
secondary = (
    'a', 'about', 'an', 'and', 'around', 'at', 'between', 'by', 'for', 'from',
    'in', 'int', 'near', 'of', 'on', 'other', 'out', 'over', 'the', 'through',
    'to', 'via', 'with', 'without', 'z')
# acronyms that should stay all upper case
acronyms = (
    'ACT', 'ACTPol', 'ALMA', 'ATCA', 'BAHAMAS', 'BOSS', 'CMASS', 'CMB',
    'EAGLE', 'GAMA', 'GMRT', 'HSC', 'HST', 'KiDS', 'LOWZ', 'MCMC', 'PLCK',
    'PSZ', 'PSZ2', 'SDSS', 'SPT', 'SZ', 'SZE')
acronyms_lower = [i.lower() for i in acronyms]

def format_word(word):
    if word.lower() in secondary:
        word = word.lower()
    elif word.lower() in acronyms_lower:
        word = acronyms[acronyms_lower.index(word.lower())]
    else:
        word = word.capitalize()
    return word

print()
# first line(s) should be the title
title = ''
line = file.readline().strip()
while len(line) > 0:
  title += line + ' '
  line = file.readline().replace('\n', '')
title = title.split()
title[0] = title[0].capitalize()
for i, word in enumerate(title[1:], 1):
    for symbol in '-+/':
        if symbol in word:
            break
    else:
        symbol = None
    if symbol:
        word = [format_word(w) for w in word.split(symbol)]
        word = symbol.join(word)
    else:
        word = format_word(word)
    title[i] = word
title = ' ' .join(title)
print(title)
print('\n')

# then comes the author list, copied directly from the paper
# assumes that each author has only one last name
nauth = 0
alist = ''
numbers = arange(10)
special = ['\xc3\x81', 'é', 'í', '\xc3\x93', 'ú',
           'ä', 'ë', 'ï', 'ö', '\xc3\x9c']
changeto = [r"\'a", r"\'e", r"\'i", r"\'o", r"\'u",
            '\"a', r'\"e', r'\"i', r'\"o', r'\"u']
for line in file:
  line = line.lower()
  line = line.split(',')
  for auth in line:
    au = auth.split()
    if len(au) > 1:
      nauth += 1
      #print au
      # boldface me
      if 'sif\xc3\x93n' in au:
        alist += r'{\bf '
      # initials
      for a in au[:-1]:
        try:
          aff = int(a)
        except ValueError:
          if a != 'and':
            alist += a[0].upper() + '.~'
      ln = au[-1] # last name
      # in case there is no space between the name and the number(s)
      for n in numbers:
        if str(n) in ln:
          ln = ln.replace(str(n), '')
      # change special chars to latex format
      for s in range(len(special)):
        ln = ln.replace(special[s], changeto[s])
      # append last name
      if ln.lower() == r"sif\'on":
        alist += ln.capitalize() + '}, '
      else:
        alist += ln.capitalize() + ', '
  #print(line)

print(alist)
print('{0} authors'.format(nauth))
print()
print(r'{0} \etal{{{1}}}'.format(alist.split()[0][:-1], nauth))
print(fr'\paper{{{title}}},')
print(r'2020, \href{}{},')
print()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scipy
import sys

if len(sys.argv) < 2:
  print('  Usage: ./authorlist.py <authorlist_filename>')
  exit()

# missing:
#  -replace special characters (e.g., é) with latex format (e.g., \'e)

file = open(sys.argv[1])

# words that should not be capitalized
secondary = (
    'a', 'about', 'and', 'around', 'between', 'by', 'for', 'from',
    'int', 'of', 'on', 'over', 'the', 'through', 'to', 'via', 'with', 'z')
# acronyms that should stay all upper case
acronyms = (
    'ACT', 'ACTPol', 'ALMA', 'ATCA', 'BAHAMAS', 'CMB', 'EAGLE', 'GAMA', 'GMRT', 'HSC',
    'HST', 'KiDS', 'MCMC', 'PLCK', 'PSZ', 'PSZ2', 'SDSS', 'SPT', 'SZ', 'SZE')

print()
# first line(s) should be the title
title = ''
line = file.readline().replace('\n', '')
while len(line) > 0:
  title += line + ' '
  line = file.readline().replace('\n', '')
print(title.split()[0].capitalize(), end=' ')
for word in title.split()[1:]:
    if word.lower() in secondary:
        print(word.lower(), end=' ')
    elif word in acronyms:
        print(word, end=' ')
    else:
        words = [w.capitalize() for w in word.split('-')]
        print('-'.join(words), end=' ')
print('\n')

# then comes the author list, copied directly from the paper
# assumes that each author has only one last name
nauth = 0
alist = ''
numbers = scipy.arange(10)
special = ['\xc3\x81', 'é', 'í', '\xc3\x93', 'ú', 
					 'ä', 'ë', 'ï', 'ö', '\xc3\x9c']
changeto = [r"\'a", r"\'e", r"\'i", r"\'o", r"\'u",
					  r'\"a', r'\"e', r'\"i', r'\"o', r'\"u']
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

#!/usr/bin/env python

import csv
import string
import sys

f = open('public_enrollment.txt')
pub = csv.reader(f, csv.excel_tab)

sys.stdout = open('popcounts.csv', 'wt')

h = pub.__next__()

last = None
grades = 0
for r in pub:
    r = [n.replace(',','') for n in r]
    school = '{:04d}-{:02d}-{:03d}'.format(int(r[3]), int(r[4]), int(r[6]))
    grade = r[11]
    if grade == 'All Grades':
        data = [school, r[5], r[7], r[2], r[12], str(grades)]
        data = [_.strip() for _ in data]
        print(','.join(data))
        grades = 0
    else:
        try:
            grades = grades | 2**int(r[11])
        except:
            if r[11] in ('KG', 'PK', 'ECSE'):
                grades = grades | 1 # 2**0

f = open('nonpublic_enrollment.txt', 'rt')
pub = csv.reader(f, csv.excel_tab)

h = pub.__next__()

last = None
grades = 0
for r in pub:
    r = [n.replace(',','') for n in r]
    school = '{:04d}-{:02d}-{:03d}'.format(int(r[1]), int(r[2]), int(r[4]))
    data = [school, r[3], r[5], r[27], r[21]]
    grades = 0
    for n in range(6,19):
        if r[n] != '0':
            grades = grades | 2**int(n-6)
    data = [school, r[3], r[5], r[27], r[21], str(grades)]
    data = [string.capwords(_.strip()) for _ in data]
    print(','.join(data))

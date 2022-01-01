#!/usr/bin/env python

import csv
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
        print(','.join(data))
        grades = 0
    else:
        try:
            grades = grades | 2**int(r[11])
        except:
            if r[11] in ('KG', 'PK', 'ECSE'):
                grades = grades | 1 # 2**0


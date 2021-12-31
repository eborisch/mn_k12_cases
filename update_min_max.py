#!/usr/bin/env python3

import csv
import sys

from datetime import datetime,date

import numpy as np

CDATA=[]
if len(sys.argv) > 1:
    FLIST = sys.argv[1:]
else:
    import os
    import re
    flist = os.listdir()
    FLIST = (f for f in os.listdir() if re.match('cases_.*', f))

for x in sorted(FLIST):
    f = open(x)
    CDATA.append(csv.reader(f))

DATES = set()
DATE_SETS = []
for d in CDATA:
    # Read header lines
    fdates = [datetime.strptime(x.strip(), '%m/%d/%y') for x  in next(d)[4:]]
    DATES.update(fdates)
    DATE_SETS.append(fdates)
DATES = sorted(DATES)

POP = []
IDS = []
META = []
GRADES = []
with open('popcounts.csv') as popfile:
    for row in csv.reader(popfile):
        IDS.append(row[0])
        META.append((*row[1:-2],))
        POP.append(int(row[-2]))
        GRADES.append(row[-1])

DMIN = np.zeros((len(IDS),len(DATES)), int)
DMAX = np.ones((len(IDS),len(DATES)), int) * 4
DMAX = DMAX / np.reshape(POP,(len(POP),1))
for n,d in enumerate(CDATA):
    for row in d:
        pts = len(row)-4
        try:
            idx = IDS.index(row[0])
        except:
            pass
        offset = DATES.index(DATE_SETS[n][0])
        pop = POP[idx]
        DMIN[idx,offset:offset+pts] = \
                [int(x.split('-')[0]) for x in row[-pts:]]
        DMAX[idx,offset:offset+pts] = \
                [int(x.split('-')[1]) for x in row[-pts:]]

DMIN = np.cumsum(DMIN, 1, int)
DMAX = np.cumsum(DMAX, 1, int)
for n in np.arange(0, len(POP)):
    DMIN[n,:] = np.clip(DMIN[n,:], 0, POP[n])
    DMAX[n,:] = np.clip(DMAX[n,:], 0, POP[n])

with open('minimums.csv', 'w') as fout:
    print(','.join(['District', 'School', 'County', 'Enrollment', 'Grades',
                    *[_.strftime('%Y/%m/%d') for _ in DATES]]), file=fout)
    for x in zip(META, DMIN, POP, GRADES):
        if x[2] < 50:
            continue
        print(','.join(x[0]) + ",{},{},".format(x[2], x[3]) + 
              ','.join('{}'.format(_) for _ in x[1]), file=fout)

with open('maximums.csv', 'w') as fout:
    print(','.join(['District', 'School', 'County', 'Enrollment', 'Grades', 
                    *[_.strftime('%Y/%m/%d') for _ in DATES]]), file=fout)
    for x in zip(META, DMAX, POP, GRADES):
        if x[2] < 50:
            continue
        print(','.join(x[0]) + ",{},{},".format(x[2], x[3]) + 
              ','.join('{}'.format(_) for _ in x[1]), file=fout)

#!/usr/bin/env python

import re
import requests
import sys

import lxml.html as lh

from datetime import datetime

def multisub(subitems, line):
    for m,r in subitems:
        line = re.sub(m, r, line)
    return line

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url='https://www.health.state.mn.us/diseases/coronavirus/stats/#k121'

page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

tbl = [_ for _ in tr_elements if len(_) ==8]
header = ','.join(e.text_content() for e in tbl[0].iterchildren())
header = multisub(((r",[0-9/]+-", ","), (r"\*", "")),
                  header)

header = header.split(',')
for n in range(len(header)):
    try:
        try:
            date = datetime.strptime(header[n], "%m/%d/%y")
        except:
            date = datetime.strptime(header[n], "%m/%d/%Y")
        header[n] = date.strftime('%m/%d/%y')
    except:
        pass
header = ','.join(header)

with open(date.strftime('cases_%Y%m%d.csv'), 'wt') as fout:
    print(header, file=fout)

    for r in tbl[1:]:
        row = ','.join(e.text_content().strip() for e in r.iterchildren())
        row = multisub(((r"\s+"     ,   " "),      # Runs of space to single
                        (r",[.-]"   ,   ",0-4")),  # Replace ./- with 0-4
                       row)
        print(row, file=fout)

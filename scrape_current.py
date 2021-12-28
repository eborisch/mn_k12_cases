#!/usr/bin/env python

import re
import requests

import lxml.html as lh

from datetime import datetime

def multisub(subitems, line):
    for m,r in subitems:
        line = re.sub(m, r, line)
    return line

url='https://www.health.state.mn.us/diseases/coronavirus/stats/#k121'

page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

tbl = [_ for _ in tr_elements if len(_) ==8]
header = ','.join(e.text_content() for e in tbl[0].iterchildren())
header = multisub(((r",[0-9/]+-", ","), (r"\*", "")),
                  header)

date = datetime.strptime(header.split(',')[-1], "%m/%d/%y")

with open(date.strftime('cases_%Y%m%d.csv'), 'wt') as fout:
    print(header, file=fout)

    for r in tbl[1:]:
        row = ','.join(e.text_content().strip() for e in r.iterchildren())
        row = multisub(((r"\s+"     ,   " "),      # Runs of space to single
                        (r",[.-]"   ,   ",0-4")),  # Replace ./- with 0-4
                       row)
        print(row, file=fout)

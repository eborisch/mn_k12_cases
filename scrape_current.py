#!/usr/bin/env python

import re
import requests

import lxml.html as lh

from datetime import datetime

url='https://www.health.state.mn.us/diseases/coronavirus/stats/#k121'

page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

tbl = [_ for _ in tr_elements if len(_) ==8]
header = ','.join(e.text_content() for e in tbl[0].iterchildren())
header = re.sub(',[0-9/]+-', ',', header)
header = re.sub(r'\*', '', header)

fout = open(datetime.now().strftime('cases_%Y%m%d.csv'), 'wt')

print(header, file=fout)

for r in tbl[1:]:
    row = ','.join(e.text_content() for e in r.iterchildren())
    row = re.sub('[^a-zA-Z0-9.()],', ',', re.sub('  +', ' ', re.sub(r',\.', ',0-4', row)))
    print(row, file=fout)

fout.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs
from collections import OrderedDict
import fnmatch
import json
import os
import sys

# error counter
counterr = 0

if (sys.version_info >= (3, 0)):
    ensure_ascii = False
    indent = "\t"
else:
    ensure_ascii = True
    indent = 4

# Need the json path
if len(sys.argv) < 2:
    dir = "json"
else:
    dir = sys.argv[1]

FS = dict()

block_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Block_*.txt')
]

for files in block_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            t = entry["tr_text"]
            j = entry["jp_text"]
            if t == "" or j == t:
                continue
            FS[t] = len(t)

FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

if len(sys.argv) == 3:
    print(json.dumps(FSs, ensure_ascii=ensure_ascii, indent=indent, sort_keys=False))
else:
    FSWP = OrderedDict((key, value) for key, value in FSs.items() if value >= 28)
    for e, s in FSWP.items():
        counterr += 1
        print(u"Block Name '{}' is too long: {}".format(e, s))

if counterr > 0:
    sys.exit("Issues found")

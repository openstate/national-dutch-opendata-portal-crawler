#!/usr/bin/env python
# encoding: utf-8
"""
aggregate.py

Created by Breyten Ernsting on 2013-08-05.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import re
import codecs
import json
from pprint import pprint
from glob import glob

def load_file(file_name):
    data = None
    with codecs.open(file_name, 'r', 'utf-8') as in_file:
        data = json.loads(in_file.read())
    return data

def load_data():
    results = []
    for file_name in glob('odn-data/*.json'):
        print file_name
        data = load_file(file_name)
        results.append(data)
    return results

def result_to_record(result):
    data = [
        result[u'id'],
        result[u'title'],
        result[u'author'],
        result[u'region'],
        result[u'description'],
        result[u'license'] ,
        u','.join(result[u'file_types']),
        result[u'url']
    ]
    return data

def tsv_escape(text):
    if text is not None:
        return u'"' + text.replace('\n', ' ').replace('\t', ' ').replace('\r', '').replace(u'"', u'') + u'"'
    else:
        return u''

def main():
    results = load_data()
    flat_results = [result_to_record(r) for r in results]
    #pprint(flat_results)
    with codecs.open('odn.csv', 'w', 'utf-8') as out_file:
        for flat_result in flat_results:
            out_file.write(u','.join([tsv_escape(f) for f in flat_result]) + u"\n")

if __name__ == '__main__':
    main()


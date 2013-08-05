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
    for file_name in glob('quick-data/data-overheid-dump-*.json'):
        print file_name
        data = load_file(file_name)
        results += data['result']['results']
    return results

def result_to_record(result):
    data = [
        result[u'id'],
        result[u'author'],
        result[u'author_email'],
        result[u'license_id'] ,
        result[u'license_title'],
        result[u'maintainer'],
        result[u'maintainer_email'],
        result[u'metadata_created'],
        result[u'metadata_modified'],
        result[u'name'],
        result[u'title'],
        result[u'notes'],
        result[u'state'],
        u','.join([r[u'display_name'] for r in result[u'tags']]),
        result[u'url']
    ]
    return data

def tsv_escape(text):
    if text is not None:
        return u'"' + text.replace('\n', ' ').replace('\t', ' ').replace('\r', '').replace(u'"', u'\\"') + u'"'
    else:
        return u''

def main():
    results = load_data()
    flat_results = [result_to_record(r) for r in results]
    #pprint(flat_results)
    with codecs.open('data-overheid.csv', 'w', 'utf-8') as out_file:
        for flat_result in flat_results:
            out_file.write(u','.join([tsv_escape(f) for f in flat_result]) + u"\n")

if __name__ == '__main__':
    main()


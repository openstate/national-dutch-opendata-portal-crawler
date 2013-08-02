#!/usr/bin/env python
# encoding: utf-8
"""
crawler.py

Created by Breyten Ernsting on 2013-08-02.
Copyright (c) 2013 Open State Foundation. All rights reserved.
"""

import sys
import os
import re
import codecs
from pprint import pprint
import time

import requests
from BeautifulSoup import BeautifulSoup

def fetch_and_parse_searchpage(page_index=0):
    soup = BeautifulSoup(requests.get('https://data.overheid.nl/data/search?query=&page=%s' % (page_index,)).text)
    datasets = soup.find('div', 'search_results', recursive=True).findAll('a', href=re.compile(r'^\/data\/dataset'))
    links = [u'https://data.overheid.nl%s/json' % (d['href'],) for d in datasets]
    return links

def fetch_and_store_json(dataset_url):
    dataset_id = dataset_url.replace(u'https://data.overheid.nl/data/dataset/', u'').replace(u'/json', u'')
    data = requests.get(dataset_url).text
    with codecs.open(u'data/%s.json' % (dataset_id,), 'w', 'utf-8') as data_file:
        data_file.write(data)

def main():
    for page_nr in range(0..300):
        print "Now at page %s ..." % (page_nr,)
        links = fetch_and_parse_searchpage(page_nr)
        time.sleep(1)
        for link in links:
            print link
            fetch_and_store_json(link)
            time.sleep(1)

if __name__ == '__main__':
    main()


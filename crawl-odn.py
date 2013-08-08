#!/usr/bin/env python
# encoding: utf-8
"""
crawler.py

Created by Breyten Ernsting on 2013-08-02.
Copyright (c) 2013 Open State Foundation. All rights reserved.
"""

import sys
import os
import json
import re
import codecs
from pprint import pprint
import time

import requests
from BeautifulSoup import BeautifulSoup

def fetch_and_parse_searchpage(page_index=0):
    soup = BeautifulSoup(requests.get('http://opendatanederland.org/nl/zoeken?page=%s' % (page_index,)).text)
    datasets = soup.find('ul', 'data-list', recursive=True).findAll('a', href=re.compile(r'^\/nl\/dataset\/'))
    links = [u'http://opendatanederland.org%s' % (d['href'],) for d in datasets]
    return links

def clean_contents(text):
    return re.sub(r'\s*$', u'', re.sub(r'^\s+', u'', text))

def fetch_and_store_json(dataset_url):
    slug = dataset_url.replace(u'http://opendatanederland.org/nl/dataset/', u'')
    soup = BeautifulSoup(requests.get(dataset_url).text)

    title = None
    try:
        title = clean_contents(
            u''.join(soup.find('h1', {'itemtype': 'name'}).findAll(text=True))
        )
    except Exception, e:
        pass

    description = None
    try:
        description = clean_contents(
            u''.join(soup.find('p', {'itemtype': 'description'}).findAll(text=True))
        )
    except Exception, e:
        pass

    odn_id = None
    try:
        odn_id = clean_contents(
            u''.join(soup.find('dd', 'odn-id').findAll(text=True))
        )
    except Exception, e:
        pass

    # FIXME: categorieen
    
    license = None
    try:
        license = clean_contents(
            u''.join(soup.find('span', 'license')['title'])
        )
    except Exception, e:
        pass

    file_types = u''
    try:
        file_types = clean_contents(
            u''.join(soup.find('span', 'filetype').findAll(text=True))
        )
    except Exception, e:
        pass

    url = None
    try:
        url = clean_contents(
            u''.join(soup.find('meta',  {'itemtype': 'url'})['content'])
        )
    except Exception, e:
        pass

    auteur = None
    try:
        auteur = clean_contents(
            u''.join(soup.find('a',  href=re.compile(r'\/nl\/instantie\/')).findAll(text=True))
        )
    except Exception, e:
        pass

    region = None
    try:
        region = clean_contents(
            u''.join(soup.find('div', 'region').find('a').findAll(text=True))
        )
    except Exception, e:
        pass
    
    data = {
        u'id': odn_id,
        u'title': title,
        u'description': description,
        u'license': license,
        u'file_types': file_types.split('/'),
        u'url': url,
        u'author': auteur,
        u'region': region
    }
    
    #return data
    with codecs.open(u'odn-data/%s.json' % (odn_id,), 'w', 'utf-8') as data_file:
        data_file.write(json.dumps(data))
    return data

def main():
    for page_nr in range(40):
    #for page_nr in range(1):
        print "Now at page %s ..." % (page_nr,)
        links = fetch_and_parse_searchpage(page_nr + 1)
        time.sleep(1)
        for link in links:
            print link
            data = fetch_and_store_json(link)
            pprint(data)
            time.sleep(1)

if __name__ == '__main__':
    main()


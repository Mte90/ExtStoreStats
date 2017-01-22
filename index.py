#!/usr/bin/python3
import requests
import json
import time
import lxml.html
import os.path
import re
from lxml.cssselect import CSSSelector

ff_ext = 'glotdict'
gc_ext = 'glotdict/jfdkihdmokdigeobcmnjmgigcgckljgl'

today = time.strftime("%d-%m-%Y")
data = {}
if os.path.isfile('data/' + ff_ext + '.json'):
    with open('data/' + ff_ext + '.json') as data_file:
        data = json.load(data_file)
else:
    data['firefox'] = {}
    data['chrome'] = {}
    data['total'] = {}
     
print('Addons Mozilla Extension Gathering for: %s' % ff_ext)

r = requests.get('https://addons.mozilla.org/api/v3/addons/addon/%s/' % ff_ext)
firefox = json.loads(r.text)
ff_download = int(firefox['average_daily_users'])

data['firefox'][today] = ff_download

print('Downloads: %s' % ff_download)

print('Google Web Store Extension Gathering for: %s' % gc_ext)

r = requests.get('https://chrome.google.com/webstore/detail/%s' % gc_ext)
# Parser the html
tree = lxml.html.fromstring(r.text)
# get the selector for the value
sel = CSSSelector('.e-f-ih')
results = sel(tree)
gc_download = int(re.sub("[^0-9]", "", results[0].text))

data['chrome'][today] = gc_download

print('Downloads: %s' % gc_download)

total = ff_download + gc_download
data['total'][today] = total

print('Total Downloads: %s' % str(total))

archive = open('data/' + ff_ext + '.json', 'w')
archive.write(json.dumps(data))
archive.close()

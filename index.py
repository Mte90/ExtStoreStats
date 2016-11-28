#!/usr/bin/python3 
import requests
import json
import lxml.html
from lxml.cssselect import CSSSelector
import re

ff_ext = 'glotdict'
gc_ext = 'glotdict/jfdkihdmokdigeobcmnjmgigcgckljgl'

print('Addons Mozilla Extension Gathering for: %s' % ff_ext)

r = requests.get('https://addons.mozilla.org/api/v3/addons/addon/%s/' % ff_ext)
firefox = json.loads(r.text)
ff_download = int(firefox['average_daily_users'])

print('Downloads: %s' % ff_download)

print('Google Web Store Extension Gathering for: %s' % gc_ext)

r = requests.get('https://chrome.google.com/webstore/detail/%s' % gc_ext)
# Parser the html
tree = lxml.html.fromstring(r.text)
# get the selector for the value
sel = CSSSelector('.e-f-ih')
results = sel(tree)
gc_download = int(re.sub("[^0-9]", "",results[0].text))

print('Downloads: %s' % gc_download)

print('Total Downloads: %s' % str(ff_download + gc_download))

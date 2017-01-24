#!/usr/bin/python3
import requests
import json
import time
import lxml.html
import os.path
import re
import configparser
from lxml.cssselect import CSSSelector

# Load configuration
config = configparser.RawConfigParser()
config.readfp(open('config.ini'))
list = config.get('Extension', 'list').split(",")

today = time.strftime("%Y-%m-%d")
html = '<html><head><title>ExtStoreStats</title></head><body>'

for ext in list:
    ext = ext.strip()
    ff_ext = config.get(ext, 'firefox')
    gc_ext = config.get(ext, 'chrome')

    data = [[], [], []]
    if os.path.isfile('data/' + ff_ext + '.json'):
        with open('data/' + ff_ext + '.json') as data_file:
            data = json.load(data_file)
            index = len(data[0])
    else:
        index = 0

    print('Addons Mozilla Extension Gathering for: %s' % ff_ext)

    r = requests.get('https://addons.mozilla.org/api/v3/addons/addon/%s/' % ff_ext)
    firefox = json.loads(r.text)
    ff_download = int(firefox['average_daily_users'])

    data[0].append({'date': today, 'value': ff_download})

    print('Downloads: %s' % ff_download)

    print('Google Web Store Extension Gathering for: %s' % gc_ext)

    r = requests.get('https://chrome.google.com/webstore/detail/%s' % gc_ext)
    # Parser the html
    tree = lxml.html.fromstring(r.text)
    # get the selector for the value
    sel = CSSSelector('.e-f-ih')
    results = sel(tree)
    gc_download = int(re.sub("[^0-9]", "", results[0].text))

    data[1].append({'date': today, 'value': gc_download})

    print('Downloads: %s' % gc_download)

    total = ff_download + gc_download
    data[2].append({'date': today, 'value': total})

    print('Total Downloads: %s' % str(total))

    archive = open('data/' + ff_ext + '.json', 'w')
    archive.write(json.dumps(data, indent=4, sort_keys=True))
    archive.close()

    with open('template.html') as template:
        template = str(template.read()).replace('[-]', ff_ext)
        template = template.replace('[/]', ff_ext.title())
        save_template = open('data/' + ff_ext + '.html', 'w')
        save_template.write(template)
        save_template.close()

    html = html + '<a href="' + ff_ext + '.html" target="_blank>'
    + ff_ext.title() + '</a><br>'

html = html + '</body></html>'
index = open('/data/index.html', 'w')
index.write(html)
index.close()

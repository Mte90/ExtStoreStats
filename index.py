#!/usr/bin/python3
import requests
import json
import time
import lxml.html
import os.path
import re
import sys
import configparser
from lxml.cssselect import CSSSelector

# Load configuration
config = configparser.RawConfigParser()
path = os.path.dirname(sys.argv[0]) + '/'
config.readfp(open(path + 'config.ini'))
list_ext = config.get('Extension', 'list').split(",")

today = time.strftime("%Y-%m-%d")
html = '<html><head><title>ExtStoreStats</title></head><body>'

for ext in list_ext:
    ext = ext.strip()
    ff_ext = config.get(ext, 'firefox')
    gc_ext = config.get(ext, 'chrome')
    generate_json = True

    data = [[], [], []]
    if os.path.isfile(path + 'data/' + ff_ext + '.json'):
        with open(path + 'data/' + ff_ext + '.json') as data_file:
            data = json.load(data_file)
            if data[0][-1]['date'] == today:
                print('%s already processed, skip to another extension!' % ff_ext)
                generate_json = False

    if generate_json is True:
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
        if len(results) != 0:
            gc_download = int(re.sub("[^0-9]", "", results[0].text))
        else:
            gc_download = 0

        data[1].append({'date': today, 'value': gc_download})

        print('Downloads: %s' % gc_download)

        total = ff_download + gc_download
        data[2].append({'date': today, 'value': total})

        print('Total Downloads: %s' % str(total))

        archive = open(path + 'data/' + ff_ext + '.json', 'w')
        archive.write(json.dumps(data, indent=4, sort_keys=True))
        archive.close()

    with open(path + 'template.html') as template:
        template = str(template.read()).replace('[-]', ff_ext)
        template = template.replace('[/]', ff_ext.title())
        save_template = open(path + 'data/' + ff_ext + '.html', 'w')
        save_template.write(template)
        save_template.close()

    html = html + '<a href="' + ff_ext + '.html" target="_blank">'
    html = html + ff_ext.title() + '</a><br>'

html = html + '</body></html>'
index = open(path + 'data/index.html', 'w')
index.write(html)
index.close()

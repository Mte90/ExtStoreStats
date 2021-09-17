#!/usr/bin/python3
import requests
import json
import time
from lxml import etree
from io import StringIO
import os.path
import re
import sys
import configparser

# Load configuration
config = configparser.RawConfigParser()
path = os.path.dirname(sys.argv[0]) + '/'
config.read_file(open(path + 'config.ini'))
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

        print('Firefox Downloads: %s' % ff_download)

        gc_download = 0
        if gc_ext != '':
            print('Google Web Store Extension Gathering for: %s' % gc_ext)

            r = requests.get('https://chrome.google.com/webstore/detail/%s' % gc_ext, headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
            }, cookies = { 'CONSENT': 'YES+cb.20210912-13-p0.it+FX+750' })
            results = etree.parse(StringIO(r.text), etree.HTMLParser(recover=True))
            results = results.xpath('//meta[@itemprop="interactionCount"]/@content')
            results = results[0].replace('UserDownloads:','')
            if len(results) != 0:
                gc_download = int(re.sub("[^0-9]", "", results))
            else:
                gc_download = 0

            print('Chrome Downloads: %s' % gc_download)

        data[1].append({'date': today, 'value': gc_download})

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

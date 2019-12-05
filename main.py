#!/usr/bin/env python3.6

import os
import re
import sys
import json
import subprocess
from subprocess import Popen, PIPE, check_output, CalledProcessError
from datetime import datetime, timezone

dir_path = os.path.dirname(os.path.realpath(__file__))
utc_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def firstPull(channelId, channelName, path, dateNow, format, token):
    try:
        cmd = 'docker run --rm -v $(pwd):/app/out -u $(id -u):$(id -g) tyrrrz/discordchatexporter export -t "NjUxODE4MzczNzI1OTQ1ODU2.XefbNw.RRGXTTWIUq37U-hJuLog-fo1-Eo" -b -c 497080413387489291 -f HtmlDark -o labsHTML -p 100'
        Popen(cmd, universal_newlines=True, shell=True,
              executable="/bin/bash")

    except:
        print("An exception occurred")


def cleanName(word):
    word = word.lower()
    word = re.sub(r'([^\s\w]|_)+', '', word)
    word = re.sub('[^A-z0-9 -]', '', word).lower()
    wordArr = word.split()
    word = "-".join(wordArr)
    return word


with open(os.path.join(dir_path, 'config.json')) as g:
    config = json.load(g)
    token = config['token']


firstPull("", "", "", "", "", "")

# firstPull("497080413387489291", "",
#        "./output/kmdlabs", utc_now, "HtmlDark", token)
'''
path = './kmdlabs/text'
files = os.listdir(path)
for index, file in enumerate(files):
    newFile = file.split()[4].lstrip('[')+'.txt'
    os.rename(os.path.join(path, file), os.path.join(path, newFile))
'''
'''
with open(os.path.join(dir_path, 'channels.json')) as f:
    textChannels = json.load(f)
    for categoryId, category in textChannels.items():
        dirPathCreate = os.path.join(
            dir_path, 'output', cleanName(category['name']))
        try:
            os.makedirs(dirPathCreate)
        except OSError:
            print("Creation of the directory %s failed" % dirPathCreate)
        else:
            print("Successfully created the directory %s " % dirPathCreate)
'''

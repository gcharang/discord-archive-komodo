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

outFormats = ['HtmlDark', 'HtmlLight', 'PlainText', 'Csv']


def firstPull(pwd, channelId, path, dateNow, outFormat, token):
    try:
        cmd = 'docker run --rm -v '+pwd+':/app/out -u $(id -u):$(id -g) tyrrrz/discordchatexporter export -t "' + \
            token + '" -b -c ' + channelId + ' -f ' + \
            outFormat + ' -o "' + path + '" -p 100'
        print(cmd)
        p = Popen(cmd, shell=True, universal_newlines=True,
                  executable="/bin/bash")
        p.wait()
    except:
        print("An exception occurred")


def cleanName(word):
    word = word.lower()
    word = re.sub('[^A-z0-9 -]', '', word).lower()
    wordArr = word.split()
    word = "-".join(wordArr)
    return word


with open(os.path.join(dir_path, 'config.json')) as g:
    config = json.load(g)
    token = config['token']
"""
firstPull(dir_path, "497080413387489291",
          "./output/kmdlabs", utc_now, "HtmlDark", token)

path = './kmdlabs/text'
files = os.listdir(path)
for index, file in enumerate(files):
    newFile = file.split()[4].lstrip('[')+'.txt'
    os.rename(os.path.join(path, file), os.path.join(path, newFile))
"""

with open(os.path.join(dir_path, 'channels.json')) as f:
    textChannels = json.load(f)
    for outFormat in outFormats:
        for categoryId, category in textChannels.items():
            dirPathCreate = os.path.join(
                dir_path, 'output', outFormat.lower(), cleanName(category['name']))
            if(not os.path.exists(dirPathCreate)):
                try:
                    original_umask = os.umask(0)
                    os.makedirs(dirPathCreate)
                except OSError:
                    print("Creation of the directory %s failed" %
                          dirPathCreate)
                else:
                    print("Successfully created the directory %s " %
                          dirPathCreate)
                finally:
                    os.umask(original_umask)
            else:
                print("the dir already exists %s " % dirPathCreate)
            for channelId, channelName in category['channels'].items():
                exportPath = os.path.join(
                    dirPathCreate, cleanName(channelName))
                print(exportPath)
                firstPull(dir_path, channelId,
                          exportPath, utc_now, outFormat, token)
"""
with open(os.path.join(dir_path, 'channels.json')) as f:
    textChannels = json.load(f)
    for outFormat in outFormats:
        for categoryId, category in textChannels.items():
            dirPathCreate = os.path.join(
                dir_path, 'output', outFormat.lower(), cleanName(category['name']))
            for channelId, channelName in category['channels'].items():
                exportPath = os.path.join(
                    dirPathCreate, cleanName(channelName))
                files = os.listdir(exportPath)
                for index, file in enumerate(files):
                    if outFormat == 'PlainText':
                        newFile = file.split()[4].lstrip('[')+'.txt'
                    elif outFormat == 'HtmlDark':
                        newFile = file.split()[4].lstrip('[')+'.html'
                    elif outFormat == 'HtmlLight':
                        newFile = file.split()[4].lstrip('[')+'.html'
                    elif outFormat == 'Csv':
                        newFile = file.split()[4].lstrip('[')+'.csv'
                    os.rename(os.path.join(exportPath, file),
                              os.path.join(exportPath, newFile))
"""

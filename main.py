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
        cmd = 'docker run --rm -v $(pwd):/app/out -u $(id -u):$(id -g) tyrrrz/discordchatexporter export -t "' + \
            token + '" -b -c ' + channelId + ' -f ' + \
            outFormat + ' --before ' + dateNow + ' -o "' + path + '" -p 100'
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


with open(os.path.join(dir_path, 'channels.json')) as f:
    textChannels = json.load(f)
    for outFormat in outFormats:
        for categoryId, category in textChannels.items():
            dirPathCreate = os.path.join(
                './output', outFormat.lower(), cleanName(category['name']))
            for channelId, channelName in category['channels'].items():
                exportPath = os.path.join(
                    dirPathCreate, cleanName(channelName))
                print(exportPath)
                firstPull(dir_path, channelId,
                          exportPath, utc_now, outFormat, token)
                files = os.listdir(exportPath)
                for index, file in enumerate(files):
                    if outFormat == 'PlainText':
                        fileArr = re.findall(r"\[(.*?)\]", file)
                        newFile = fileArr[len(fileArr)-1].split()[0]+'.txt'
                    elif outFormat == 'HtmlDark':
                        fileArr = re.findall(r"\[(.*?)\]", file)
                        newFile = fileArr[len(fileArr)-1].split()[0]+'.html'
                    elif outFormat == 'HtmlLight':
                        fileArr = re.findall(r"\[(.*?)\]", file)
                        newFile = fileArr[len(fileArr)-1].split()[0]+'.html'
                    elif outFormat == 'Csv':
                        fileArr = re.findall(r"\[(.*?)\]", file)
                        newFile = fileArr[len(fileArr)-1].split()[0]+'.csv'
                    os.rename(os.path.join(exportPath, file),
                              os.path.join(exportPath, newFile))


'''
For anyone else looking at the wget solution, I had to add a couple more flags (cygwin version, Windows) to get attached images to download:

wget -x -k --mirror -H -Ddiscordapp.com,localhost,cdn.discordapp.com,cdnjs.cloudflare.com -e robots=off -U mozilla http://localhost/

(Easy hosting solution: python -m SimpleHTTPServer 80)

I was getting a lot of robots.txt and no image files without the robots and user agent flags.
https://github.com/Tyrrrz/DiscordChatExporter/issues/21#issuecomment-536213642
'''

#!/usr/bin/env python3.6

import os
import re
import sys
import json
import subprocess
from subprocess import Popen, PIPE, check_output, CalledProcessError
from datetime import datetime, date, timezone, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))

utc_now = datetime.now(timezone.utc).strftime("%Y-%b-%d")

outFormats = ['HtmlDark', 'HtmlLight', 'PlainText', 'Csv']

with open('dateOfFirstBefore', 'r') as p:
    dateOfFirstBefore = p.readline().strip()
    firstDir = './docs/.vuepress/public/before-' + dateOfFirstBefore


def firstPull(channelId, path, dateNow, outFormat, token):
    try:
        cmd = 'docker run --rm -v $(pwd):/app/out -u $(id -u):$(id -g) tyrrrz/discordchatexporter export -t "' + \
            token + '" -b -c ' + channelId + ' -f ' + \
            outFormat + ' --before ' + dateNow + ' -o "' + path + '" -p 100'
        p = Popen(cmd, shell=True, universal_newlines=True,
                  executable="/bin/bash")
        p.wait()
    except:
        print("An exception occurred")


def normalPull(channelId, path, dateOfBefore, dateOfAfter, outFormat, token):
    try:
        cmd = 'docker run --rm -v $(pwd):/app/out -u $(id -u):$(id -g) tyrrrz/discordchatexporter export -t "' + \
            token + '" -b -c ' + channelId + ' -f ' + \
            outFormat + ' --before ' + dateOfBefore + ' --after ' + \
            dateOfAfter + ' -o "' + path + '" -p 100'
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


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['path'] = path
        d['children'] = [path_to_dict(os.path.join(path, x))
                         for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d


def clean_file_names(path):
    for dirName, subdirList, fileList in os.walk(path):
        if (len(fileList) == 1):
            print("renaming: "+fileList[0])
            newFile = '1.' + fileList[0].split('.')[1]

            os.rename(os.path.join(dirName, fileList[0]),
                      os.path.join(dirName, newFile))


with open(os.path.join(dir_path, 'config.json')) as g:
    config = json.load(g)
    token = config['token']


with open(os.path.join(dir_path, 'channels.json')) as f:
    textChannels = json.load(f)
    for outFormat in outFormats:
        for categoryId, category in textChannels.items():

            for channelId, channelName in category['channels'].items():

                if not os.path.isdir(firstDir):
                    dirPathCreate = os.path.join('./docs/.vuepress/public',
                                                 'before-'+utc_now, outFormat.lower(), cleanName(category['name']))
                    exportPath = os.path.join(
                        dirPathCreate, cleanName(channelName))
                    print(exportPath)
                    firstPull(channelId,
                              exportPath, utc_now, outFormat, token)
                    with open('dateOfFirstBefore', 'w+') as q:
                        q.write(utc_now)
                    files = os.listdir(exportPath)
                    for index, file in enumerate(files):
                        if outFormat == 'PlainText':
                            fileArr = re.findall(r"\[(.*?)\]", file)
                            newFile = fileArr[len(
                                fileArr)-1].split()[0]+'.txt'
                        elif outFormat == 'HtmlDark':
                            fileArr = re.findall(r"\[(.*?)\]", file)
                            newFile = fileArr[len(
                                fileArr)-1].split()[0]+'.html'
                        elif outFormat == 'HtmlLight':
                            fileArr = re.findall(r"\[(.*?)\]", file)
                            newFile = fileArr[len(
                                fileArr)-1].split()[0]+'.html'
                        elif outFormat == 'Csv':
                            fileArr = re.findall(r"\[(.*?)\]", file)
                            newFile = fileArr[len(
                                fileArr)-1].split()[0]+'.csv'
                        os.rename(os.path.join(exportPath, file),
                                  os.path.join(exportPath, newFile))

                else:
                    delta = datetime.now(timezone.utc) - datetime.strptime(
                        dateOfFirstBefore+'-+0000', '%Y-%b-%d-%z')
                    dateOfAfter = dateOfFirstBefore
                    for i in range(delta.days + 1):
                        day = datetime.strptime(
                            dateOfFirstBefore+'-+0000', '%Y-%b-%d-%z') + timedelta(days=i)
                        currDate = day.strftime("%Y-%b-%d")

                        dirPathCreate = os.path.join('./docs/.vuepress/public',
                                                     'after-'+dateOfFirstBefore, currDate, outFormat.lower(), cleanName(category['name']))
                        exportPath = os.path.join(
                            dirPathCreate, cleanName(channelName))

                        if not currDate == dateOfFirstBefore and not os.path.isdir(exportPath):
                            print(exportPath)
                            normalPull(channelId, exportPath, currDate,
                                       dateOfAfter, outFormat, token)
                            files = os.listdir(exportPath)
                            for index, file in enumerate(files):
                                if outFormat == 'PlainText':
                                    fileArr = re.findall(r"\[(.*?)\]", file)
                                    newFile = fileArr[len(
                                        fileArr)-1].split()[0]+'.txt'
                                elif outFormat == 'HtmlDark':
                                    fileArr = re.findall(r"\[(.*?)\]", file)
                                    newFile = fileArr[len(
                                        fileArr)-1].split()[0]+'.html'
                                elif outFormat == 'HtmlLight':
                                    fileArr = re.findall(r"\[(.*?)\]", file)
                                    newFile = fileArr[len(
                                        fileArr)-1].split()[0]+'.html'
                                elif outFormat == 'Csv':
                                    fileArr = re.findall(r"\[(.*?)\]", file)
                                    newFile = fileArr[len(
                                        fileArr)-1].split()[0]+'.csv'
                                os.rename(os.path.join(exportPath, file),
                                          os.path.join(exportPath, newFile))
                        else:
                            pass
                        dateOfAfter = currDate


clean_file_names('./docs/.vuepress/public')

with open('./docs/.vuepress/theme/dirStructure.js', 'w+') as outfile:
    outfile.write("export default ")
    json.dump(path_to_dict('./docs/.vuepress/public'), outfile)
    outfile.write(";")

with open('./docs/.vuepress/public/dirStructure.js', 'w+') as outfile:
    outfile.write("export default ")
    json.dump(path_to_dict('./docs/.vuepress/public'), outfile)
    outfile.write(";")


'''

For anyone else looking at the wget solution, I had to add a couple more flags (cygwin version, Windows) to get attached images to download:

wget -x -k --mirror -H -Ddiscordapp.com,localhost,cdn.discordapp.com,cdnjs.cloudflare.com -e robots=off -U mozilla http://localhost/

(Easy hosting solution: python -m SimpleHTTPServer 80)

I was getting a lot of robots.txt and no image files without the robots and user agent flags.
https://github.com/Tyrrrz/DiscordChatExporter/issues/21#issuecomment-536213642
'''

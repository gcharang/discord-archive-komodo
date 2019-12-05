#!/usr/bin/env python3.6

import os
path = './kmdlabs/text'
files = os.listdir(path)


for index, file in enumerate(files):
    newFile = file.split()[4].lstrip('[')+'.txt'
    os.rename(os.path.join(path, file), os.path.join(path, newFile))

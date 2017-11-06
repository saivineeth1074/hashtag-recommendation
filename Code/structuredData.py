"""
    Program: Create structured dataset from files containing posts
"""

import os
import re, string
import csv
import requests

f = open("politics_data.csv", "w")
writer = csv.writer(f, delimiter=',')
writer.writerow(["Id", "Section", "Title", "Timestamp", "URL", "Description", "Content", "Tags"])

#Dir of the files to be structured
dirPath = "./crawled-data_politics/"
fileCount = 0

for filename in os.listdir(dirPath):
    file = open(dirPath + filename)
    if(file):
        lines = file.readlines()
        if(len(lines) <= 1):
            continue

        fileCount += 1
        url = lines[0][5:].strip()
        timestamp = lines[1][6:].strip()
        section = lines[2][9:].strip()
        title = lines[3][7:]
        desc = lines[4][6:]
        content = lines[5][9:]
        tags = lines[-1][6:].strip()

        title = re.sub("[\s+]?&.*;[\s+]?", ' ', title)
        title = re.sub("\s+", " ", title).strip(". $-:;~'?")
        desc = re.sub("[\s+]?&.*;[\s+]?", ' ', desc)
        desc = re.sub("\s+", " ", desc).strip(". $-:;~'?")
        content = re.sub("[\s+]?&.*;[\s+]?", ' ', content)
        content = re.sub("\s+", " ", content).strip(". $-:;~'?")

        row = [fileCount, section, title, timestamp, url, desc, content, tags]
        writer.writerow(row)

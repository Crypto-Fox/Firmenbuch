# -*- coding: utf-8 -*-
import json

def writeToJson(filename,data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,indent=2)

def readFromJson(filename):
    with open(filename) as infile:
        fileJson = json.load(infile)
        return fileJson
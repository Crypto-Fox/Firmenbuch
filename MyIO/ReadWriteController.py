# -*- coding: utf-8 -*-
import ReadWriteJson
import ReadWriteXslx
import os

#This module will be responsible for reading and writting to and form files throug using the the imported classes.
def writeData(path,data,nodeData,edgeData):
    nameJson = path + "myJson.json"
    nameXlsx = path + "myXl.xlsx"
    nameNetwork = path + "network.xlsx"

    #Check if our directory exists
    if not os.path.exists(path):
        os.makedirs(path)

    ReadWriteJson.writeToJson(nameJson,data)
    ReadWriteXslx.writeDictToExcel(nameXlsx,data)
    ReadWriteXslx.writeNetworkData(nameNetwork,nodeData,edgeData)



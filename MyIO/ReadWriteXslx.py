# -*- coding: utf-8 -*-
import xlsxwriter
import xlrd

#This is the main function for writting the dict to our database
def writeDictToExcel(savename,dataDict):
    workbook = xlsxwriter.Workbook(savename)
    sheet = workbook.add_worksheet()
    #Write the dict to excel
    row = 0
    intKeys = list()
    for key in dataDict.keys():
        intKeys.append(int(key))
    sortedKeys = sorted(intKeys)
    for i in range(len(sortedKeys)):
        key = str(sortedKeys[i])
        value = dataDict[key]
        sheet.write(row,0,key)
        row =writeDictEntry(value,sheet, row+1, 1)
    workbook.close()
    print "done"

#write our network data to an excel file
def writeNetworkData(nameNetwork,nodeData,edgeData):
    workbook = xlsxwriter.Workbook(nameNetwork)
    sheetNodes = workbook.add_worksheet("nodes")
    sheetEdges = workbook.add_worksheet("edges")

    for i in range(len(nodeData)):
        sheetNodes.write(i,0,nodeData[i])

    for i in range(len(edgeData)):
        for j in range(len(edgeData[i])):
            sheetEdges.write(i,j,edgeData[i][j])

    workbook.close()

def readNetworkData(filename):
    workbook = xlrd.open_workbook(filename)
    node_sheet = workbook.sheet_by_name("nodes")
    edge_sheet = workbook.sheet_by_name("edges")
    edges = list()
    nodes = list()

    #Get the nodes
    for i in range(node_sheet.nrows):
        nodes.append(unicode(node_sheet.cell(i,0).value))

    # Get the edges
    for i in range(edge_sheet.nrows):
        edges.append((unicode(edge_sheet.cell(i, 0).value),unicode(edge_sheet.cell(i, 1).value)))

    #workbook.close()

    return (nodes,edges)







#This function is our recursive funciton that gets called repeatedly to ensure we print the whole dictionnary
def writeDictEntry(dataDict,sheet,row,column):
    #Write our key
    row = row
    for i in range(len(dataDict.keys())):
        #Define key value pair for ease of use
        key = dataDict.keys()[i]
        value = dataDict.values()[i]

        #Make sure our encoding is correct
        if isinstance(key, str):keyOut = key.decode("utf-8")
        else:keyOut = key
        if isinstance(value, str):valOut = value.decode("utf-8")
        else: valOut = value

        #Check if our value is a dict
        if isinstance(value,dict):
            #Write our key
            sheet.write(row,column,keyOut)
            #Then call the function again 1 row and column deeper
            row = writeDictEntry(value,sheet,row+1,column+1)+1

        #If our value is not a dict
        else:
            #Write our key value pair and go to the next row
            sheet.write(row,column,keyOut)
            sheet.write(row,column+1,valOut)
            row+=1

    return row

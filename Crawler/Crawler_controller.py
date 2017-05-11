# -*- coding: utf-8 -*-
import Crawler_results
import Crawler_companies
from MyIO import ReadWriteController
from Constants import *
import datetime

#This function runs our crawler with the necessary inputs
def runCrawler(where,what,statusVar,resultVar):

    #Get all the basic information from the companies we find on the result pages
    basicCompanies,numberOfResults = Crawler_results.searchResultPages(where,what,statusVar,resultVar)

    #Get all the company info from the individual companies
    detailedCompanies = Crawler_companies.getDetailedCompanies(basicCompanies,numberOfResults,statusVar)

    #Save our data
    date = datetime.date.today().strftime("%Y%m%d")
    resultPath = u"/Users/tobiasfuma/Desktop/FirmenbuchCrawler/Results/"
    name = date + "_" + where + "_" + what
    path = resultPath + name + "/"
    ReadWriteController.writeData(path,detailedCompanies,nodes,edges)


    statusVar.set("Done")



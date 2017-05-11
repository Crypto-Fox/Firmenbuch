# -*- coding: utf-8 -*-
import re

import Crawler_person
import mySoupFuncs
from Constants import *


def getDetailedCompanies(basicCompanies,numberOfResults,statusVar):
    detailedCompanies = dict()
    depthLimit = 2

    #Loop through all the companies
    for i in range(len(basicCompanies.keys())):
        # Update our frame
        statusVar.set("Retrieving data from pages: " + str(i) + "/" + str(numberOfResults))

        #Get the company we want to get more info on
        companyDict = basicCompanies.values()[i]
        companyPage = mySoupFuncs.getSoup(companyDict["FirmenbuchURL"])
        visitedCompanies = [companyDict["FirmenbuchURL"]]

        #Get detailed company info
        detailedCompanies[str(i)] = getDetailedInfo(companyPage,companyDict,visitedCompanies,0,depthLimit)

    return detailedCompanies

# Fetch the results
def getDetailedInfo(companyPage, companyDict, visitedLinks, depth, depthLimit):
    if depth < depthLimit:
        companyDict["URL"] = getURL(companyPage)
        companyDict["Email"] = getEmail(companyPage)
        companyDict["Phone"] = getPhone(companyPage)
        companyDict["Founding date"] = getFoundingDate(companyPage)
        companyDict["Employees"] = getEmployees(companyPage)
        companyDict["Description"] = getDescription(companyPage)
        companyDict["Revenue"] = getRevenue(companyPage)
        (stakeholders, investments, employees) = getAssociations(companyPage, companyDict["Name"], visitedLinks, depth, depthLimit)
        companyDict["Associations"] = dict()
        companyDict["Associations"]["Stakeholders"] = stakeholders
        companyDict["Associations"]["Investments"] = investments
        companyDict["Associations"]["Employees"] = employees
    else:
        return companyDict


    return companyDict

# Gets the web address of a company
def getURL(moreInfoSite):
    try:
        return moreInfoSite.find_all("a", itemprop="url")[0]["href"]
    except:
        return "NA"


# Gets the web address of a company
def getEmail(moreInfoSite):
    try:
        return moreInfoSite.find_all("meta", property="og:email")[0]["content"]
    except:
        return "NA"


# Gets the phone number of a company
def getPhone(moreInfoSite):
    try:
        return moreInfoSite.find_all("div", class_="mobile-portrait-row phone")[0].find_all("a")[0]["href"]
    except:
        return "NA"


# Gets the founding date
def getFoundingDate(moreInfoSite):
    try:
        return moreInfoSite.find_all("span", itemprop="foundingDate")[0].string
    except:
        return "NA"


# Gets the number of employees
def getEmployees(moreInfoSite):
    try:
        return moreInfoSite.find_all("span", itemprop="numberOfEmployees")[0].string
    except:
        return "NA"


# Gets the company description
def getDescription(moreInfoSite):
    try:
        return re.sub("Eingetragener Gegenstand: ", "", moreInfoSite.find_all("span", itemprop="description")[0].string,
                      count=1)
    except:
        return "NA"

def getAssociations(companyPage, name, visitedLinks, depth, depthLimit):
    #Set default value of our lists to NA
    employees = "NA"
    stakeholders = "NA"
    investments = "NA"

    # Get the relevant blue box section
    crefoSoup = companyPage.find("div", id="crefo")

    # Split between handelnde personen and beteiligungen
    terms = ["Handelnde Personen:","Anteilseigner:", "Beteiligungen von " + name.strip()]
    segments = mySoupFuncs.segmentByTerms(crefoSoup, terms)

    #If we have results
    if segments !="NA":
        for i in range(len(segments)):
            soup = mySoupFuncs.toSoup(segments[i][0])
            if segments[i][1] == "Handelnde Personen:":
                employees = getEmployeeInfo(soup, visitedLinks, depth, depthLimit)
            elif segments[i][1] == "Anteilseigner:":
                stakeholders = getStakeholders(soup, visitedLinks, depth, depthLimit)
            elif segments[i][1] == "Beteiligungen von " + name.strip():
                investments = getInvestments(soup, visitedLinks, depth, depthLimit)

    createCompanyEdges(stakeholders,investments, employees,name)

    return stakeholders,investments, employees

def createCompanyEdges(stakeholders,investments, employees,name):
    lists = list()
    if investments != "NA":
        lists.append(investments["Gesellschafter"])
        lists.append(investments["Aktionär"])
    if stakeholders != "NA":
        lists.append(stakeholders["Persons"]["Gesellschafter"])
        lists.append(stakeholders["Persons"][u"Aktionär"])
        lists.append(stakeholders["Companies"]["Gesellschafter"])
        lists.append(stakeholders["Companies"][u"Aktionär"])
    if employees != "NA":
        lists.append(employees[u"Geschäftsführer"])
        lists.append(employees[u"Aufsichtsrat"])
        lists.append(employees[u"Vorstand"])

    for associateList in lists:
        if associateList != "NA":
            for item in associateList.keys():
                edges.append((name,item))


# Get all companies this company is associated with
def getInvestments(soup, visitedLinks, depth, depthLimit):
    # Data Structures
    investments = dict()
    gesellschafter = dict()
    aktionaer = dict()

    # Get segments for investments
    terms = [u"Gesellschafter", u"Aktionär"]
    segments = mySoupFuncs.segmentByTerms(soup, terms)
    if segments =="NA": return "NA"

    # Retrieve the relevant information from the data structures
    for segment in segments:
        segmentSoup = mySoupFuncs.toSoup(segment[0])

        # If we have a foreign company
        company = dict()
        if "(Ausland)" in segment[0]:
            company["Name"] = "Failure: Ausland"

        else:
            try:
                #Get the basic company information
                company["Name"] = (segmentSoup.find("a").getText().strip())
                company["Link"] = (segmentSoup.find("a")["href"])
                try:company["Anteil"] = str(re.findall("\d+\,\d+", segment[0])[0].strip()) + "\%"
                except:company["Anteil"] = "NA"

                #Get more detailed information for the company
                if company["Link"] not in visitedLinks:
                    visitedLinks.append(company["Link"])
                    page = mySoupFuncs.getSoup(company["Link"])
                    company = getDetailedInfo(page, company, visitedLinks, depth + 1, depthLimit)

                #Add to the relevant section
                if segment[1] == u"Gesellschafter":gesellschafter[company["Name"]] = company
                elif segment[1] == u"Aktionär":aktionaer[company["Name"]] = company
                else:print "NEW COMPANY TYPE"

            except:print "Couldnt retrieve investments. Data with no link."


    investments["Gesellschafter"] = gesellschafter
    investments["Aktionär"] = aktionaer

    return investments


# Get all peoples names associated with the company
def getStakeholders(soup, visitedLinks, depth, depthLimit):
    # Data Structures we will reuturn
    stakeholders = dict()
    stakeholders["Persons"] = dict()
    stakeholders["Companies"] = dict()
    stakeholders["Persons"]["Gesellschafter"] = dict()
    stakeholders["Persons"][u"Aktionär"] = dict()
    stakeholders["Companies"]["Gesellschafter"] = dict()
    stakeholders["Companies"][u"Aktionär"] = dict()

    # Get info for handelnde personen first
    terms = [u"Gesellschafter", u"Aktionär"]
    segments = mySoupFuncs.segmentByTerms(soup, terms)
    if segments == "NA": return "NA"

    # Retrieve the relevant information from the data structures
    for segment in segments:
        segmentSoup = mySoupFuncs.toSoup(segment[0])

        # For companies
        if "Einzelperson" not in segment[0]:
            # If we have a foreign company
            company = dict()
            if "(Ausland)" in segment[0]:
                company["Name"] = "Failure: Ausland"

            else:
                try:
                    # Get the basic company information

                    company["Name"] = (segmentSoup.find("a").getText().strip())
                    company["Name"] = "Bad data. Please check manually"
                    company["Link"] = (segmentSoup.find("a")["href"])
                    try:
                        company["Anteil"] = str(re.findall("\d+\,\d+", segment[0])[0].strip()) + "\%"
                    except:
                        company["Anteil"] = "NA"

                    # Get more detailed information for the company
                    if company["Link"] not in visitedLinks:
                        visitedLinks.append(company["Link"])
                        page = mySoupFuncs.getSoup(company["Link"])
                        company = getDetailedInfo(page, company, visitedLinks, depth + 1, depthLimit)

                    if segment[1] == u"Gesellschafter":
                        stakeholders["Companies"]["Gesellschafter"][company["Name"]] = company
                    elif segment[1] == u"Aktionär":
                        stakeholders["Companies"][u"Aktionär"][company["Name"]] = company
                except:
                    print "Couldnt retrieve stakeholder. Data with no link"



        # For people
        elif "Einzelperson" in segment[0]:
            person = dict()
            # Get the name
            stringSection = repr(segmentSoup.getText())
            # If someone has a name with Herrn or Frau
            if "Herrn" in segment[0]:
                start = stringSection.index("Herrn")
                end = stringSection[start:].index("\\r")
                person["Name"] = (stringSection[start:start + end])
            elif "Frau" in segment[0]:
                start = stringSection.index("Frau")
                end = stringSection[start:].index("\\r")
                person["Name"] = (stringSection[start:start + end])
            else:
                start = segment[0].index("<br/>") + 5
                end = segment[0][start:].index("<br/>")
                person["Name"] = (stringSection[start:start + end]).strip()

            # Get link to person and more detailed information
            if segmentSoup.find("a"):
                person["Link"] = segmentSoup.find("a")["href"]
                if person["Link"] not in visitedLinks:
                    visitedLinks.append(person["Link"])
                    person = Crawler_person.getPersonInfo(person, visitedLinks, depth, depthLimit)

            # Try to get anteil
            try:
                anteil = str(re.findall("\d+\,\d+", segment[0])[0].strip()) + "\%"
                person["Anteil"] = anteil
            except:
                pass

            # Append to the relevant list
            if segment[1] == u"Gesellschafter":
                stakeholders["Persons"]["Gesellschafter"][person["Name"]] = person
            elif segment[1] == u"Aktionär":
                stakeholders["Persons"][u"Aktionär"][person["Name"]] = person
            else:
                print "NEW PERSON TYPE"

    return stakeholders


# Get all peoples names associated with the company
def getEmployeeInfo(soup, visitedLinks, depth, depthLimit):
    # Data Structures we will reuturn
    employees = dict()
    fuehrer = dict()
    aufsichtsrat= dict()
    vorstand = dict()

    # Get info for handelnde personen first
    terms = [u"Vorstand", u"Geschäftsführer", u"Aufsichtsrat"]
    segments = mySoupFuncs.segmentByTerms(soup, terms)
    if segments=="NA": return "NA"

    # Retrieve the relevant information from the data structures
    for segment in segments:
        segmentSoup = mySoupFuncs.toSoup(segment[0])
        person = dict()
        # Get the name
        stringSection = repr(segmentSoup.getText())
        #try:
        # If someone has a name with Herrn or Frau
        if "Herrn" in segment[0]:
            start = stringSection.index("Herrn")
            end = stringSection[start:].index("\\r")
            person["Name"] = (stringSection[start:start + end])
        elif "Frau" in segment[0]:
            start = stringSection.index("Frau")
            end = stringSection[start:].index("\\r")
            person["Name"] = (stringSection[start:start + end])
        else:
            start = segment[0].index("<br/>") + 5
            end = segment[0][start:].index("<br/>")
            person["Name"] = (stringSection[start:start + end]).strip()

        # Get link to person and more detailed information
        if segmentSoup.find("a"):
            person["Link"] = segmentSoup.find("a")["href"]
            if person["Link"] not in visitedLinks:
                visitedLinks.append(person["Link"])
                person = Crawler_person.getPersonInfo(person, visitedLinks, depth, depthLimit)

        # Append to the relevant dict
        if segment[1] == "Vorstand":
            vorstand[person["Name"]] = person
        elif segment[1] == "Aufsichtsrat":
            aufsichtsrat[person["Name"]] = person
        elif segment[1] == u"Geschäftsführer":
            fuehrer[person["Name"]] = person
        else:
            print "NEW PERSON TYPE"
        #except:
        #    print "FAILURE TO GET PERSON",segment

        #Add the new data to existing dict
        employees[u"Geschäftsführer"] = fuehrer
        employees[u"Aufsichtsrat"] = aufsichtsrat
        employees[u"Vorstand"] = vorstand

    return employees

# If "Umsatz" is present, find the section of string that will contain the revenue. Split this between millions and thousands
def getRevenue(moreInfoSite):
    [s.extract() for s in moreInfoSite(['style', 'script', '[document]', 'head', 'title'])]
    siteString = moreInfoSite.getText()
    #try:
    if "Umsatz" in siteString:
        index = siteString.index("Umsatz")
        # Relevant string
        relString = siteString[index:index + 120]
        # If we are dealing with millions
        if "," in relString:
            return str(float(re.findall("\d+,\d+", relString)[0].strip().replace(",", "").replace(".", "")) * 1000000)
        # If we are dealing with thousands
        else:
            return str(float(re.findall("\d+\.\d+", relString)[0].strip().replace(".", "")))
    else:
        return "NA"


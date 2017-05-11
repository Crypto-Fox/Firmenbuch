# -*- coding: utf-8 -*-
import Crawler_companies
import mySoupFuncs
from Constants import *
import random


def getPersonInfo(personDict,visitedCompanies,depth,depthLimit):
    uniqueID = str(random.randrange(100000000))
    nodes.append(personDict["Name"],uniqueID)
    person = personDict
    person["Investments"] = dict()
    person["Functions"] = dict()
    url = personDict["Link"]
    soup = mySoupFuncs.getSoup(url)
    body = soup.find("div",class_="modal-body")
    sections = mySoupFuncs.segmentByTerms(body,["<h2 class=\"h4\">"])

    if sections == "NA": return personDict

    #Now get beteiligungen and funktionen
    for section in sections:
        section = mySoupFuncs.toSoup(section[0])
        if "Beteiligungen" in section.getText():
            result = section.find_all("a", class_="blue")
            for subsection in result:
                company = dict()
                company["Name"] = subsection.getText().replace("\r"," ").replace("\n"," ").strip()
                company["Link"] = subsection["href"]
                if company["Link"] not in visitedCompanies:
                    edges.append((personDict["Name"],company["Name"]))
                    visitedCompanies.append(company["Link"])
                    page = mySoupFuncs.getSoup(company["Link"])
                    person["Investments"][company["Name"]]= Crawler_companies.getDetailedInfo(page,company,visitedCompanies,depth+1,depthLimit)


        elif "Funktionen" in section.getText():
            result = section.find_all("a", class_="blue")
            for subsection in result:
                company = dict()
                company["Name"] = subsection.getText().replace("\r", " ").replace("\n", " ").strip()
                company["Link"] = subsection["href"]
                if company["Link"] not in visitedCompanies:
                    edges.append((personDict["Name"], company["Name"]))
                    visitedCompanies.append(company["Link"])
                    page = mySoupFuncs.getSoup(company["Link"])
                    person["Functions"][company["Name"]] = Crawler_companies.getDetailedInfo(page, company,
                                                                                               visitedCompanies,depth+1,depthLimit)

    #Now we return the result
    return person

#"http://www.firmenabc.at/person/gunkel-walter_efrohl"



# -*- coding: utf-8 -*-
import mySoupFuncs
from Constants import *
from Formater import EnsureFormat


def searchResultPages(where, what,statusVar,resultVar):
    convWhere = EnsureFormat.convertUmlauts(where)
    convWhat = EnsureFormat.convertUmlauts(what)
    url = createUrl(convWhere, convWhat)
    (urls,pages) = getUrlsAndPages(url)
    numberOfResults = getNumberOfResults(pages[0])

    # Update frame variables
    resultVar.set("Found " +numberOfResults + " results")
    statusVar.set("Getting page results")

    # Get all the company sections from our pages found between these search terms with the location being correct
    term1 = '<span class="list-heading-base bg-dark-grey">Firmentreffer</span>'
    term2 = '<span class="list-heading-base bg-orange">Empfehlungen</span>'
    terms = [term1, term2]
    companySections = getCompanySections(pages, terms, where)

    #Use the company sections to retrieve the basic information about the relevant companies and their respective links
    #Such that we can then find out more information about these comapnies from these pages
    companies = getBasicInfo(companySections)
    return companies,numberOfResults

def getBasicInfo(companySections):
    companies = dict()
    for i in range(len(companySections)):
        company = dict()
        company["Name"]= getNames(companySections[i])
        nodes.append(company["Name"])
        company["Location"] = getLocations(companySections[i])
        company["FirmenbuchURL"] = getFirmenURL(companySections[i])

        #Add our company to the companies dict with an ID number
        companies[str(i)] = company

    return companies

def getNames(companySection):
    return companySection.find_all("h2", class_="card-heading pull-left", itemprop="name")[0].text

def getLocations(companySection):
    return companySection.find_all("span", itemprop="addressLocality")[0].text

# Finds the more information page
def getFirmenURL(companySection):
    url = companySection.find_all("a", itemprop="url")[0]["href"]
    return url


# Create the search string for www.firmenabc.at.
def createUrl(where, what):
    return "http://www.firmenabc.at/result.aspx?what=" + what + "&where=" + where + "&exact=false&inTitleOnly=false&l=&si=0&iid=&sid=&did=&cc="

# Get all URLS to the result pages
def getUrlsAndPages(url):
    urls = list()
    pages = list()
    urls.append(url)
    page = mySoupFuncs.getSoup(url)
    pages.append(page)

    nextURL = page.find("a",class_="next")
    i=2
    while nextURL.has_attr("href"):
        urls.append(nextURL["href"])
        newPage = mySoupFuncs.getSoup(nextURL["href"])
        pages.append(newPage)
        nextURL = newPage.find("a",class_="next")
        i +=1

    return (urls,pages)

#Get the number of results from the first page that we find
def getNumberOfResults(site):
    for strong in site("strong"):
        if "Firmentreffer" in strong.text:
            return strong.text.replace("Firmentreffer", "").strip()
        else:
            return "NA"


#Get the sections where the links and basic information to the company pages are found
def getCompanySections(pages, terms, where):
    # Get the relevant segments
    relevantSegments = list()
    companySections = list()
    count = 1
    for page in pages:
        segments = mySoupFuncs.segmentByTerms(page, terms)
        for segment in segments:
            if where.lower() in mySoupFuncs.toSoup(segment[0]).span.next_sibling.next_sibling.string.lower():
                relevantSegments.append(segment[0])

    for segment in relevantSegments:
        # Get all the company sections from this section
        sections = mySoupFuncs.toSoup(segment).find_all("li", class_="card result")
        for section in sections:
            companySections.append(section)

    return companySections





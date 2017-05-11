import urllib2
from bs4 import BeautifulSoup
import re


# Segments a soup by search terms, with a custom classification name (A,B,C or whatever) depending on whether
# We are going from A->B in this section, then classification is A. In case be go from D->A, then classification
# Is D
def segmentByTerms(soup, terms):
    indexDict = dict()
    # Turn the soup into unicode
    uniSoup = unicode(soup)
    # Find all the indexes for the different terms
    for i in range(len(terms)):
        indices = [m.start() for m in re.finditer(terms[i], uniSoup)]
        # Add all the indices to our indexDict
        for index in indices:
            indexDict[index] = terms[i]

    # Create a sorted index list
    sortedIndicies = sorted(indexDict.keys())
    if sortedIndicies == []:
        return "NA"

    # Create our segment list with classifications. This list is 2D.
    segments = list()
    for i in range(len(sortedIndicies) - 1):
        start = sortedIndicies[i]
        end = sortedIndicies[i + 1]
        segments.append([uniSoup[start:end], indexDict[start]])

    #Add the last segment, which is from the last index to the end
    start = sortedIndicies[-1]
    segments.append([uniSoup[start::], indexDict[start]])

    return segments


# Get soup from singular url
def getSoup(url):
    try:
        content = urllib2.urlopen(url).read()
        return BeautifulSoup(content, "lxml")

    except urllib2.HTTPError as e:
        print e, url
        return BeautifulSoup("","lxml")


# Get soups from url list
def getSoups(urlList):
    soups = list()
    for url in urlList:
        soups.append(getSoup(url))
    return soups


# This function will turn a list of unicode sections into one soup page
def toSoupList(unicodeList):
    toSoup = "\n".join(unicodeList)
    return BeautifulSoup(toSoup, "lxml")


def toSoup(uniSoup):
    return BeautifulSoup(uniSoup, "lxml")

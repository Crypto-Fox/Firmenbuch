import mySoupFuncs
import urllib2
import re
from MyIO import ReadWriteJson
import datetime

links = set()

def getLinks(pageURL,baseURL):
    global links
    try:
        soup = mySoupFuncs.getSoup((pageURL))

        for link in soup.find_all("a"):
            if "href" in link.attrs:
                if link.attrs["href"] not in links:
                    if baseURL in link.attrs["href"]:
                        if "@" not in link.attrs["href"]:
                            #We got a new page
                            newPage = link.attrs["href"]
                            print newPage
                            links.add(newPage)
                            #Exclude certain file extensions
                            exclude4 = [".pdf",".doc",".jpg",".ris"]
                            exclude5 = [".docx"]
                            #if link.attrs["href"][-4:].lower() == ".pdf" or link.attrs["href"][-4:].lower() == ".ris" or link.attrs["href"][-5:].lower() == ".docx" or link.attrs["href"][-4:].lower() == ".jpg": pass
                            if link.attrs["href"][-4:].lower() in exclude4 or link.attrs["href"][-5:].lower() in exclude5: print "EXCLUDED",link.attrs["href"][-5:].lower()
                            else:getLinks(newPage,baseURL)

    except: print "ERROR", pageURL



def saveAllPageContents(urlList,baseURL):
    pages = dict()
    myJson = dict()
    for url in urlList:
        try:
            pages[url]=mySoupFuncs.getSoup(url).prettify()
        except:
            pages[url] = "Not gathered"

    #Save our results with the current date and time
    strTime = datetime.datetime.strftime(datetime.datetime.today(),"%Y-%m-%d %H:%M:%S")
    filename = u"/Users/tobiasfuma/Desktop/FirmenbuchCrawler/Results/"+baseURL+".json"
    try:
        myJson = ReadWriteJson.readFromJson(filename)
    except:
        print "ERROR IN READING"

    myJson[strTime] = pages
    ReadWriteJson.writeToJson(filename,myJson)
    return pages




if __name__ == "__main__":
    baseURL ="bmi.gv.at"
    #baseURL = "fizz112.com"
    url = "http://"+baseURL
    getLinks(url,baseURL)
    print links
    pages = saveAllPageContents(links,baseURL)
    print pages



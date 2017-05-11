# -*- coding: utf-8 -*-

#This module forces all the data i deal with to be unicode.
def ensureUnicode(text):
    if isinstance(text,str):
        return unicode(text,"utf-8")
    elif isinstance(text,int) or isinstance(text,float):
        return unicode(str(text),"utf-8")
    elif isinstance(text,unicode):
        return text
    else:
        print "Data type not considered"

def convertUmlauts(text):
    return text.replace(u"ä", 'ae').replace(u"ö", 'oe').replace(u"ü", 'ue').replace(u"ß", 'ss')


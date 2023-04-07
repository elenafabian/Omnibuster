import sys
import os, urllib.parse, urllib.request
import io
import codecs
import xml.sax
from xml.sax.handler import feature_external_ges

import Omnibuildingblocks

# module: https://github.com/python/cpython/blob/3.11/Lib/xml/sax/saxutils.py

class OmniBillHandler(xml.sax.ContentHandler):
    def __init__(self):
        self._locator = None
        self._indent = 0
        self._file = open("temp2.txt", "a")

    def resolveEntity(self, publicID, systemID):
        print ("TestHandler.resolveEntity(): %s %s" % (publicID, systemID))
        return systemID

    def skippedEntity(self, name):
        print ("TestHandler.skippedEntity(): %s" % (name))

    def notationDecl(self, name, publicID, systemID):
        print ("TestHandler.notationDecl(): %s %s" % (publicID, systemID))

    def unparsedEntityDecl(self, name, publicID, systemID, ndata):
        print ("TestHandler.unparsedEntityDecl(): %s %s" % (publicID, systemID))

    def startElement(self, name, attrs):
        # e.g., element: <a href:"google.com">Google!</a>
        # name: the type of elemment, e.g., a
        # attrs: the attributes, e.g., href:"google.com" 
        name = name.strip()
        xhtml = "<" + name + " "
        for (name, value) in attrs.items():
            xhtml += name + "=\"" + value + "\" "
        xhtml = xhtml.strip()
        xhtml += ">\n"
        print(xhtml)
        for i in range(self._indent):
            self._file.write("\t")
        self._file.write(xhtml)
        self._indent += 1

    def characters(self, content):
        content = content.strip()
        print(content)
        for i in range(self._indent):
            self._file.write("\t")
        self._file.write(content + "\n")

    def endElement(self, name):
        name = name.strip()
        self._indent -= 1
        for i in range(self._indent):
            self._file.write("\t")
        xhtml = "</" + name + ">\n"
        print(xhtml)
        self._file.write(xhtml)
        
    def startDocument(self):
        # self._file.write("<!DOCTYPE html>\n<head>\n\t<title>Omnibuster Bill Render</title>\n\t<link rel=\"stylesheet\" href=\"HR_Temp_Style.css\">\n</head>\n")
        return super().startDocument()
    
    def endDocument(self):
        # self._file.write("</body>")
        self._file.close()
        return super().endDocument()
    

print("\n\nOmniparseSAX.py is running!\n\n")

parser = xml.sax.make_parser()
parser.setFeature(feature_external_ges, True)
handler = OmniBillHandler()
parser.setContentHandler(handler)
parser.setEntityResolver(handler)
parser.setDTDHandler(handler)

bill = open("originalXMLs/114_6450.xml")

try:
    parser.parse(bill)
except xml.sax.SAXParseException as err:
    print("\nError: %s\n" % err)
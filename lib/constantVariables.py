#  -*- coding: utf-8 -*-

# lib to measure time
import time
#namedtuple
from collections import namedtuple


# import the handlers
from lib.docxHandler import DocxHandler
from lib.odtHandler import OdtHandler
from lib.txtHandler import TxtHandler
from lib.rtfHandler import RtfHandler

'''
Constant variables and tools
'''

# constant variables for DocxHandler

# filelist -> main part of the document, header 1-2-3, footer 1-2-3
FILELIST_DOCX = ['word/document.xml','word/header1.xml','word/header2.xml','word/header3.xml','word/footer1.xml','word/footer2.xml','word/footer3.xml']
# tag names for the dom tree
# paragraph node
DOCX_PARAGRAPH = "w:p"
# inner section node
DOCX_SECTION = "w:r"
# text node
DOCX_TEXT = "w:t"

# constant variables for OdtHandler

#filelist -> main part of the document and headers,footers
FILELIST_ODT = ["content.xml", "styles.xml"]
# tag names for dom tree
# paragraph node
ODT_PARAGRAPH = "text:p"
# text node
ODT_TEXT_TAG = "#text"
# space tag
ODT_SPACE_TAG = "text:s"


Match=namedtuple('Match','a b size')
# text fitting
chars = ['.', ',', '-', ' ']

# construction
creator = \
    {
        'docx' : DocxHandler,
        'odt' : OdtHandler,
        'txt' : TxtHandler,
        'rtf' : RtfHandler
    }

# supported file formats
VALID_EXTENSIONS = ["docx", "odt", "rtf", "txt"]


# tool to measure execution time
class ExecutionMeter():

    def __init__(self):
        self.start()
    # start the watch
    def start(self):
        self.startime=time.time()
    # stop the watch, and return the elapsed time in formatted string
    def stop(self):
        return ("--- %s seconds ---" % (time.time() - self.startime))


# costum exception class
class MyError(Exception):
    # constructor
    def __init__(self,value):
        self.value=value
    # return the string representation of self.value
    def __str__(self):
        return repr(self.value)

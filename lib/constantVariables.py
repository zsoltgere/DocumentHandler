#  -*- coding: utf-8 -*-

from collections import namedtuple
from lib.docxHandler import DocxHandler
from lib.odtHandler import OdtHandler
from lib.txtHandler import TxtHandler

'''
Constant variables and tools
'''

# constant variables for DocxHandler

# filelist -> main part of the document, header 1-2-3, footer 1-2-3
FILELIST_DOCX = ['word/document.xml','word/header1.xml','word/header2.xml','word/header3.xml','word/footer1.xml','word/footer2.xml','word/footer3.xml','word/footnotes.xml']
# tag names for the dom tree
DOCX_PARAGRAPH = "w:p"  # paragraph node
DOCX_SECTION = "w:r"    # inner section node
DOCX_TEXT = "w:t"       # text node
#changes
DOCX_INSERTION_TAG = "w:ins"
DOCX_DELETION_TAG = "w:del"
DOCX_DATE_TAG = "w:date"
DOCX_AUTHOR_TAG = "w:author"
DOCX_ID_TAG = "w:id"

docx_mode_selector = {
    "deletion" : DOCX_DELETION_TAG,
    "insertion" : DOCX_INSERTION_TAG
}

# constant variables for OdtHandler

#filelist -> main part of the document and headers,footers
FILELIST_ODT = ["content.xml", "styles.xml"]
# tag names for dom tree
ODT_PARAGRAPH = "text:p"    # paragraph node
ODT_TEXT_TAG = "#text"      # text node
ODT_SPACE_TAG = "text:s"    # space tag
# changes
ODT_DELETION_TAG = "text:deletion"
ODT_INSERTION_TAG = "text:insertion"
ODT_CHANGE_INFO_TAG = "office:change-info"
ODT_TRACKED_CHANGES_TAG = "text:tracked-changes"
ODT_CHANGED_REGION_TAG = "text:changed-region"
ODT_TEXT_ID_TAG = "text:id"
ODT_XML_ID_TAG = "xml:id"
ODT_AUTHOR_TAG = "dc:creator"
ODT_DATE_TAG = "dc:date"
ODT_OFFICE_TAG = "office:text"

odt_mode_selector = {
    "deletion" : ODT_DELETION_TAG,
    "insertion" : ODT_INSERTION_TAG
}


# longest common substring vars
Match=namedtuple('Match','a b size')
# text fitting
chars = ['.', ',', '-', ' ']

# construction
creator = \
    {
        'docx' : DocxHandler,
        'odt' : OdtHandler,
        'txt' : TxtHandler
    }

# supported file formats
VALID_EXTENSIONS = ["docx", "odt", "txt"]

DEFAULT_AUTHOR = "DocumentHandler"
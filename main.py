#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import docx
import zipfile
from xml.etree.cElementTree import XML

DOCX_NAMESPACE='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
DOCX_PARAGRAPH = DOCX_NAMESPACE + 'p'
DOCX_TEXT = DOCX_NAMESPACE + 't'

def readDocx():
    #open the .docx file as zip file 
    doc_file=zipfile.ZipFile('test.docx')
    #get the document.xml from the zip -> it contains the text
    document_xml=doc_file.read('word/document.xml')
    doc_file.close()
    print(document_xml)
    xml_content=XML(document_xml)
   
    
    for paragraph in xml_content.getiterator(DOCX_PARAGRAPH):
        for text in paragraph.getiterator(DOCX_TEXT):
            print (str(text.text))
    
   
    

readDocx()
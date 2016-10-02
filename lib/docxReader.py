#  -*- coding: utf-8 -*-

import zipfile
from xml.etree.cElementTree import XML

# for debug

class DocxReader:

    #namespaces
    DOCX_NAMESPACE='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    DOCX_PARAGRAPH = DOCX_NAMESPACE + 'p'
    DOCX_TEXT = DOCX_NAMESPACE + 't'


    def __init__(self,path):
        self.read(path)


    def read(self,path):
        #open the .docxHandler file as zip file
        doc_file=zipfile.ZipFile(path)
        #get the document.xml from the zip -> it contains the text
        document_xml=doc_file.read('word/document.xml')
        doc_file.close()
        self.xml_content=XML(document_xml)


    def print(self):
        for paragraph in self.xml_content.getiterator(self.DOCX_PARAGRAPH):
            print ("NEW PARAGRAPH from DocxReader")
            paragraph_string=""
            for text in paragraph.getiterator(self.DOCX_TEXT):
                paragraph_string+=text.text
            print (paragraph_string)

    
   
    


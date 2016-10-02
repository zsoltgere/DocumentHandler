#  -*- coding: utf-8 -*-

import docx
from lib import documentHandler

# docx handler class, based on python-docx

class DocxHandler(documentHandler.DocumentHandler):
    def __init__(self,path):
        self.document=docx.Document(path)

    def print(self):
        for p in self.document.paragraphs:
            print ("NEW PARAGPRAH from DocxHandler")
            print (p.text)


#  -*- coding: utf-8 -*-


from lib import docxHandler
from lib import docxReader

path="test.docx"

docx_self= docxReader.DocxReader(path)
docx_self.print()
docx= docxHandler.DocxHandler(path)
docx.print()
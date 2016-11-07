#  -*- coding: utf-8 -*-


from lib import docxHandler
from lib import odtHandler


# docx without paragraph and word splitting, except the auto generated pagebreak and Goback tags
docx_path="proba2.docx"
# docx sample
#docx_path="test.docx"

# lxml based docxhandler
'''
docx_lxml= docxHandler.DocxHandler(docx_path)

paras=docx_lxml.readall()

for ind in range(len(paras)):
    docx_lxml.para[ind]=paras[ind].replace('a','9')

docx_lxml.save_zip("test.docx")
'''

# docx without paragraph and word splitting, except the auto generated pagebreak and Goback tags
odt_path="proba2.odt"
# odt sample
#odt_path="test.odt"

# minidom
odt_minidom=odtHandler.OdtHandler(odt_path)

paras=odt_minidom.readall()

for ind in range(len(paras)):
    odt_minidom.para[ind]=paras[ind].replace('a','9')


odt_minidom.save_zip("test.odt")





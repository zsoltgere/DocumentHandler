#  -*- coding: utf-8 -*-


from lib.documentHandler import DocumentHandler
from lib.constantVariables import ExecutionMeter
from lib.basicHandler import Paragraph
# files without text splitting inside the paragrapsh
docx_path="proba2.docx"
odt_path="proba2.odt"
rtf_path="proba2.rtf"
txt_path="proba2.txt"


# paragraph test
import difflib

p=Paragraph()
a="baszki ez egy teszt, "
b="asd ami ha nem sikerül időben, "
c="akkor elbukom a tárgyat ahogy van"
fragments=[a,b,c]

for i in fragments:
    p.fragments.append(i)

#print (p.getParagraph())

new="ez egy próbálkozás, ami ha most nem sikerül azonnal, akkor elbukom ezt a tárgyat is mint a szar"

#print (new)
p.update(new)

#print (p.fragments)



'''
# DOCX example

docx_timer=ExecutionMeter()

docx_handler=DocumentHandler(docx_path)

docx_paras = docx_handler.readall()

for ind in range(len(docx_paras)):
    docx_handler.para[ind]=docx_paras[ind].replace('ipsum','anyád')
docx_handler.save("output")

print (docx_path,docx_timer.stop())
'''
'''
# ODT example

odt_timer=ExecutionMeter()


odt_handler=DocumentHandler(odt_path)

odt_paras = odt_handler.readall()

for ind in range(len(odt_paras)):
    odt_handler.para[ind]=odt_paras[ind].replace('a','9')

odt_handler.save("output")

print (odt_path,odt_timer.stop())



# TXT example

txt_timer=ExecutionMeter()


txt_handler=DocumentHandler(txt_path)

txt_paras = txt_handler.readall()

for ind in range(len(txt_paras)):
    txt_handler.para[ind]=txt_paras[ind].replace('a','9')

txt_handler.save("output")

print (txt_path,txt_timer.stop())

'''
'''
# not implemented yet

# RTF example

rtf_timer=ExecutionMeter()


rtf_handler=DocumentHandler(rtf_path)

rtf_paras = rtf_handler.readall()

for ind in range(len(rtf_paras)):
    rtf_handler.para[ind]=rtf_paras[ind].replace('a','9')

rtf_handler.save("output")

print (rtf_path,rtf_timer.stop())

'''
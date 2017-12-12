#  -*- coding: utf-8 -*-
from lib.documentHandler import DocumentHandler
from lib.constantVariables import ExecutionMeter

# files without text splitting inside the paragrapsh
docx_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\proba2.docx"
odt_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\proba2.odt"
txt_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\\minta.txt"

outputname="output"

output_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\outputs\\"

"""
spellchecker={
"bemutatésa":"bemutatása",
"Radcliff":"Ratcliff",
"SequeneMacther":"SequenceMatcher",
"összehasonlás":"összehasonlítás",
"ürres":"üres"
}
"""

spellchecker = {
    "lábjegyzet1111111111111111111111111111" : "lábjegyzet",
    "dasdasdasdasdasdasdlábjegyzet" : "lábjegyzet"
}

# DOCX example

docx_timer=ExecutionMeter()

docx_handler=DocumentHandler(docx_path)

docx_paras = docx_handler.readall()

ls=[]
for para in docx_paras:
    temp=para.split(' ')
    for i,word in enumerate(temp):
        if word in spellchecker:
            temp[i]=spellchecker[word]
    t=' '.join(temp)
    ls.append(t)

for i,j in enumerate(ls):
    docx_handler.para[i]=j
docx_handler.save(output_path,outputname)

print (docx_path,docx_timer.stop())

# ODT example

odt_timer=ExecutionMeter()

odt_handler=DocumentHandler(odt_path)

odt_paras = odt_handler.readall()

ls=[]
for para in odt_paras:
    temp=para.split(' ')
    for i,word in enumerate(temp):
        if word in spellchecker:
            temp[i]=spellchecker[word]
    t=' '.join(temp)
    ls.append(t)

for i,j in enumerate(ls):
    odt_handler.para[i]=j
odt_handler.save(output_path,outputname)

print (odt_path,odt_timer.stop())



# TXT example

txt_timer=ExecutionMeter()


txt_handler=DocumentHandler(txt_path)

txt_paras = txt_handler.readall()

for ind in range(len(txt_paras)):
    txt_handler.para[ind]=txt_handler.para[ind].replace('ODT','Open Document Format')
    txt_handler.para[ind]=txt_handler.para[ind].replace('DOCX','Office Open XML')

txt_handler.save(output_path,outputname)

print (txt_path,txt_timer.stop())
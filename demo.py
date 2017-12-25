#  -*- coding: utf-8 -*-

from lib.documentHandler import DocumentHandler
from lib.utils import ExecutionMeter
from lib.paragraph import Paragraph
from xml.dom import minidom
import time
from lib.odtHandler import OdtHandler

output_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\outputs\\"


param_set = 0
mode = -1
algorithm = 0

if param_set == 0:
    docx_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\proba2.docx"
    odt_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\proba2.odt"
    txt_path="d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\\minta.txt"

    outputname="output"

    spellchecker = {
        "lábjegyzet1111111111111111111111111111": "lábjegyzet",
        "dasdasdasdasdasdasdlábjegyzet": "lábjegyzet",
        "Lorem": "CSERÉLVE"
    }
elif param_set ==1:
    docx_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\minta.docx"
    odt_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\minta.odt"
    txt_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\\minta.txt"

    outputname = "minta"

    spellchecker = {
        "bemutatésa": "bemutatása",
        "Radcliff": "Ratcliff",
        "SequeneMacther": "SequenceMatcher",
        "összehasonlás": "összehasonlítás",
        "ürres": "üres"
    }
elif param_set == 2:
    odt_path = "d:\\Egyetem\szakd\\DocumentHandler\\test\inputs\korrektura.odt"
    outputname = "korrektura"
    spellchecker = {}

if algorithm == 0:
    algorithm_ = "dtw"
else:
    algorithm_ = "lcs"

if mode in [-1]:
    # DOCX example with context manager

    docx_timer=ExecutionMeter()

    with DocumentHandler(docx_path) as docx_handler:
        docx_paras = docx_handler.readall()
        modified_paragraphs = []
        for para in docx_paras:
            temp = para.split(' ')
            for i, word in enumerate(temp):
                if word in spellchecker:
                    temp[i] = spellchecker[word]
            t = ' '.join(temp)
            modified_paragraphs.append(t)
    docx_handler.save(output_path,outputname,modified_paragraphs,algorithm_)

    print (docx_path,docx_timer.stop())

if mode in [0,4]:
    par_1 = Paragraph()
    par_1.fragments.append("d ")                                #0
    par_1.fragments.append("")                                  #1
    par_1.fragments.append("Anita szeret a kutyájával, ")       #2
    par_1.fragments.append("")                                  #3
    par_1.fragments.append("Bé")                                #4
    par_1.fragments.append("lával ")                            #5
    par_1.fragments.append("szét")                              #6
    par_1.fragments.append("tördelt")                           #7
    par_1.fragments.append("szóóó ")                            #8
    par_1.fragments.append("minusze ")                          #9
    par_1.fragments.append("minusz a lovával a kertben játszani. ") #10
    par_1.fragments.append("")                                  #11
    par_1.fragments.append("próba")                             #12
    par_1.fragments.append("")                                  #13


    dtw_timer = ExecutionMeter()
    par_1.printfragments()
    par_1.update("h Márta szeret néha a macskájával Bélával széttördeltszóóó minuszegy a h egy kettő három négy öt. próba",algorithm_)
    par_1.printfragments()
    print (dtw_timer.stop())


if mode in [1,5]:

    # DOCX example

    docx_timer=ExecutionMeter()

    docx_handler=DocumentHandler(docx_path)

    docx_paras = docx_handler.readall()

    modified_paragraphs=[]
    for para in docx_paras:
        temp=para.split(' ')
        for i,word in enumerate(temp):
            if word in spellchecker:
                temp[i]=spellchecker[word]
        t=' '.join(temp)
        modified_paragraphs.append(t)

    docx_handler.save(output_path,outputname,modified_paragraphs,algorithm_)

    print (docx_path,docx_timer.stop())

if mode in [2,5]:
    # ODT example

    odt_timer=ExecutionMeter()

    odt_handler=DocumentHandler(odt_path)

    odt_paras = odt_handler.readall()

    modified_paragraphs=[]
    for para in odt_paras:
        temp=para.split(' ')
        for i,word in enumerate(temp):
            if word in spellchecker:
                temp[i]=spellchecker[word]
        t=' '.join(temp)
        modified_paragraphs.append(t)

    odt_handler.save(output_path,outputname,modified_paragraphs,algorithm_)

    print (odt_path,odt_timer.stop())

if mode in [3,5]:
    # TXT example

    txt_timer=ExecutionMeter()

    txt_handler=DocumentHandler(txt_path)

    txt_paras = txt_handler.readall()
    modified_paragraphs = []
    for ind in range(len(txt_paras)):
        txt_paras[ind] = txt_paras[ind].replace('ODT','Open Document Format')
        txt_paras[ind] = txt_paras[ind].replace('DOCX','Office Open XML')
        modified_paragraphs.append(txt_paras[ind])

    txt_handler.save(output_path,outputname,modified_paragraphs)

    print (txt_path,txt_timer.stop())

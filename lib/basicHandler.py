#  -*- coding: utf-8 -*-

# abstract class

from collections import OrderedDict
from copy import copy


class BasicHandler():
    # will declared in the child classes
    EXTENSION=""

    def __init__(self,path):
        # save path
        self.path=path
        # original paragraphs
        self.paragraph_list=[]
        # edited paragraphs
        self.para=[]
        self.xml_content=OrderedDict()

    # returns a list that contains all the paragraphs of the document
    def readall(self):
        # returns the copy of the paragraph list
        return copy(self.para)

    def buildParagraphList(self):
        pass

    def update(self,list=[]):
        pass

    def save(self,name):
        pass





# Paragraph class will represent a paragraph and separate the fragments as they are stored in the files
class Paragraph():

    def __init__(self):
        self.fragments=[]

    def replace(self,old,new):
        for fragment in self.fragments:
            fragment.replace(old,new)


    def getParagraph(self):
        paragraph=""

        for fragment in self.fragments:
            paragraph+=fragment

        return paragraph

    #class method, create a string list from the given list, if the list elements are Paragraphs
    def createParagraphList(list):
        temp=[]
        for paragraph in list:
            para = ""

            for fragment in paragraph.fragments:
                para += fragment

            temp.append(para)

        return temp
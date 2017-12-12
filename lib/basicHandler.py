#  -*- coding: utf-8 -*-


from collections import OrderedDict



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
        return self.para[:]

    def buildParagraphList(self):
        pass

    def update(self,list=[]):
        pass

    def save(self,name):
        pass
#  -*- coding: utf-8 -*-


# parent class
from lib.xmlBasedHandler import XmlBasedHandler
# constant variables
import lib.constantVariables
# paragraph
from lib.paragraph import Paragraph


# ordered dictionary to keep insertion order
from collections import OrderedDict



class DocxHandler(XmlBasedHandler):

    EXTENSION=".docx"

    # file path, parser (default is lxml)
    def __init__(self,path):
        super(DocxHandler,self).__init__(path,lib.constantVariables.FILELIST_DOCX)


    def buildParagraphList(self):

        # ordered dict in (range(x,y): filename) format, where x is the first and y-1 is the last paragraph that belongs to that file from self.paragrah_list
        self.paragraph_indexes=OrderedDict()

        for filename,file_content in self.xml_content.items():

            if len(self.paragraph_indexes) == 0:
                counter = 0
            else:
                # get the upper bound of the last key
                counter=list(self.paragraph_indexes.keys())[-1].stop

            par_counter=counter

            # paragraph level
            for paragraph in file_content.getElementsByTagName(lib.constantVariables.DOCX_PARAGRAPH):
                temp=Paragraph()

                # fragment level
                for fragments in paragraph.getElementsByTagName(lib.constantVariables.DOCX_SECTION):
                    # fragment inner level -> formatting and text nodes
                    for child in fragments.childNodes:
                        # if it's a text node
                        if child.nodeName== lib.constantVariables.DOCX_TEXT:
                            # get the text
                            temp.fragments.append(child.firstChild.nodeValue)
                self.paragraph_list.append(temp)
                par_counter+=1


            self.paragraph_indexes[range(counter, par_counter)] = filename

        self.para=Paragraph.createParagraphList(self.paragraph_list)




    def update(self,updated_text=[]):
        if not updated_text:
            updated_text=self.para

        if len(updated_text) != len(self.paragraph_list):
            raise ValueError ("Incorrect list length")
        else:

            par_counter=0

            while (par_counter < len(self.paragraph_list)):


                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(lib.constantVariables.DOCX_PARAGRAPH):
                    self.paragraph_list[par_counter].update(updated_text[par_counter])

                    fragment_counter = 0

                    for fragments in paragraph.getElementsByTagName(lib.constantVariables.DOCX_SECTION):

                        for child in fragments.childNodes:

                            if child.nodeName == lib.constantVariables.DOCX_TEXT:
                                #print  (updated_text[par_counter])
                                #print (self.paragraph_list [par_counter].fragments[fragment_counter])
                                child.firstChild.nodeValue = self.paragraph_list [par_counter].fragments[fragment_counter]
                                #print (child.firstChild.nodeValue)

                                fragment_counter+=1

                    par_counter+=1



    def update2(self,list=[]):
        if not list:
            list=self.para

        print (list)

        if len(list) != len(self.paragraph_list):
            raise ValueError ("Incorrect list length")
        else:
            par_counter=0

            while (par_counter < len(self.paragraph_list)):
                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(lib.constantVariables.DOCX_PARAGRAPH):
                    # implement the splitting function/algorithm to here
                    for fragments in paragraph.getElementsByTagName(lib.constantVariables.DOCX_SECTION):

                        for child in fragments.childNodes:
                            if child.nodeName == lib.constantVariables.DOCX_TEXT:
                                child.firstChild.nodeValue = list [par_counter]
                    par_counter+=1






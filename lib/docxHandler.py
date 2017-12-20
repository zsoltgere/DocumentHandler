#  -*- coding: utf-8 -*-

from lib.xmlBasedHandler import XmlBasedHandler
import lib.constantVariables
from lib.paragraph import Paragraph
from collections import OrderedDict



class DocxHandler(XmlBasedHandler):

    EXTENSION=".docx"

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




    def update(self,updated_text=[],mode = "dtw"):
        if not updated_text:
            updated_text=self.para

        if len(updated_text) != len(self.paragraph_list):
            raise ValueError ("Incorrect list length")
        else:

            par_counter=0

            while (par_counter < len(self.paragraph_list)):


                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(lib.constantVariables.DOCX_PARAGRAPH):
                    #self.paragraph_list[par_counter].printfragments()
                    self.paragraph_list[par_counter].update(updated_text[par_counter],mode)

                    fragment_counter = 0
                    #print("UPDATED_PARAGRAPH:", updated_text[par_counter])
                    for fragments in paragraph.getElementsByTagName(lib.constantVariables.DOCX_SECTION):

                        for child in fragments.childNodes:

                            if child.nodeName == lib.constantVariables.DOCX_TEXT:
                                #print ("UPDATED_FRAGMENT:",self.paragraph_list [par_counter].fragments[fragment_counter])
                                new = self.paragraph_list[par_counter].fragments[fragment_counter]
                                if child.firstChild.nodeValue:
                                    if child.firstChild.nodeValue[0] == " ":
                                        if new:
                                            if new[0] != " ":
                                                new = " " + new
                                child.firstChild.nodeValue = new
                                #print ("PRINTED_NODEVALUE: ",child.firstChild.nodeValue)

                                fragment_counter+=1

                    par_counter+=1
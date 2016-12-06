#  -*- coding: utf-8 -*-

# parent class
from lib.xmlBasedHandler import XmlBasedHandler
# constant variables
import lib.constantVariables
# paragraph
from lib.basicHandler import Paragraph


# ordered dictionary to keep insertion order
from collections import OrderedDict



class OdtHandler(XmlBasedHandler):

    EXTENSION=".odt"

    def __init__(self,path):
        super(OdtHandler,self).__init__(path,lib.constantVariables.FILELIST_ODT)



    def buildParagraphList(self):

        # ordered dict in (range(x,y): filename) format, where x is the first and y-1 is the last paragraph that belongs to that file from self.paragrah_list
        self.paragraph_indexes = OrderedDict()

        for filename,content in self.xml_content.items():

            if len(self.paragraph_indexes) == 0:
                counter = 0
            else:
                counter=list(self.paragraph_indexes.keys())[-1].stop

            par_counter=counter

            for paragraph in content.getElementsByTagName(lib.constantVariables.ODT_PARAGRAPH):

                temp=Paragraph()

                for node in paragraph.childNodes:

                    if node.nodeName == lib.constantVariables.ODT_TEXT_TAG:

                        temp.fragments.append(node.nodeValue)

                    for childnode in node.childNodes:

                        if childnode.nodeName == lib.constantVariables.ODT_TEXT_TAG:

                            temp.fragments.append(childnode.nodeValue)

                self.paragraph_list.append(temp)
                par_counter+=1

            self.paragraph_indexes[range(counter,par_counter)]=filename
        self.para=Paragraph.createParagraphList(self.paragraph_list)



    def update(self,updated_text=[]):
        if not updated_text:
            updated_text = self.para

        if len(updated_text) != len(self.paragraph_list):
            raise ValueError ("Incorrect list length")
        else:
            par_counter=0

            while (par_counter < len(self.paragraph_list)):


                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(lib.constantVariables.ODT_PARAGRAPH):

                    self.paragraph_list[par_counter].update(updated_text[par_counter])

                    fragment_counter = 0

                    for node in paragraph.childNodes:
                        if node.nodeName == lib.constantVariables.ODT_TEXT_TAG :

                            node.nodeValue=self.paragraph_list[par_counter].fragments[fragment_counter]
                            fragment_counter += 1

                        # span tag
                        for childnode in node.childNodes:
                            if childnode.nodeName == lib.constantVariables.ODT_TEXT_TAG:

                                childnode.nodeValue = self.paragraph_list[par_counter].fragments[fragment_counter]
                                fragment_counter+=1


                    par_counter+=1







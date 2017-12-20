#  -*- coding: utf-8 -*-

from lib.xmlBasedHandler import XmlBasedHandler
import lib.constantVariables
from lib.paragraph import Paragraph
from collections import OrderedDict
from xml.dom import minidom
from lib.utils import getTime

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

                    if node.nodeName == lib.constantVariables.ODT_SPACE_TAG:
                        if len(temp.fragments) > 0:
                            temp.fragments[len(temp.fragments)-1]+=" "

                    if node.nodeName == lib.constantVariables.ODT_TEXT_TAG:
                        temp.fragments.append(node.nodeValue)

                    for childnode in node.childNodes:
                        if childnode.nodeName == lib.constantVariables.ODT_SPACE_TAG:
                            if len(temp.fragments) > 0:
                                temp.fragments[len(temp.fragments) - 1] += " "

                        if childnode.nodeName == lib.constantVariables.ODT_TEXT_TAG:

                            temp.fragments.append(childnode.nodeValue)

                self.paragraph_list.append(temp)
                par_counter+=1

            self.paragraph_indexes[range(counter,par_counter)]=filename
        self.para=Paragraph.createParagraphList(self.paragraph_list)
    # further possibilities: made it recursive
    def update(self,updated_text=[],mode = "dtw"):
        if not updated_text:
            updated_text = self.para

        if len(updated_text) != len(self.paragraph_list):
            raise ValueError ("Incorrect list length")
        else:
            par_counter=0


            while (par_counter < len(self.paragraph_list)):
                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(lib.constantVariables.ODT_PARAGRAPH):

                    self.paragraph_list[par_counter].update(updated_text[par_counter],mode)
                    fragment_counter = 0
                    child = None
                    nodes = paragraph.childNodes

                    for index in range(len(nodes)):
                        # normal text tag
                        if nodes[index].nodeName == lib.constantVariables.ODT_TEXT_TAG :
                            nodes[index].nodeValue = self.paragraph_list[par_counter].fragments[fragment_counter]
                            fragment_counter += 1
                        if nodes[index].nodeName == lib.constantVariables.ODT_SPACE_TAG:
                            if index > 0:
                                if nodes[index-1].nodeValue and not child:
                                    if nodes[index-1].nodeValue[len(nodes[index-1].nodeValue)-1] == " ":
                                        nodes[index-1].nodeValue = nodes[index-1].nodeValue[:-1]
                                elif child and child.nodeValue: # space from previous node from lower level
                                    if child.nodeValue[len(child.nodeValue)-1] == " ":
                                        child.nodeValue = child.nodeValue[:-1]
                            child = None

                        # span tag
                        grandchild = None
                        childNodes = nodes[index].childNodes
                        for index2 in range(len(childNodes)):
                            if childNodes[index2].nodeName == lib.constantVariables.ODT_TEXT_TAG:
                                childNodes[index2].nodeValue = self.paragraph_list[par_counter].fragments[fragment_counter]
                                child = childNodes[index2]
                                fragment_counter += 1
                            if childNodes[index2].nodeName == lib.constantVariables.ODT_SPACE_TAG and index2 > 0:
                                if childNodes[index2-1].nodeValue and not grandchild:
                                    if childNodes[index2 - 1].nodeValue[len(childNodes[index2 - 1].nodeValue) - 1] == " ":
                                        childNodes[index2 - 1].nodeValue = childNodes[index2 - 1].nodeValue[:-1]
                                elif grandchild and grandchild.nodeValue:
                                    if grandchild.nodeValue[len(grandchild.nodeValue)-1] == " ":
                                        grandchild.nodeValue = grandchild.nodeValue[:-1]
                                grandchild = None

                    par_counter+=1

            for filename, file in self.xml_content.items():
                element = file.getElementsByTagName(lib.constantVariables.ODT_OFFICE_TAG)
                for elem in element:
                    childs = elem.childNodes
                    for child in childs:
                        if child.nodeName == lib.constantVariables.ODT_TRACKED_CHANGES_TAG:
                            newNode = OdtHandler.createTrackedChanges()
                            childNode = OdtHandler.createChangedRegionNode("deletion")
                            newNode.appendChild(childNode)
                            child.parentNode.replaceChild(newNode,child)

    # proof methods for additional function
    @staticmethod
    def createChangedRegionNode(type,name=None):
        if not name:
            name = lib.constantVariables.DEFAULT_AUTHOR
        # todo: xml:id , nodevalue, generate unique ID
        mode = lib.constantVariables.odt_mode_selector[type]
        id = "ct2243093767648"
        document = minidom.getDOMImplementation().createDocument(None, "Dummy", None)
        root = document.createElement(lib.constantVariables.ODT_CHANGED_REGION_TAG)
        root.setAttribute(lib.constantVariables.ODT_TEXT_ID_TAG, id)
        root.setAttribute(lib.constantVariables.ODT_XML_ID_TAG, id)
        t = document.createElement(mode)
        info = document.createElement(lib.constantVariables.ODT_CHANGE_INFO_TAG)
        creator = document.createElement(lib.constantVariables.ODT_AUTHOR_TAG)
        creator.nodeValue = name
        date = document.createElement(lib.constantVariables.ODT_DATE_TAG)
        date.nodeValue = getTime()
        info.appendChild(creator)
        info.appendChild(date)
        t.appendChild(info)
        root.appendChild(t)
        return root

    @staticmethod
    def createTrackedChanges():
        document = minidom.getDOMImplementation().createDocument(None, "Dummy", None)
        return document.createElement(lib.constantVariables.ODT_TRACKED_CHANGES_TAG)







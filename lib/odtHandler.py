#  -*- coding: utf-8 -*-

from lib.xmlBasedHandler import XmlBasedHandler
import zipfile
import xml.dom.minidom as MD
from collections import OrderedDict


class OdtHandler(XmlBasedHandler):

    EXTENSION=".odt"
    ODT_PARAGRAPH = "text:p"
    ODT_TEXT_TAG="#text"

    def __init__(self,path):
        super(OdtHandler,self).__init__(path)

        #open the .odt file as zip file
        self.zip_file=zipfile.ZipFile(path,'a')

        # information objects of the files inside the .odt file
        self.fileInfo = self.zip_file.infolist()

        self.relevant_file_namelist=["content.xml","styles.xml"]
        self.files=OrderedDict([(item,self.zip_file.read(item)) for item in self.relevant_file_namelist])

        self.parseXML()

    def parseXML(self):

        for filename, zipf in self.files.items():
            self.xml_content[filename] = MD.parseString(zipf)

        # get all the paragraphs
        self.buildParagraphList(self.xml_content)
        #debug info
        print ("readen files: "+str(len(self.xml_content)))

    def buildParagraphList(self,dict):

        # ordered dict in (range(x,y): filename) format, where x is the first and y-1 is the last paragraph that belongs to that file from self.paragrah_list
        self.paragraph_indexes = OrderedDict()

        for filename,content in self.xml_content.items():

            if len(self.paragraph_indexes) == 0:
                counter = 0
            else:
                counter=list(self.paragraph_indexes.keys())[-1].stop

            par_counter=counter

            for paragraph in content.getElementsByTagName(self.ODT_PARAGRAPH):
                #print (str(par_count)+" ELEMENT",paragraph)
                temp=""
                for node in paragraph.childNodes:
                    if node.nodeName == "#text":
                        #print ("\tchild: ",node.nodeValue)
                        temp+=node.nodeValue
                    for childnode in node.childNodes:
                        if childnode.nodeName == "#text":
                            #print ("\t\t\tGrandchild: ",childnode.nodeValue)
                            temp+=childnode.nodeValue

                #print ("\n"+temp+"\n")
                self.paragraph_list.append(temp)
                #print (str(len(self.paragraph_list)))
                par_counter+=1

            self.paragraph_indexes[range(counter,par_counter)]=filename
        self.para=self.paragraph_list

    def update(self,list=[]):
        if not list:
            list = self.para

        if len(list) != len(self.paragraph_list):
            print("Incorrect list length")
            # todo: exception!
        else:
            par_counter=0

            while (par_counter < len(self.paragraph_list)):

                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(self.ODT_PARAGRAPH):
                    # implement the splitting function/algorithm to here
                    splitted_counter = 0
                    for node in paragraph.childNodes:
                        if node.nodeName == self.ODT_TEXT_TAG :
                            if splitted_counter == 0:
                                node.nodeValue=list[par_counter]
                                splitted_counter+=1
                            else:
                                # todo
                                node.nodeValue="###########SPLITTED TEXT############TODO#############"
                        # span tag
                        for childnode in node.childNodes:
                            if childnode.nodeName == self.ODT_TEXT_TAG:
                                childnode.nodeValue = list[par_counter]
                    par_counter+=1

    def save_xml(self):
        for filename, content in self.xml_content.items():
            self.createXMLfile(filename, content.documentElement.toprettyxml(encoding="utf-8"))




    '''
    #### debug functions ####
    '''

    def print_xml_content(self,xml_file):
        par_c=0
        for paragraph in xml_file.iter(self.ODT_PARAGRAPH):
            print(str(par_c))
            for text in paragraph.iter():
                #print(text)
                #print(text.text)
                for x in text.iter("*"):
                    print (x)
                    print (x.text)

            par_c+=1




    '''
    #### obsolete functions ####
    '''



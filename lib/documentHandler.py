#  -*- coding: utf-8 -*-

# abstract class -> maybe this will useful somewhere

# file operations
import zipfile
import os
from shutil import move
from shutil import rmtree
from lxml import etree
import xml.dom.minidom as MD
from collections import OrderedDict
from copy import copy


class DocumentHandler:
    TEMP_DIR="temp"
    TEMP_DIR_PATH="temp/"

    def __init__(self,path,parser):

        # save path
        self.path=path
        # init
        self.parser=parser
        # original paragraphs
        self.paragraph_list=[]
        # edited paragraphs
        self.para=[]

    # todo: rename
    # parse the XML files with lxml.etree
    def readDocumentXML_lxml(self):

        self.xml_content=OrderedDict()

        # parse the xml files
        if self.parser==3:
            for filename,zipf in self.files.items():
                self.xml_content[filename]=etree.fromstring(zipf)
        else:
            for filename, zipf in self.files.items():
                self.xml_content[filename] = MD.parseString(zipf)

        # get all the paragraphs
        self.buildParagraphList(self.xml_content)
        #debug info
        print ("readen files: "+str(len(self.xml_content)))



    def createTemporaryDir(self):
        # create the temporary folder
        if not os.path.exists("temp"):
            os.makedirs("temp")

    def deleteTemporaryDir(self):
        # delete temporary folder
        rmtree("temp")

    def createXMLfile(self,path,content=""):
        # remove the old file
        os.remove(self.TEMP_DIR_PATH+path)
        # create the new file and fill it with the modified content
        with open(self.TEMP_DIR_PATH+path,"w",encoding="utf-8") as file:
            file.write(content.decode("utf-8"))

    def createZipFile(self,name):
        # create the new document file
        zip=zipfile.ZipFile(self.TEMP_DIR_PATH+name,'w')

        #build the new zip (docx) file
        for i in self.fileInfo:
            #path of the extracted file, path of file inside the docx file, compress_type
            zip.write(self.TEMP_DIR_PATH+i.filename,i.filename,8)

        zip.close()

        # move the new document file
        move(self.TEMP_DIR_PATH+name,str(self.parser)+name)


    def buildParagraphList(self,dict):
        pass

    # returns a list that contains all the paragraphs of the document
    def readall(self):
        # returns the copy of the paragraph list
        return copy(self.para)

    def update(self,list):
        pass

    #returns the filename that contains the "int". paragraph
    def getFilename(self,int):
        for key,value in self.paragraph_indexes.items():
            if int in key:
                return value


    def save_zip(self,name):

        self.update()

        self.createTemporaryDir()

        # extract the original docx file
        self.zip_file.extractall(self.TEMP_DIR_PATH)

        # write the new xml files
        for filename, content in self.xml_content.items():
            if self.parser == 3:
                self.createXMLfile(filename, etree.tostring(content, encoding="utf-8"))
            elif self.parser == 2:
                self.createXMLfile(filename,content.documentElement.toprettyxml(encoding="utf-8"))
        self.createZipFile(name)

        # close zip files
        self.zip_file.close()

        self.deleteTemporaryDir()



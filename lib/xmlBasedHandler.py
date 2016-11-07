#  -*- coding: utf-8 -*-


# file operations
import zipfile
import os
from shutil import move
from shutil import rmtree
from lib.basicHandler import BasicHandler


class XmlBasedHandler(BasicHandler):

    TEMP_DIR="temp"
    TEMP_DIR_PATH="temp/"

    def __init__(self,path):
        super(XmlBasedHandler,self).__init__(path)

    # parsing functions, will implemented in the child classes, because the odt and the docx will use different parsers
    def parseXML(self):
        pass


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


    def createZipFile(self,filename):
        name=filename+self.EXTENSION
        # create the new document file
        zip=zipfile.ZipFile(self.TEMP_DIR_PATH+name,'w')

        #build the new zip (docx) file
        for i in self.fileInfo:
            #path of the extracted file, path of file inside the docx file, compress_type
            zip.write(self.TEMP_DIR_PATH+i.filename,i.filename,8)

        zip.close()

        # move the new document file
        move(self.TEMP_DIR_PATH+name,name)

    #returns the filename that contains the "int". paragraph
    def getFilename(self,int):
        for key,value in self.paragraph_indexes.items():
            if int in key:
                return value


    def save(self,name):

        self.update()

        self.createTemporaryDir()

        # extract the original docx file
        self.zip_file.extractall(self.TEMP_DIR_PATH)

        # write the new xml files
        self.save_xml()

        self.createZipFile(name)

        # close zip files
        self.zip_file.close()

        self.deleteTemporaryDir()

    # will implemented in child classes
    def save_xml(self):
        pass



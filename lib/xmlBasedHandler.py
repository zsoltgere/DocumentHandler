#  -*- coding: utf-8 -*-

from lib.basicHandler import BasicHandler
import zipfile
import tempfile
from os import path
from shutil import move
import xml.dom.minidom as minidom
from collections import OrderedDict


class XmlBasedHandler(BasicHandler):


    def __init__(self,path,filelist):
        super(XmlBasedHandler,self).__init__(path)

        self.filelist=filelist

        self.openFiles()

        self.parseXML()


    # getting the .xml files from the zip archives and saving the other files into a temporary directory
    def openFiles(self):

        #open the odt/docx file as zip file
        # the mode parameter is 'r' because now only reading the file
        zip_file=zipfile.ZipFile(self.path,'r')
        # information objects of the files inside the .odt/.docx file
        self.nameList = zip_file.namelist()
        # ordered dictionary in (filename,file) structure
        self.files=OrderedDict()
        #iterate the files that contains text
        for filename in self.filelist:
            # if it's exist in the archive
            if filename in self.nameList:
                # create a new (filename,file) element
                self.files[filename]=zip_file.read(filename)

        #create temporary directory
        self.tempdirectory=tempfile.TemporaryDirectory()
        # extract all the files of the document to the temporary directory
        for i in self.nameList:
            if i not in self.filelist:
                zip_file.extract(path=self.tempdirectory.name,member=i)
        # close the zip file
        zip_file.close()

    # parsing functions, using minidom
    def parseXML(self):
        # parse every xml file
        for filename, zipf in self.files.items():
            self.xml_content[filename] = minidom.parseString(zipf)
        # get all the paragraphs
        self.buildParagraphList()
        # debug info to the console
        print(self.EXTENSION,"readen files:",str(len(self.xml_content)))

    # creating
    def createXMLfile(self):
        # iterate trough the files
        for filename, content in self.xml_content.items():
            try:
                # open an xml file in the temporary directory
                with open(path.join(self.tempdirectory.name,filename),"w",encoding="utf-8") as file:
                    file.write(content.documentElement.toxml(encoding="utf-8").decode("utf-8"))
            except IOError as e:
                print ('IOError')




    def createZipFile(self,fpath=None,fname=None):

        tmp = path.split(self.path)

        if fpath == None:
            fpath = tmp[0]

        if fname == None:
            fname = tmp[1]
        else:
            fname += self.EXTENSION

        #new zip container in the temporary directory
        zip=zipfile.ZipFile(path.join(self.tempdirectory.name,fname),'w')
        # fill the zip with the files
        for i in self.nameList:
            zip.write(path.join(self.tempdirectory.name,i),i,8)
        # close it
        zip.close()
        # move it
        #print ("SAVING TO...",path.join(fpath,fname))
        move(zip.filename,path.join(fpath,fname))
        # delete the temporary directory
        self.tempdirectory.cleanup()


    #returns the filename that contains the "index". paragraph
    def getFilename(self,index):
        for key,value in self.paragraph_indexes.items():
            if index in key:
                return value

    # saving
    def save(self,path=None,name=None):
        # update the text content with the changes
        self.update("dtw")
        # write the new xml files
        self.createXMLfile()
        # create the new zip container
        self.createZipFile(path,name)





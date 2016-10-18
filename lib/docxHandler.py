#  -*- coding: utf-8 -*-

# parsers
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
# file operations
import zipfile
import os
from shutil import move
from shutil import rmtree
# regular expression for debug function
import re
# abstract class
from lib.documentHandler import DocumentHandler


class DocxHandler(DocumentHandler):

    #namespaces for the xml parser
    DOCX_NAMESPACE='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    DOCX_PARAGRAPH = DOCX_NAMESPACE + 'p'
    DOCX_TEXT = DOCX_NAMESPACE + 't'


    def __init__(self,path,parser=1):

        # save path
        self.path=path

        # init
        self.parser=parser
        #open the .docxHandler file as zip file
        self.docx_file=zipfile.ZipFile(path,'a')
        self.document_xml=self.docx_file.read('word/document.xml')

        # choose parser
        if self.parser==1:
            self.readDocumentXML_MINIDOM()
        elif self.parser==2:
            self.readDocumentXML_ElementTree()

        self.print_xml_content()
        #save (temporary)
        self.save()

    # parse the XML file with xml.dom.minidom
    def readDocumentXML_MINIDOM(self):

        self.xml_content = MD.parseString(self.document_xml)

    # parse the XML file with xml.etree.ElementTree
    def readDocumentXML_ElementTree(self):

        # register namespaces
        # OK
        ET.register_namespace('mc',"http://schemas.openxmlformats.org/markup-compatibility/2006")
        ET.register_namespace('r',"http://schemas.openxmlformats.org/officeDocument/2006/relationships")
        ET.register_namespace('w',"http://schemas.openxmlformats.org/wordprocessingml/2006/main")

        # nem hasznalt??
        ET.register_namespace('m',"http://schemas.openxmlformats.org/officeDocument/2006/math")

        ET.register_namespace('wp',"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
        ET.register_namespace('wp14',"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing")

        ET.register_namespace('wpc',"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas")
        ET.register_namespace('wpg',"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup")
        ET.register_namespace('wpi',"http://schemas.microsoft.com/office/word/2010/wordprocessingInk")
        ET.register_namespace('wps',"http://schemas.microsoft.com/office/word/2010/wordprocessingShape")

        ET.register_namespace('wne',"http://schemas.microsoft.com/office/word/2006/wordml")
        ET.register_namespace('w14',"http://schemas.microsoft.com/office/word/2010/wordml")
        ET.register_namespace('w15',"http://schemas.microsoft.com/office/word/2012/wordml")

        ET.register_namespace('o',"urn:schemas-microsoft-com:office:office")
        ET.register_namespace('v',"urn:schemas-microsoft-com:vml")
        ET.register_namespace('w10',"urn:schemas-microsoft-com:office:word")


        self.xml_content = ET.fromstring(self.document_xml)

        # debug for namespaces
        # print(self.namespace(self.xml_content))




    def save(self):

        # create the temporary folder
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # create the new docx file
        newzip=zipfile.ZipFile('temp/test.docx','w')

        #extract the original docx file
        self.docx_file.extractall('temp/')

        #delete the old document.xml
        os.remove("temp/word/document.xml")

        # write the new document.xml file

        # mini DOM
        if self.parser==1:
            r_string = self.xml_content.toxml(encoding="utf-8")
        # element tree
        elif self.parser == 2:
            r_string = ET.tostring(self.xml_content,encoding="utf-8")






        # edit header
        #self.editHeader(r_string)

        with open("temp/word/document.xml", "w", encoding="utf-8") as f:
            f.write(r_string.decode("utf-8"))

        #information objects of the files inside the .docx file
        fileInfo =self.docx_file.infolist()

        #build the new zip (docx) file
        for i in fileInfo:
            #path of the extracted file, path of file inside the docx file, compress_type
            newzip.write("temp/"+i.filename,i.filename,8)

        #close zip files
        newzip.close()
        self.closeDocxZip()

        # move the new docx file
        move('temp/test.docx','test2.docx')

        # delete temporary folder
        rmtree("temp")


    def closeDocxZip(self):
        self.docx_file.close()

    #debug
    def print_xml_content(self):
        pattern = re.compile('[^a-zA-ZÍÁÉŐÚŰÓÜÖíéáűúőóüö]')
        if self.parser == 1:
            par=0
            for paragraph in self.xml_content.getElementsByTagName("w:p"):
                par_text=""
                par+=1
                sect=0
                section_list=paragraph.getElementsByTagName("w:t")
                #check the emptiness of the paragraph
                if section_list:
                    print("Paragraph: " + str(par))
                    for section in section_list:
                        sect+=1
                        word_list=section.firstChild.nodeValue.split()
                        for word in word_list:
                            #print (pattern.sub('',word))
                            print (word)
                        if section.hasAttribute("xml:space"):
                            print ("xml:space")
                        par_text+=section.firstChild.nodeValue
                #for i in par_text.split():
                #    print (i)

        elif self.parser == 2:
            for paragraph in self.xml_content.getiterator(self.DOCX_PARAGRAPH):
                for text in paragraph.iter(self.DOCX_TEXT):
                    print (text.text)

    # missing namespaces
    def editHeader(self,s):
        # obs
        '''
        DOCX_HEADER="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>"""
        DOCX_DOCUMENT_OPEN="""<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 wp14">"""
        DOCX_DOCUMENT_CLOSE="</w:document>"
        '''

        #for tag in self.xml_content.iter():
            #print (tag.tag)
        #body=self.xml_content.find(self.DOCX_NAMESPACE+"body")
        #rs= ET.tostring(body,encoding="utf-8")
        #print (rs.decode("utf-8"))

        #xmlfile=MD.parseString(self.document_xml)
        #print (xmlfile.toprettyxml(encoding="utf-8").decode("utf-8"))
        pass

    # debug to ElementTree namespaces
    def namespace(self, element):
        m = re.match('\{.*\}', element.tag)
        return m.group(0) if m else ''

    # working only with several files
    def spellchecker(self):

        for paragraph in self.xml_content.iter(self.DOCX_PARAGRAPH):
            case = 0
            for text in paragraph.iter():
                if text.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}proofErr" and \
                                text.attrib == {'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type': 'spellStart'}:
                    case = 1
                if case == 1 and text.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t":
                    print (text.text)
                    case = 0
                    text.text="######spellWarning#######"
                    print (text.text)
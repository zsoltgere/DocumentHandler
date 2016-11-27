#  -*- coding: utf-8 -*-

# parser

# file operations
import zipfile
# regular expression for debug function
import re
# abstract class
from lib.xmlBasedHandler import XmlBasedHandler
# ordered dictionary to keep insertion order
from collections import OrderedDict
from lib.basicHandler import Paragraph



class DocxHandler(XmlBasedHandler):

    EXTENSION=".docx"

    #tag names for the xml parser
    DOCX_PARAGRAPH="w:p"
    DOCX_SECTION="w:r"
    DOCX_TEXT="w:t"

    # path to document.xml in the docx file
    DOC_XML_PATH='word/document.xml'

    # file path, parser (default is lxml)
    def __init__(self,path):
        super(DocxHandler,self).__init__(path)

        #open the .docx file as zip file
        self.zip_file=zipfile.ZipFile(path, 'a')

        #information objects of the files inside the .docx file
        self.fileInfo =self.zip_file.infolist()
        self.all_file_namelist =self.zip_file.namelist()

        # collect the file names/paths that contains text
        self.relevant_file_namelist=[self.DOC_XML_PATH]
        self.relevant_file_namelist+=[item for item in self.all_file_namelist if re.search('header[0-9].xml', item)]
        self.relevant_file_namelist+=[item for item in self.all_file_namelist if re.search('footer[0-9].xml', item)]
        # open these files
        self.files=OrderedDict([(item,self.zip_file.read(item)) for item in self.relevant_file_namelist])

        # parse the xml files
        self.parseXML()


    def buildParagraphList(self):

        # ordered dict in (range(x,y): filename) format, where x is the first and y-1 is the last paragraph that belongs to that file from self.paragrah_list
        self.paragraph_indexes=OrderedDict()

        for filename,file_content in self.xml_content.items():


            if len(self.paragraph_indexes) == 0:
                counter = 0
            else:
                counter=list(self.paragraph_indexes.keys())[-1].stop

            par_counter=counter

            # paragraph level
            for paragraph in file_content.getElementsByTagName(self.DOCX_PARAGRAPH):
                temp=Paragraph()

                # fragment level
                for fragments in paragraph.getElementsByTagName(self.DOCX_SECTION):
                    # fragment inner level -> formatting and text nodes
                    for child in fragments.childNodes:
                        # if it's a text node
                        if child.nodeName== self.DOCX_TEXT:
                            # get the text
                            temp.fragments.append(child.firstChild.nodeValue)

                self.paragraph_list.append(temp)
                par_counter+=1


            self.paragraph_indexes[range(counter, par_counter)] = filename
        self.para=Paragraph.createParagraphList(self.paragraph_list)



    def update(self,list=[]):

        if not list:
            list=self.para


        if len(list) != len(self.paragraph_list):
            print ("Incorrect list length")
            # todo: exception!
        else:
            par_counter=0

            while (par_counter < len(self.paragraph_list)):
                for paragraph in self.xml_content[self.getFilename(par_counter)].getElementsByTagName(self.DOCX_PARAGRAPH):
                    # implement the splitting function/algorithm to here
                    for fragments in paragraph.getElementsByTagName(self.DOCX_SECTION):

                        for child in fragments.childNodes:
                            if child.nodeName == self.DOCX_TEXT:
                                child.nodeValue = list [par_counter]
                        par_counter+=1



    '''
    #### debug functions ####
    '''
    def print_paras(self):
        j=0
        for i in self.paragraph_list:
            print (str(j)+" . paragraph\n"+i.getParagraph())
            j += 1

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

        elif self.parser in [2,3]:
            for paragraph in self.xml_content.getiterator(self.DOCX_PARAGRAPH):
                for text in paragraph.iter(self.DOCX_TEXT):
                    print (text.text)




    '''
    #### below this, these aren't necessary (maybe obsolete) functions ####
    '''

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



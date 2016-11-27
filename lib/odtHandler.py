#  -*- coding: utf-8 -*-



from lib.xmlBasedHandler import XmlBasedHandler
import zipfile
from collections import OrderedDict
from lib.basicHandler import Paragraph



class OdtHandler(XmlBasedHandler):

    EXTENSION=".odt"
    ODT_PARAGRAPH ="text:p"
    ODT_TEXT_TAG="#text"

    def __init__(self,path):
        super(OdtHandler,self).__init__(path)

        #open the .odt file as zip file
        self.zip_file=zipfile.ZipFile(path,'a')

        # information objects of the files inside the .odt file
        self.fileInfo = self.zip_file.infolist()
        # files that contains text
        self.relevant_file_namelist=["content.xml","styles.xml"]
        # read these files
        self.files=OrderedDict([(item,self.zip_file.read(item)) for item in self.relevant_file_namelist])
        # parse
        self.parseXML()

    def buildParagraphList(self):

        # ordered dict in (range(x,y): filename) format, where x is the first and y-1 is the last paragraph that belongs to that file from self.paragrah_list
        self.paragraph_indexes = OrderedDict()

        for filename,content in self.xml_content.items():

            if len(self.paragraph_indexes) == 0:
                counter = 0
            else:
                counter=list(self.paragraph_indexes.keys())[-1].stop

            par_counter=counter

            for paragraph in content.getElementsByTagName(self.ODT_PARAGRAPH):

                temp=Paragraph()

                for node in paragraph.childNodes:

                    if node.nodeName == self.ODT_TEXT_TAG:

                        temp.fragments.append(node.nodeValue)

                    for childnode in node.childNodes:

                        if childnode.nodeName == self.ODT_TEXT_TAG:

                            temp.fragments.append(childnode.nodeValue)

                self.paragraph_list.append(temp)
                par_counter+=1

            self.paragraph_indexes[range(counter,par_counter)]=filename
        self.para=Paragraph.createParagraphList(self.paragraph_list)



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
                                node.nodeValue="###########SPLITTED TEXT (page-break)############TODO#############"
                        # span tag
                        splitted_counter2 = 0
                        for childnode in node.childNodes:
                            if childnode.nodeName == self.ODT_TEXT_TAG:
                                if splitted_counter == 0:
                                    childnode.nodeValue = list[par_counter]
                                    splitted_counter += 1
                                else:
                                    #todo
                                    childnode.nodeValue = "###########SPLITTED TEXT (SPAN)############TODO#############"

                    par_counter+=1




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



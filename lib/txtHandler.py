#  -*- coding: utf-8 -*-
from lib.xmlBasedHandler import XmlBasedHandler


class TxtHandler(XmlBasedHandler):

    EXTENSION=".txt"
    LINE = "\n"

    def __init__(self,path):
        super(TxtHandler,self).__init__(path)

        self.open_file()

    def open_file(self):

        with open(self.path,'r') as txt_file:

            for line in txt_file:

                self.paragraph_list.append(line)

        self.para=self.paragraph_list


    def update(self,list):

        if not list:
            return
        if len(list) != len(self.paragraph_list):
            print ("Incorrect list length")
            return

        self.para=list


    def save(self,name):
        with open(name+self.EXTENSION,'w') as file:
                file.writelines(self.para)

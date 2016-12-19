#  -*- coding: utf-8 -*-
from lib.basicHandler import Paragraph
from lib.basicHandler import BasicHandler


class TxtHandler(BasicHandler):

    EXTENSION=".txt"
    SEPARATOR = '\n'

    def __init__(self,path):
        super(TxtHandler,self).__init__(path)

        self.open_file()

    def open_file(self):
        with open(self.path,'r') as txt_file:

            temp_par = Paragraph()
            temp=""
            separator_line_counter=0

            for line in txt_file:
                #if a line equal to the separator
                if line == self.SEPARATOR:
                    #increment separator counter by 1
                    separator_line_counter+=1
                    # if the temp str is not empty (if it's empty that means the previous line was the end of a paragraph)
                    if temp != "":
                        # append the paragraph to the list
                        self.paragraph_list.append(temp_par)
                        # reset the temp -> end of the paragraph
                        temp=""
                        temp_par=Paragraph()

                    # if the current line is the second separator line in a row, it could be == 2 too
                    if separator_line_counter % 2 == 0:
                        # append the separator to the paragraph list
                        sep_par=Paragraph()
                        sep_par.fragments.append(self.SEPARATOR)
                        self.paragraph_list.append(sep_par)
                        # reset the counter
                        separator_line_counter=0
                        # reset the temp -> end of the paragraph
                        temp=""
                        temp_par = Paragraph()

                # if the line not equal to the separator
                else:
                    # append it to the temp
                    temp+=line
                    temp_par.fragments.append(line)
                    # reset the separator counter
                    separator_line_counter=0
            # after the last line, check there is no text in the temp
            if temp !="":
                # if there is, add it to the list
                self.paragraph_list.append(temp_par)

        self.para=Paragraph.createParagraphList(self.paragraph_list)

    def update(self,list=[]):

        if not list:
            return
        if len(list) != len(self.paragraph_list):
            print ("Incorrect list length")
            return

        self.para=list

    def save(self,fpath=None,name=None):
        from os import path

        tmp = path.split(self.path)

        if fpath == None:
            path = tmp[0]

        if name == None:
            name = tmp[1]
        else:
            name += self.EXTENSION


        with open(path.join(fpath,name),'w') as file:
            # store the number of paragraphs
            ln=len(self.para)
            # iterate through the paragraphs
            for i in range(ln):
                # write i. paragraph
                file.write(self.para[i])
                # if i is not the last paragraph
                if i != ln-1:
                    # write predefined separator line between two paragraphs
                    file.write(self.SEPARATOR)
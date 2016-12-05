#  -*- coding: utf-8 -*-


from collections import OrderedDict
from copy import copy
#
import difflib


class BasicHandler():
    # will declared in the child classes
    EXTENSION=""

    def __init__(self,path):
        # save path
        self.path=path
        # original paragraphs
        self.paragraph_list=[]
        # edited paragraphs
        self.para=[]
        self.xml_content=OrderedDict()

    # returns a list that contains all the paragraphs of the document
    def readall(self):
        # returns the copy of the paragraph list
        return copy(self.para)

    def buildParagraphList(self):
        pass

    def update(self,list=[]):
        pass

    def save(self,name):
        pass





# Paragraph class will represent a paragraph and separate the fragments as they are stored in the files
class Paragraph():

    def __init__(self):
        self.fragments=[]


    def replace(self,old,new):
        for i,fragment in enumerate(self.fragments):
            self.fragments[i]=fragment.replace(old,new)

    # getting matches  with optional printing
    def getMatches(self,new,old,printer=False):
        differ=difflib.SequenceMatcher(None,new,old)
        d=[item for item in differ.get_matching_blocks()  if item.size > 1]

        matches = OrderedDict()

        # debug printer function
        temp = ""
        space = 0

        for match_index, match in enumerate(d):

            if len(temp) == 0:
                 if match.a !=0:
                   space=match.a
            else:
                space=match.a-len(temp)

            if printer:
                print (match,"spaces to append:",space)

            for i in range(space):
                temp+=" "
            if match.size > 1:

                temp+=new[match.a:match.a + match.size]
                #matches.append(new[match.a:match.a + match.size])
                matches[new[match.a:match.a + match.size]]=match
            else:
                temp+=" "

        if printer:
            print("### New Paragraph ###")
            print(new)
            print("### matches (aligned to the new) ###")
            print(temp)
            print("### Old Paragraph ###")
            print(old)

        return matches

    def update(self,new):

        matches_dict = self.getMatches(new,self.getParagraph())
        matches = list (matches_dict.keys())

        skeleton=OrderedDict()
        for i in range(len(self.fragments)):
            skeleton[i]=[]

        remaining_matches=len(matches)
        remaining_fragments=len(self.fragments)
        last_match=0

        for m_index, match in enumerate(reversed(matches[:remaining_matches])):
            # copy it, because the future changes
            temp_match=match
            match_found=False

            while (not match_found):

                for f_index,fragment in enumerate(reversed(self.fragments[:remaining_fragments])):
                    # if found
                    found=fragment.rfind(temp_match)
                    #print ("searching",match,"in",f_index,"remainin fragments:",remaining_fragments)
                    if found  != -1:
                        print (temp_match,remaining_fragments-f_index-1)
                        skeleton[remaining_fragments-f_index-1].append(matches_dict[match])
                        # if match found in fragment, stop searching that match
                        match_found=True
                        break

                if match_found:
                    remaining_matches -= 1
                    #print (f_index,last_match,remaining_fragments,match)

                    # if the fragment was found in a new fragment (fragment without any match), decrease the length of the fragments to spare time
                    if f_index > last_match:
                        # the list is reversed so in order to get the normal index...
                        remaining_fragments=(f_index-len(self.fragments))*-1
                        last_match=f_index


                else:
                    # if match not found, that means the match is splitted in the file and need to shorten to find it's fragment
                    temp_match=temp_match[1::]



        for fragment_index,fragment in enumerate(self.fragments):

            if fragment_index == 0:
                begin=0
            else:
                prev=skeleton[fragment_index-1][-1]
                print ("prev",prev)
                begin=prev.a+prev.size+1

            if fragment_index == len(self.fragments)-1:
                end=len(new)
            else:
                next=skeleton[fragment_index+1][0]
                print ("next",next)
                end=next.a-1

            self.fragments[fragment_index]=new[begin:end]

        print (self.fragments)

    def getParagraph(self):
        paragraph=""

        for fragment in self.fragments:
            paragraph+=fragment

        return paragraph

    #class method, create a string list from the given list, if the list elements are Paragraphs
    def createParagraphList(list):
        temp=[]
        for paragraph in list:
            para = ""

            for fragment in paragraph.fragments:
                para += fragment

            temp.append(para)

        return temp
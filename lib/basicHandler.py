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
        print ("of",len(self.fragments))
        print ("old fragments",self.fragments)
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
                    if found  != -1:
                        skeleton[remaining_fragments-f_index-1].append(matches_dict[match])
                        match_found=True
                        break

                if match_found:
                    remaining_matches -= 1

                    # if the fragment was found in a new fragment (fragment without any match), decrease the length of the fragments to spare time
                    if f_index > last_match:
                        # the list is reversed so in order to get the normal index...
                        remaining_fragments=(f_index-len(self.fragments))*-1
                        last_match=f_index


                else:
                    # if match not found, that means the match is splitted in the file and need to shorten to find it's fragment
                    temp_match=temp_match[1::]

        print ("matches",matches)
        print ("mat:",skeleton)
        align=0
        for fragment_index,fragment in enumerate(self.fragments):

            if fragment != "" and skeleton[fragment_index]:

                aligned_fragment_index=fragment_index-align

                if aligned_fragment_index != 0:

                    prev = current

                next = None
                if fragment_index != len(self.fragments)-1:
                    for i in range (fragment_index+1,len(self.fragments)):
                        if skeleton[i]:
                            next=skeleton[i]
                            break



                current = skeleton[fragment_index]


                if aligned_fragment_index == 0:
                    #print("fragments:",len(self.fragments))

                    #print ("first case",fragment_index)
                    begin=0

                    # optimal end -> aligned_index: 1

                    if next:
                        n=next[-1].a
                        end = self.getOptimalIndex(new, current[0].a + current[0].size, n)
                    else:
                        end=len(new)


                elif fragment_index == len(self.fragments)-1:
                    #print ("last case")
                    #optimal begin -> aligned_index: len-2
                    begin = self.getOptimalIndex(new,prev[0].a+prev[0].size,current[0].a)
                    end=len(new)
                else:

                    #print ("inner case",fragment_index)
                    # optimal shit part 1 comes to here
                    begin = self.getOptimalIndex(new,prev[0].a+prev[0].size,current[0].a)
                    #print ("prev",prev)
                    #print ("current",current)
                    #print ("next",next)
                    # optimal shit part 2 comes to here
                    if next:
                        n=next[-1].a
                    else:
                        n=len(new)

                    end=self.getOptimalIndex(new,current[0].a+current[0].size,n)

                #print ("begin",begin)
                #print ("end",end)

                if len(self.fragments) > 1 and aligned_fragment_index > 0 and begin == 0 and end == len(new):
                    print ("ops, we lost a fragment",begin,end)
                    self.fragments[fragment_index]=""
                else:
                    self.fragments[fragment_index]=new[begin:end]


                if end == len(new):
                    break
            else:
                align+=1
                self.fragments[fragment_index]=""

        print ("new fragments",self.fragments)

    def getOptimalIndex(self,new,begin,end):

        chars=['.',',','-',' ']

        slice=new[begin:end]

        for char in chars:
            index = slice.find(char)
            if index != -1:
                index+=begin
                print(char, index)

                if char == '-':
                    if index > begin:
                        return index-1
                else:
                    if index < end:
                        return index+1
                return index

        return int(len(slice)/2)+begin



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
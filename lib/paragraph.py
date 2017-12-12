from copy import copy
import lib.constantVariables
import difflib
from collections import OrderedDict


# Paragraph class will represent a paragraph and separate the fragments as they are stored in the files
class Paragraph():

    def __init__(self):
        self.fragments=[]

    def printfragments(self,info):
        print (info)
        for index,value in enumerate(self.fragments):
            print (index,value)
        print("\n")

    def replace(self,old,new):
        for i,fragment in enumerate(self.fragments):
            self.fragments[i]=fragment.replace(old,new)

    # getting matches  with optional printing
    def getMatches(self,new,old,printer=False):
        differ=difflib.SequenceMatcher(None,new,old)
        d=[item for item in differ.get_matching_blocks()] # if item.size > 1

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
            #debug
            if printer:
                print (match,"spaces to append:",space)

            for i in range(space):
                temp+=" "
            if match.size: #> 1:

                temp+=new[match.a:match.a + match.size]
                matches[new[match.a:match.a + match.size]]=match
            # unused now
            else:
                temp+=" "

        #debug
        if printer:
            print("### Old Paragraph ###")
            print(old)
            print("### New Paragraph ###")
            print(new)
            print("### matches (aligned to the new) ###")
            print(temp)
            print (matches)

        return matches

    def optimalize(self,matches_dict):

        matches = list (matches_dict.keys())
        #print (matches)
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

                for f_index, fragment in enumerate(reversed(self.fragments[:remaining_fragments])):
                    # if found
                    found = fragment.rfind(temp_match)
                    if found != -1:
                        skeleton[remaining_fragments - f_index - 1].append(matches_dict[match])
                        match_found = True
                        break

                if match_found:
                    remaining_matches -= 1

                    # if the fragment was found in a new fragment (fragment without any match), decrease the length of the fragments to spare time
                    if f_index > last_match:
                        # the list is reversed so in order to get the normal index...
                        remaining_fragments = (f_index - len(self.fragments)) * -1
                        last_match = f_index

                # if match not found in any fragments, it's in more than one,
                else:

                    all_found=False
                    f_one= False
                    # copy match
                    y=temp_match
                    # match initial paramteres
                    a=0
                    b=0
                    size=0
                    s=0

                    while not all_found:

                        if not f_one:
                            y=y[1::]
                            #print (y)

                        else:
                            f_one=False

                        for f_ind, frag in enumerate(self.fragments):
                            f = frag.rfind(y)
                            if f != -1:
                                #print ("FOUND",y)
                                # avoid to short after match
                                f_one=True
                                # set Match parameters
                                size=len(y)
                                s += size
                                a=matches_dict[match].a + matches_dict[match].size - s
                                # create Match
                                m=lib.constantVariables.Match(a,b,size)
                                # append
                                skeleton[f_ind].append(m)
                                #print ("ASDAS",m)
                                # slice the match
                                y=temp_match[0:len(temp_match)-s]
                                #print (y)
                                # remaining_fragments beállítása


                                # break for loop
                                break
                        # check the length of the match
                        if len(y) == 0:
                            all_found=True

                    # if all parts of the match found, delete the match from the dictionary
                    matches_dict.pop(match)
                    # break the while loop
                    match_found=True


        return skeleton

    def update(self,new):

        matches_dict = self.getMatches(new,self.getParagraph())

        skeleton=self.optimalize(matches_dict)

        for i,v in skeleton.items():
            for j,e in enumerate(v):
                if e.size == 1 and new[e.a] == ' ':
                    skeleton[i].remove(e)
        #print ("SKELETON",skeleton)


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

                    begin=0
                    # optimal end -> aligned_index: 1
                    if next:
                        n=next[-1].a
                        end = self.getOptimalIndex(new, current[0].a + current[0].size, n)
                    else:
                        end=len(new)

                elif fragment_index == len(self.fragments)-1:

                    #optimal begin -> aligned_index: len-2

                    begin = self.getOptimalIndex(new,prev[0].a+prev[0].size,current[0].a)
                    end=len(new)
                else:


                    begin = self.getOptimalIndex(new,prev[0].a+prev[0].size,current[0].a)


                    if next:
                        n=next[-1].a
                    else:
                        n=len(new)

                    end=self.getOptimalIndex(new,current[0].a+current[0].size,n)



                if len(self.fragments) > 1 and aligned_fragment_index > 0 and begin == 0 and end == len(new):
                    print ("ops, we lost a fragment",begin,end) # only debug info
                    self.fragments[fragment_index]=""
                else:
                    """
                    print (self.fragments)
                    print (new)
                    print ("ÚJ",begin,end)
                    print ("ÚJ",new[begin:end])
                    """
                    self.fragments[fragment_index]=new[begin:end]

                if end == len(new):
                    break
            else:
                align+=1
                self.fragments[fragment_index]=""


    def getOptimalIndex(self,new,begin,end):

        slice=new[begin:end]

        for char in lib.constantVariables.chars:
            index = slice.find(char)
            if index != -1:
                index+=begin

                if char == '-':
                    if index > begin:
                        return index-1
                else:
                    if index < end:
                        return index+1
                return index
        '''
        if len(slice)/2 == 0.5:
            a=1
        else:
            a=int(len(slice)/2)
        '''
        return begin



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
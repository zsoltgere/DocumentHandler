#  -*- coding: utf-8 -*-

import lib.constantVariables
import difflib
from collections import OrderedDict
from lib.utils import Utils
import numpy


# Paragraph class will represent a paragraph and separate the fragments as they are stored in the files
class Paragraph():



    def __init__(self):
        self.fragments=[]
        self.freq = []

        self.UPDATE_MODES = {
            "lcs": self.updateWithLongestCommonSubstring,
            "dtw": self.updateWithDynamicTimeWarping
        }

    def printfragments(self):
        print("\n")
        for index,value in enumerate(self.fragments):
            print (index,value)
        if not len(self.fragments):
            print ("EMPTY PARAGRAPH")
        print("\n")

    def replace(self,old,new):
        for i,fragment in enumerate(self.fragments):
            self.fragments[i]=fragment.replace(old,new)

    def getParagraph(self):
        paragraph = ""
        for fragment in self.fragments:
            paragraph += fragment
        return paragraph

    def eraseFragments(self):
        self.fragments = [""] * len(self.fragments)

    # class method, create a string list from the given list, if the list elements are Paragraphs
    def createParagraphList(list):
        temp = []
        for paragraph in list:
            para = ""
            for fragment in paragraph.fragments:
                para += fragment
            temp.append(para)
        return temp

    def update(self, new_paragraph, mode = "dtw"):
        self.UPDATE_MODES[mode](new_paragraph)

    # Dynamic Time Warping based update functions functions
    def updateWithDynamicTimeWarping(self, new_paragraph):

        old_paragraph = self.getParagraph()
        if old_paragraph != new_paragraph:      # it's the same? -> if yes, do nothing
            if self.fragments == 0:             # safety check to avoid error
                print("Warning! Into empty paragraphs, inserting is not available.")
            elif not len(new_paragraph):        # empty input, all fragment must erased
                self.eraseFragments()
            elif len(self.fragments) == 1:      # if there is only one fragment, there are no problem (optimal case)
                self.fragments[0] = new_paragraph
            else:                               # more than one fragment, so this is where the fun begins

                old_paragraph = self.createSplitableParagraph()
                old_list = old_paragraph.split(" ")             # init arrays
                new_list = new_paragraph.split(" ")
                distance_matrix = Utils.dtw(new_list,old_list)  # run dtw, based on edit distance algorithm(Levenshtein)
                self.calculateWordFreqs()

                new_fragments = [""] * len(self.fragments)

                depth_limit = 0  # limit to spare time and avoid fake matches from the repeating words
                actual_fragment = 0  # store the actual fragment's index for further use
                last_assigned_from_old = -1  # pointer to store which old word was handled at the last match

                for col_index in range(len(distance_matrix[0])):  # col_index ->  old words
                    for row_index in range(depth_limit,len(distance_matrix)):  #row_index -> new words

                        if distance_matrix[row_index,col_index] == 0:   # if the Levenshtein dist is 0, it's the same word

                            actual_fragment = self.getFragmentID(col_index)  # get the original place of the matched word
                            self.alignAddedWords(new_fragments, new_list, old_list, actual_fragment,
                                                 last_assigned_from_old, col_index, depth_limit, row_index) # add the words from the new before the match

                            new_fragments[actual_fragment] += old_list[col_index] + " " # add the match

                            last_assigned_from_old = col_index
                            depth_limit = row_index + 1 # set new limit -> under this the matrix can contain "fake" matches (they're coming from the repeating words)
                            break

                self.alignAddedWords(new_fragments, new_list, old_list, actual_fragment,
                                     last_assigned_from_old, col_index, depth_limit, len(new_list))  #add the remaining words

                self.removeUnwantedSpaces(new_fragments)
                self.fragments = new_fragments

    # mode -> where it comes from?  right: True, -> append to the end of the fragment
    #                               left: False ->  insert it to the beginning
    def recursiveLevenshtein (self, mode, new_fragments,words_to_substitute_in_new, old_list,
                              start_after, end_before):

        if not words_to_substitute_in_new:
            return

        words_to_substitute_in_old = old_list[start_after+1:end_before]
        if words_to_substitute_in_old:

            distance_matrix = Utils.dtw(words_to_substitute_in_new, words_to_substitute_in_old)
            index = self.findMostSimilarWordIndex(distance_matrix, words_to_substitute_in_new, words_to_substitute_in_old)
            index_to_append = start_after+1+index[1]
            fragment_to_append = self.getFragmentID(index_to_append)

            if index[0] != 0: # there are at least one word left from this
                left = words_to_substitute_in_new[:index[0]]
                self.recursiveLevenshtein(False, new_fragments, left, old_list, start_after, index_to_append)

            if mode:
                new_fragments[fragment_to_append] += words_to_substitute_in_new[index[0]] + " "
            else:
                new_fragments[fragment_to_append] = words_to_substitute_in_new[index[0]] + " " + new_fragments[fragment_to_append]

            if len(words_to_substitute_in_new)-1 > index[0]: # there are at least one word right from this
                right = words_to_substitute_in_new[index[0]+1:]
                self.recursiveLevenshtein(True, new_fragments, right, old_list, index_to_append, end_before)

        else: # add the remaining new words
            fragment_to_append = self.getFragmentID(start_after+1)
            for word in words_to_substitute_in_new:
                new_fragments[fragment_to_append] += word + " "

    def alignAddedWords(self, new_fragments,new_list, old_list, actual_fragment,
                        last_assigned_from_old, actual_match_index_in_old,
                        last_assigned_form_new, actual_match_index_in_new):

        words_to_align = []     # getting the words which need to be aligned
        for i in range(last_assigned_form_new,actual_match_index_in_new):
            words_to_align.append(new_list[i])

        if not words_to_align: # if it's empty, do nothing
            return  #1

        #2
        last_edited_fragment = self.getFragmentID(last_assigned_from_old)
        actual_is_the_last_not_empty = not self.checkNextFragments(actual_fragment)

        if (actual_fragment == last_edited_fragment or actual_match_index_in_new == len(new_list)) and actual_is_the_last_not_empty:
            for word in words_to_align:
                if word:
                    new_fragments[actual_fragment] += word + " "
            return

        start_after = last_assigned_from_old
        end_before = actual_match_index_in_old

        #       2.1 -> first block is only from the new sequence, split check not needed
        if last_assigned_from_old == -1:
            storage = words_to_align
            self.recursiveLevenshtein(True,new_fragments,storage,old_list,start_after, end_before)
            return

        split_words = self.getSplittedWords(last_assigned_from_old+1,actual_match_index_in_old,old_list)
        storage = []

        for word_to_align in words_to_align:
            index = -1
            for i, v in enumerate(split_words):
                if v[0] == word_to_align:
                    index = i
                    break

            if split_words and index != -1: # handle split words
                end_before = split_words[index][2][0]

                if storage:
                    self.recursiveLevenshtein(True, new_fragments, storage, old_list, start_after, end_before)

                split_word = split_words[index]
                for i in range(len(split_word[2])):
                    new_fragments[split_word[1].start+i] += old_list[split_word[2][i]]

                start_after = split_word[2][len(split_word[2])-1]
                new_fragments[split_word[1].start + i] += " "
                storage = []
                del split_words[index]
            else:
                end_before = actual_match_index_in_old
                storage.append(word_to_align)
        if storage:
            self.recursiveLevenshtein(True, new_fragments, storage, old_list, start_after, end_before)

    def calculateWordFreqs(self):
        freqs = [0] * len(self.fragments)
        for i in range(len(self.fragments)):
            str = self.fragments[i]
            if str:
                if str[-1] == " ":
                    str = str[:-1]
                freqs[i] += len(str.split(" "))
            if i > 0:
                freqs[i] += freqs[i-1]
        self.freq = freqs

    def getFragmentID(self, index):
        for i in range(len(self.freq)):
            if index < self.freq[i]:
                return i
        return len(self.freq)-1

    def checkNextFragments(self,index):
        for i in range(index+1,len(self.fragments)):
            if self.fragments[i]:
                return True     # there is at least one more valid fragment
        return False            # there is no more valid fragment in the list

    def createSplitableParagraph(self):
        ret = ""
        self.whitespaces = [False] * len(self.fragments)
        for i in range(len(self.fragments)):
            if self.fragments[i]:
                if self.fragments[i][-1] != " ":
                    ret += self.fragments[i] + " "
                else:
                    self.whitespaces[i] = True
                    ret += self.fragments[i]
        if ret[-1] == " ":
            ret = ret[:-1]
        return ret

    def removeUnwantedSpaces(self,new_fragments):
        for i in range(len(new_fragments)):
            if not self.whitespaces[i] and new_fragments[i]:
                if new_fragments[i][-1] == " ":
                    new_fragments[i] = new_fragments[i][:-1]
            elif self.whitespaces[i]:
                if not new_fragments[i]:
                    print(new_fragments[i])
                    new_fragments[i] = " "
                else:
                    if new_fragments[i][-1] != " ":
                        new_fragments[i] += " "

    def getSplittedWords(self,word_1,word_2,old_list):
        word_1_fragment = self.getFragmentID(word_1)
        word_2_fragment = self.getFragmentID(word_2-1)

        if word_1_fragment == word_2_fragment:
            return []

        splitted_words = []
        tmp = () # left: word right: range(x,y), where: x is the first y-1 is the last fragment where the word's parts are
        for i in range(word_1_fragment, word_2_fragment+1):
            if not self.whitespaces[i] and self.fragments[i]:
                if not tmp:
                    tmp = (old_list[self.freq[i]-1],range(i,i+1),[self.freq[i]-1])
                else:
                    ls = tmp[2]
                    ls.append(self.freq[i]-1)
                    tmp = (tmp[0] + old_list[self.freq[i]-1],range(tmp[1].start,i+1),ls)
                j = i
            else:
                if tmp:
                    ls = tmp[2]
                    ls.append(self.freq[j])
                    tmp = (tmp[0] + old_list[self.freq[j]],range(tmp[1].start,tmp[1].stop+1),ls)
                    splitted_words.append(tmp)
                tmp = ()
        return splitted_words

    def findMostSimilarWordIndex(self,matrix,new,old):
        dict = {}
        for (x,y) in numpy.ndenumerate(matrix):
            if y in dict:
                dict[y].append(x)
            else:
                dict[y] = [x]
        closest_ones = dict[min(dict)]
        dist = numpy.inf
        ret = (0,0)
        for index in closest_ones:
            tmp = numpy.abs(len(new[index[0]])-len(old[index[1]]))
            if tmp < dist:
                dist = tmp
                ret = index
        return ret

    # longest common substring algorithm based update functions
    def updateWithLongestCommonSubstring(self,new):
        matches_dict = self.getMatches(new,self.getParagraph())
        skeleton = self.optimalize(matches_dict)

        for i,v in skeleton.items():
            for j,e in enumerate(v):
                if e.size == 1 and new[e.a] == ' ':
                    skeleton[i].remove(e)

        align = 0
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
                    print ("Warning, we lost a fragment", begin, end)
                    self.fragments[fragment_index]=""
                else:
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
        return begin

    # getting matches  with optional printing
    def getMatches(self, new, old, printer=False):
        differ = difflib.SequenceMatcher(None, new, old)
        d = [item for item in differ.get_matching_blocks()]  # if item.size > 1

        matches = OrderedDict()

        # debug printer function
        temp = ""
        space = 0

        for match_index, match in enumerate(d):

            if len(temp) == 0:
                if match.a != 0:
                    space = match.a
            else:
                space = match.a - len(temp)
            # debug
            if printer:
                print(match, "spaces to append:", space)

            for i in range(space):
                temp += " "
            if match.size:  # > 1:

                temp += new[match.a:match.a + match.size]
                matches[new[match.a:match.a + match.size]] = match
            # unused now
            else:
                temp += " "

        # debug
        if printer:
            print("### Old Paragraph ###")
            print(old)
            print("### New Paragraph ###")
            print(new)
            print("### matches (aligned to the new) ###")
            print(temp)
            print(matches)

        return matches

    def optimalize(self, matches_dict):
        matches = list(matches_dict.keys())
        skeleton = OrderedDict()

        for i in range(len(self.fragments)):
            skeleton[i] = []

        remaining_matches = len(matches)
        remaining_fragments = len(self.fragments)
        last_match = 0

        for m_index, match in enumerate(reversed(matches[:remaining_matches])):
            # copy it, because the future changes
            temp_match = match
            match_found = False

            while not match_found:

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

                else:  # if match not found in any fragments, it's in more than one,

                    all_found = False
                    f_one = False
                    # copy match
                    y = temp_match
                    # match initial paramteres
                    a = 0
                    b = 0
                    size = 0
                    s = 0

                    while not all_found:
                        if not f_one:
                            y = y[1::]
                        else:
                            f_one = False

                        for f_ind, frag in enumerate(self.fragments):
                            f = frag.rfind(y)
                            if f != -1:
                                f_one = True
                                # set Match parameters
                                size = len(y)
                                s += size
                                a = matches_dict[match].a + matches_dict[match].size - s
                                m = lib.constantVariables.Match(a, b, size)  # create Match
                                skeleton[f_ind].append(m)
                                y = temp_match[0:len(temp_match) - s]  # slice the match
                                break

                        if len(y) == 0: # check the length of the match
                            all_found = True

                    matches_dict.pop(match)  # if all parts of the match found, delete the match from the dictionary
                    match_found = True  # break the while loop

        return skeleton
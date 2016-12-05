#  -*- coding: utf-8 -*-
from lib.xmlBasedHandler import XmlBasedHandler


# this will be implemented in the future
class RtfHandler(XmlBasedHandler):

    EXTENSION=".rtf"

    def __init__(self,path):
        super(RtfHandler,self).__init__(path)

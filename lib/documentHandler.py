#  -*- coding: utf-8 -*-

from lib.docxHandler import DocxHandler
from lib.odtHandler import OdtHandler
from lib.txtHandler import TxtHandler
from lib.rtfHandler import RtfHandler

#the user will create this class
class DocumentHandler:

    VALID_EXTENSIONS=["docx","odt","rtf","txt"]

    def __init__(self):
        pass

    def __new__(self,path):
        pathls = path.split(".")

        if not path or "." not in path or len(pathls) > 2:
            # todo exception
            print ("Path format is invalid! ",path)
        elif pathls[1].lower() not in self.VALID_EXTENSIONS:
            # todo exception
            print ("The given file extension is not supported. ","The valid extensions are: ",self.VALID_EXTENSIONS)
        else:
            extension=pathls[1].lower()

            if extension == "docx":
                return DocxHandler(path)
            elif extension == "odt":
                return OdtHandler(path)
            elif extension == "rtf":
                return RtfHandler(path)
            elif extension == "txt":
                return TxtHandler(path)







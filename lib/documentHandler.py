#  -*- coding: utf-8 -*-

# import the handlers
from lib.docxHandler import DocxHandler
from lib.odtHandler import OdtHandler
from lib.txtHandler import TxtHandler
from lib.rtfHandler import RtfHandler
# import the costum exception class
from lib.constantVariables import MyError
# constant variables
import lib.constantVariables as constantVariables

#the user will create this class
class DocumentHandler:


    def __init__(self):
        pass

    def __new__(self,path):
        # split the path by the dot, so the last element of the list will be extension of the file
        pathls = path.split(".")

        # if the path is an empty string or there are no or more then one (if there is more than one dot, there will be more then two element in the list) dot in it
        if not path or "." not in path or len(pathls) > 2:

            raise MyError("Path format is invalid! "+path)

        else:
            # get the extension
            extension=pathls[1].lower()
            # if it's not valid or not supported
            if extension not in constantVariables.VALID_EXTENSIONS:

                raise MyError ("The given file extension "+pathls[1].lower()+" is not supported. "+"The valid extensions are: "+str(constantVariables.VALID_EXTENSIONS))

            else:
                # return the suitable handler object
                if extension == "docx":
                    return DocxHandler(path)
                elif extension == "odt":
                    return OdtHandler(path)
                elif extension == "rtf":
                    return RtfHandler(path)
                elif extension == "txt":
                    return TxtHandler(path)






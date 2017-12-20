DocumentHandler
=======

DocumentHandler is written in Python 3.4 to provide access to the text content of the supported document formats directly, and after manipulations the program is able to insert back the changed text into the original document file. There are no dependencies ,only the modules of the Python 3.4 Standard Library are used.

During the insertion of the text, the aligning of the new content between the fragments inside a paragraph can be done based on two method. The default is the Dynamic Time Warping (to use this, call te update and save function with mode = "dtw" set). The other method is based on the Longest Common Substring Algorithm and to use, set the mode parameter to "lcs".
The currently supported document formats:  docx, odt, txt.

Documentation
-----------

DocumentHandler
=======

"dtw" = Dynamic Time Warping
"lcs" = Longest Common Substring

DocumentHandler.DocumentHandler(path)
------------
Providing the interface for the program.

path: full path of the document (must including the name and the extension of the file too).

DocumentHandler.para
----

List, that contains all the text from the document. Each element represents one paragraph of the document in string.

DocumentHandler.readall() -> List:
----

Returns the copy of para.

DocumentHandler.save(path=None, filename=None, mode = "dtw")
----

Saving the the document to the given path on the given name with the original extension. If path is not given, the program saves the file to the original destination. If filename is not given the program uses the original name. Both parameters are optional. Inside the function the DocumentHandler.update() function is called. The mode parameter can be "dtw" or "lcs", it depends on which aligning method is wanted to using. The default is "dtw".


DocumentHandler.update(list_of_paragraphs=None,mode = "dtw")
----

Updates the content of the document. The length of list_of_paragraphs must be equal to the DocumentHandler.para list's length. The parameter is optional, if it's not given, the function uses the DocumentHandler.para list. The mode parameter can be "dtw" or "lcs", it depends on which aligning method is wanted to using. The default is "dtw".

DocumentHandler.Paragraph()
=======

Contains a paragraph and the original fragments of the paragraph. Inside a document a paragraph is splitted into fragments, it's necessary to keep them separately because the formatting is based on this structure.

DocumentHandler.Paragraph.fragments
------
List, that contains the fragments of the paragraph.


DocumentHandler.Paragraph.replace(old,new)
------

The classic string.replace() function, implemented to this costum structure. Iterates through the Paragraph.fragments list and calls the string.replace() function on each with the given parameters. 


DocumentHandler.Paragraph.update(new_paragraph, mode = "dtw")
------
Updates the paragraph. The new_paragraph parameter is the modified paragraph. This function attempts to split the new string, to fit to the old.
The mode parameter can be "dtw" or "lcs", it depends on which aligning method is wanted to using. The default is "dtw".

DocumentHandler.Paragraph.getParagraph() -> String
------

Joins and returns the contents of the Paragraph.fragments. It's the whole paragraph.

DocumentHandler.Paragraph.createParagraphList(list) -> List
------

The given list must contains Paragraph instances. The function calls the Paragraph.getParagraph() function on each, and makes a list of them and returns it.
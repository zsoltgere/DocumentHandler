DocumentHandler
=======

This is a program written in Python 3.4 to access text content of the supported document formats directly, and after costum manipulations the program is able to insert back the changed text into the original (or into a new) document. Only the modules of the Python Standard Library 3.4 are used by the program.

The currently supported document formats:  docx, odt, txt.

Documentation
-----------

DocumentHandler
=======

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

DocumentHandler.save(path=None, filename=None)
----

Saving the the document to the given path on the given name with the original extension. If path is not given, the program saves the file to the original destination. If filename is not given the program uses the original name. Both parameters are optional. Inside the function the DocumentHandler.update() function is called.

DocumentHandler.update(list_of_paragraphs=None)
----

Updates the content of the document. The length of list_of_paragraphs must be equal to the DocumentHandler.para list's length. The parameter is optional, if it's not given, the function uses the DocumentHandler.para list.

DocumentHandler.Paragraph()
=======

Contains a paragraph and the original fragments of the paragraph. Inside a document a paragraph is splitted into fragments, it's necessary to keep them separately because the formatting is based on this structure.



DocumentHandler.Paragraph.fragments
------
List, that contains the fragments of the paragraph.


DocumentHandler.Paragraph.replace(old,new)
------

The classic string.replace() function, implemented to this costum structure. Iterates through the Paragraph.fragments list and calls the string.replace() function on each with the given parameters. 


DocumentHandler.Paragraph.update(new)
------
Updates the paragraph. The new parameter is the modified paragraph. This function attempts to split the new string, to fit to the old.


DocumentHandler.Paragraph.getParagraph() -> String
------

Joins and returns the contents of the Paragraph.fragments. It's the whole paragraph.

DocumentHandler.Paragraph.createParagraphList(list) -> List
------

The given list must contains Paragraph instances. The function calls the Paragraph.getParagraph() function on each, and makes a list of them and returns it.


issues:
---------------

- more comment (already in progress)

TODO / IDEAS
--------------

- Support footnotes in docx/odt.
- Support the rtf format.
- Implement context manager (book: page 34)
#  -*- coding: utf-8 -*-
from lib.documentHandler import DocumentHandler

path="yourdocument.docx"

old="old"
new="new"

docx_handler=DocumentHandler(path)
# bekezdések kiolvasása
docx_paras = docx_handler.readall()

# A bekezdések módosítása DocumentHandler.para listán keresztül
for index,item in enumerate(docx_paras):
    docx_handler.para[index]=docx_paras[index].replace(old,new)

# manuális mentés szükséges ebben az esetben
docx_handler.save("output")

# vagy

with DocumentHandler(path) as docx_handler2:
    # A bekezdések módosítása DocumentHandler.para listán keresztül
    for index, item in enumerate(docx_handler2.para):
        docx_handler.para[index] = docx_paras[index].replace(old, new)
        docx_handler2.save()
# ebben az esetben nem kell menteni, ez automatikus

# vagy

docx_handler3=DocumentHandler(path)

new_paras=somespellcheckfunction(docx_handler3.readall())

docx_handler3.update(new_paras)

docx_handler3.save()















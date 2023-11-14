from docx import Document
import re
import codecs

def change_orientation(document):
    current_section = document.sections[-1]
    new_width, new_height = current_section.page_height, current_section.page_width
    new_section = document.add_section(Document.WD_SECTION.NEW_PAGE)
    new_section.orientation = Document.WD_ORIENT.LANDSCAPE
    new_section.page_width = new_width
    new_section.page_height = new_height

    return new_section


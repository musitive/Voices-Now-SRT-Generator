from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement,qn
from docx.enum.section import WD_SECTION, WD_ORIENT

import shutil
import re
import codecs

def changeOrientation(document) -> None:
    sections = document.sections

    for section in sections:
        # change orientation to landscape
        section.orientation = WD_ORIENT.LANDSCAPE

        new_width, new_height = section.page_height, section.page_width
        section.page_width = new_width
        section.page_height = new_height

    return

def removeMetadata(table) -> None:
    table._element.getparent().remove(table._element)
    return

def set_repeat_table_header(header_row):
    """ set repeat table row on every new page
    """
    tr = header_row._tr
    trPr = tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader')
    tblHeader.set(qn('w:val'), "true")
    trPr.append(tblHeader)
    return header_row

def prevent_document_break(document):
    """https://github.com/python-openxml/python-docx/issues/245#event-621236139
       Globally prevent table cells from splitting across pages.
    """
    tags = document.element.xpath('//w:tr')
    rows = len(tags)
    for row in range(0, rows):
        tag = tags[row]  # Specify which <w:r> tag you want
        child = OxmlElement('w:cantSplit')  # Create arbitrary tag
        tag.append(child)  # Append in the new tag

def set_widths(row):
    row.cells[0].width = Inches(0.5)
    row.cells[1].width = Inches(1)
    row.cells[2].width = Inches(1.5)
    row.cells[3].width = Inches(3)
    row.cells[4].width = Inches(3)

def shiftTranslation(old_row, new_row, text: str, document) -> None:
    new_row.cells[0].text = old_row.cells[0].text
    new_row.cells[0].paragraphs[0].style = document.styles['Normal']

    new_row.cells[1].text = text
    new_row.cells[1].paragraphs[0].style = document.styles['Normal']
    
    for n in range(1, len(old_row.cells)):
        new_row.cells[n+1].text = old_row.cells[n].text
        new_row.cells[n+1].paragraphs[0].style = document.styles['Normal']

    set_widths(new_row)
    return

def enhanceScript(filename: str, timecodeFilename: str) -> None:
    newFilename = "output.docx"

    document = Document(filename)
    timecodeFile = open(timecodeFilename, "r")

    style = document.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)

    changeOrientation(document)

    removeMetadata(document.tables[2])
    removeMetadata(document.tables[0])

    old_table = document.tables[0]

    new_table = document.add_table(1, 5)
    new_table.style = 'Table Grid'
    set_repeat_table_header(new_table.rows[0])

    old_rows = old_table.rows
    new_row = new_table.rows[0]

    for _ in range(12):
        timecodeFile.readline()
    shiftTranslation(old_rows[0], new_row, "TIMECODE", document)

    for old_row in old_rows[1:]:
        marker = timecodeFile.readline()
        # Split the marker data and timestamp
        _, timestamp, _, _, _, _ = re.split("\s+", marker)
        new_row = new_table.add_row()
        shiftTranslation(old_row, new_row, timestamp, document)

    prevent_document_break(document)

    document.save(newFilename)

    return

# Test Case
if __name__ == '__main__':
    enhanceScript("test.docx", "BMVL_308_Timecode.txt")
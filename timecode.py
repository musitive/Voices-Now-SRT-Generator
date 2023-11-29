from ProToolsMarkers import ProToolsMarkers

from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement,qn
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

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

def update_text(document, new_row, text: str, style: str, cell, bold: bool):
    run = new_row.cells[cell].paragraphs[0].add_run(text)
    new_row.cells[cell].paragraphs[0].style = document.styles[style]
    run.bold = bold
    # new_row.cells[cell].paragraphs[0].style.font.bold = bold

def shiftTranslation(old_row, new_row, text: str, document, bold: bool, style: str = 'Normal') -> None:
    update_text(document, new_row, old_row.cells[0].text, style, 0, bold)
    update_text(document, new_row, text, style, 1, bold)
    
    for n in range(1, len(old_row.cells)):
        update_text(document, new_row, old_row.cells[n].text, style, n+1, bold)

    set_widths(new_row)
    return

def color_cell(cell):
    shading_elm_1 = parse_xml(r'<w:shd {} w:fill="F6CC9E"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading_elm_1)

def enhance_script(filename: str, timecode_filename: str, new_filename: str) -> None:
    document = Document(filename)
    markers = ProToolsMarkers(timecode_filename)

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

    shiftTranslation(old_rows[0], new_row, "TIMECODE", document, True)
    for cell in new_row.cells:
        color_cell(cell)
    timecode_index = 0

    def get_next_marker():
        marker = markers.get_marker(timecode_index)
        name = marker.get_name()
        timecode_index += 1

        while name == 'x' or name == 'w':
            marker = markers.get_marker(timecode_index)
            name = marker.get_name()
            timecode_index += 1
            continue

        return marker

    for old_row in old_rows[1:]:
        marker = get_next_marker()
        
        location = marker.get_timecode_in_frames()

        new_row = new_table.add_row()
        shiftTranslation(old_row, new_row, location, document, False)

        timecode_index += 1

    prevent_document_break(document)

    removeMetadata(document.tables[0])

    document.save(new_filename)

    return

# Test Case
if __name__ == '__main__':
    enhance_script("test.docx", "BMVL_308_Timecode.txt", "output.docx")
from docx import Document
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

def shiftTranslation(row, content) -> None:
    row.cells[4].text = row.cells[3].text
    row.cells[3].text = row.cells[2].text
    row.cells[2].text = row.cells[1].text
    row.cells[1].text = content

def enhanceScript(filename: str, timecodeFilename: str) -> None:
    newFilename = "output.docx"

    document = Document(filename)
    timecodeFile = open(timecodeFilename, "r")

    changeOrientation(document)

    removeMetadata(document.tables[2])
    removeMetadata(document.tables[0])

    table = document.tables[0]
    table.add_column(table.columns[3].width)
    table.autofit = True
    rows = table.rows

    for _ in range(12):
        timecodeFile.readline()

    shiftTranslation(rows[0], "TIMECODE")

    for row in rows[1:]:
        marker = timecodeFile.readline()
        # Split the marker data and timestamp
        _, timestamp, _, _, _, _ = re.split("\s+", marker)
        shiftTranslation(row, timestamp)

    document.save(newFilename)

    return

# Test Case
if __name__ == '__main__':
    enhanceScript("test.docx", "BMVL_308_Timecode.txt")
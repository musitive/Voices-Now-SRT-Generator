from ProToolsMarkers import ProToolsMarkers
from LdsScript import LdsScript

from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.shared import OxmlElement,qn
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

import shutil
import re
import codecs

def enhance_script(filename: str, timecode_filename: str, new_filename: str) -> None:
    script = LdsScript(filename)
    markers = ProToolsMarkers(timecode_filename)

    script.set_styles()
    script.change_orientation()
    script.initialize_tables()

    timecode_index = 0
    translation_index = 1

    n = len(markers.get_markers())

    for timecode_index in range(n):
        marker = markers.get_marker(timecode_index)
        in_time = marker.get_timecode_in_frames()

        name = marker.get_name()
        if name == 'x' or name == 'END':
            timecode_index += 1
            continue

        script.add_row_to_new_table(translation_index, in_time)
        translation_index += 1


    script.prevent_document_break()
    script.remove_table(0)

    script.save_as_new_script(new_filename)

    return

# Test Case
if __name__ == '__main__':
    enhance_script("tests/test.docx", "tests/BMVL_308_Timecode.txt", "tests/output.docx")
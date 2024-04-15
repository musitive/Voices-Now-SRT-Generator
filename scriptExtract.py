"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

import SRTManager
from importlib import reload

reload(SRTManager)

from ProToolsMarkers import ProToolsMarkers
from LdsScript import LdsScript
from SRTManager import SRTManager


PRO_TOOLS_MARKER_START = 12         # Line that Pro Tools Marker data starts on

def create_srt_file(word_filename: str, timecode_filename: str, srt_filename: str, lang: str) -> None:
    # Open relevant documents
    markers = ProToolsMarkers(timecode_filename)                    # Open Pro Tools Marker file
    script = LdsScript(word_filename)                               # Open Word Document
    srt_manager = SRTManager(srt_filename, lang=lang)                          # Open SRT Manager

    # Variables and iterators
    n = markers.get_number_of_markers() # number of markers in the Pro Tools file
    translation_index = 1               # current cell we are on in columns, 0 being the title "TRANSLATION" and 1 being the first translated text

    # Get the first marker
    marker = markers.get_marker(0)

    # Modular index update function
    def update_indices(inc_translation: bool = True, inc_marker: bool = True):
        nonlocal marker, next_marker, timecode_index, translation_index
        timecode_index += 1
        if inc_translation:
            translation_index += 1
        if inc_marker:
            marker = next_marker

    for timecode_index in range(n):
        next_marker = markers.get_marker(timecode_index+1)
        if next_marker == None:
            break

        # Marker names that are not to be included in the SRT file
        if marker.name == 'x' or marker.name == 'END':
            update_indices(False)
            continue
        elif marker.name == 'w':
            update_indices()
            continue
        elif not marker.name.isnumeric():
            update_indices(False, False)
            continue

        # Get translation from Word Doc
        translation = script.get_translation(translation_index).replace("\n", "")

        # Skip grunts and efforts
        if translation == "(R)" or translation == "DO NOT TRANSLATE":
            update_indices()
            continue

        # Generate SRT text
        srt_manager.create_SRT_blocks(translation, marker.timecode, next_marker.timecode)

        update_indices()

    # Write SRTs to file
    srt_manager.write_SRTs_to_file()

    return

# Test Case
if __name__ == '__main__':
    create_srt_file("tests/BMVL_502_IND.docx", "tests/BMVL_502_timecode.txt", "tests/BMVL_502_IND_refactor.srt")
"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

from ProToolsMarkers import ProToolsMarkers
from LdsScript import LdsScript
from SRTInfo import SRTInfo
import codecs

MAX_CHARACTER_LEN = 88              # Maximum number of characters allow in an SRT caption
PRO_TOOLS_MARKER_START = 12         # Line that Pro Tools Marker data starts on

def create_srt_file(word_filename: str, timecode_filename: str, srt_filename: str) -> None:
    # Open relevant documents
    markers = ProToolsMarkers(timecode_filename)                    # Open Pro Tools Marker file
    script = LdsScript(word_filename)                               # Open Word Document
    srt_file = codecs.open(srt_filename, "w+", encoding="utf-8")    # Open SRT file

    # Variables and iterators
    n = markers.get_number_of_markers() # number of markers in the Pro Tools file
    srt_id = 1                          # current SRT number we are on, indexing starts at 1
    translation_index = 1               # current cell we are on in columns, 0 being the title "TRANSLATION" and 1 being the first translated text
    in_time = "00:00:00,000"            # timecode for the start of the current loop, defaulted to 0
    out_time = "00:00:00,000"           # timecode for the end of the current loop, defaulted to 0
    srts = []                           # list of SRTs to be written to the file

    # Get the first marker
    marker = markers.get_marker(0)

    # Modular index update function
    def update_indices():
        nonlocal marker, next_marker, in_time, out_time, timecode_index
        timecode_index += 1
        marker = next_marker
        in_time = out_time

    for timecode_index in range(n):
        next_marker = markers.get_marker(timecode_index+1)
        if next_marker == None:
            break
        out_time = next_marker.get_timecode_in_frames()

        name = marker.get_name()

        # Marker names that are not to be included in the SRT file
        if name == 'x' or name == 'END':
            update_indices()
            continue
        elif name == 'w':
            update_indices()
            translation_index += 1
            continue

        # Get translation from Word Doc
        translation = script.get_translation(translation_index).replace("\n", "")

        # Skip grunts and efforts
        if translation == "(R)":
            update_indices()
            translation_index += 1
            continue

        in_time = marker.get_timecode_in_ms()
        out_time = next_marker.get_timecode_in_ms()

        # Generate SRT text
        srts.append(SRTInfo(srt_id, in_time, out_time, translation))

        update_indices()
        translation_index += 1
        srt_id += 1


    # Write SRTs to file
    for srt in srts:
        srt_file.write(str(srt)+"\n")

    # Close related text files
    srt_file.close()

    return

# Test Case
if __name__ == '__main__':
    create_srt_file("tests/BMVL_502_IND.docx", "tests/BMVL_502_timecode.txt", "tests/BMVL_502_IND_refactor.srt")
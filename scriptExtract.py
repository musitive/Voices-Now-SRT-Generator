"""
Code to extract translation from an LDS script
Author: Dallin Frank

Build executable:
py -m PyInstaller -w --onefile "SRT Generator.py"
"""

from ProToolsMarkers import ProToolsMarkers
from LdsScript import LdsScript
import codecs

MAX_CHARACTER_LEN = 88              # Maximum number of characters allow in an SRT caption
PRO_TOOLS_MARKER_START = 12         # Line that Pro Tools Marker data starts on

def generateSRT(srtID: int, previousTime: str, nextTime: str, translation: str) -> str:
    text = str(srtID) + "\n"
    text += previousTime + " --> " + nextTime + "\n"
    text += translation + "\n\n"
    return text

def createSrtFile(wordFilename: str, timecodeFilename: str, srtFilename: str) -> None:
    # Open relevant documents
    markers = ProToolsMarkers(timecodeFilename)
    script = LdsScript(wordFilename)
    srtFile = codecs.open(srtFilename, "w+", encoding="utf-8")

    # Variables and iterators
    currentSrtId = 1                    # current SRT number we are on, indexing starts at 1
    translationRow = 1                  # current cell we are on in columns, 0 being the title "TRANSLATION" and 1 being the first translated text
    previousTimecode = "00:00:00,000"   # timecode for the previous loop, defaulted to 0
    currentTimecode = "00:00:00,000"    # timecode for the current loop, defaulted to 0

    # Iterate through the timecode file
    for marker in markers.get_markers():
        # Support for the "w" marker in Pro Tools
        if marker.get_name() == 'w':
            translationRow += 1
            continue

        # First index, since this is a backwards looking algorithm
        if script.newSection:
            previousTimecode = marker.get_timecode_in_ms()
            script.newSection = False
            continue

        # Get translation from Word Doc
        loopText = script.get_translation(translationRow)

        # Reformat Timecode
        currentTimecode = marker.get_timecode_in_ms()

        # Conditional Formatting here

        # Skip grunts and efforts
        if loopText == "(R)":
            previousTimecode = currentTimecode
            translationRow += 1
            continue

        # Generate SRT text
        srtText = generateSRT(currentSrtId, previousTimecode, currentTimecode, loopText)

        # print(srtText)

        # Add text to file
        srtFile.write(srtText)

        # Update iterators
        previousTimecode = currentTimecode
        translationRow += 1
        currentSrtId += 1

        # Support for the "x" marker in Pro Tools
        if marker.get_name() == 'x':
            script.newSection = True

    # Close related text files
    srtFile.close()

    return

# Test Case
if __name__ == '__main__':
    createSrtFile("test.docx", "BMVL_308_Timecode.txt", "refactor.txt")
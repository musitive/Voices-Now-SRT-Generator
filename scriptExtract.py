# Code to extract translation from an LDS script
# Author: Dallin Frank

# Build executable:
# py -m PyInstaller -w --onefile "SRT Generator.py"

from docx import Document
import re
import codecs

FRAME_RATE = 24                     # Number of frames per second, as determined by the video file
ROUNDING_RATE = 0.5                 # Determine whether to round up or down
MAX_CHARACTER_LEN = 88              # Maximum number of characters allow in an SRT caption
PRO_TOOLS_MARKER_START = 12         # Line that Pro Tools Marker data starts on

# Helper functions
def framesToMilliseconds(timestamp: str) -> str:
    delimiter = ":"
    _, m, s, f = re.split(delimiter, timestamp)
    millisec = int((int(f) * 1000) / FRAME_RATE + ROUNDING_RATE)
    return "00" + delimiter + m + delimiter + s + "," + "%(millisec)03d" % {'millisec': millisec}

def generateSRT(srtID: int, previousTime: str, nextTime: str, translation: str) -> str:
    text = str(srtID) + "\n"
    text += previousTime + " --> " + nextTime + "\n"
    text += translation + "\n\n"
    return text

def createSrtFile(wordFilename: str, timecodeFilename: str, srtFilename: str) -> None:
    # Open relevant documents
    document = Document(wordFilename)
    timecode = open(timecodeFilename, "r")
    srtFile = codecs.open(srtFilename, "w+", encoding="utf-8")

    # Python-docx set-up
    # Most LDS Translations should be in the second table, fourth column
    tables = document.tables
    columns = tables[1].columns
    translation = columns[3]
    newSection = True

    # Variables and iterators
    timecodeIndex = 0                   # timecode file iterator, starts at 0
    currentSrtId = 1                    # current SRT number we are on, indexing starts at 1
    translationRow = 1                  # current cell we are on in columns, 0 being the title "TRANSLATION" and 1 being the first translated text
    previousTimecode = "00:00:00,000"   # timecode for the previous loop, defaulted to 0
    currentTimecode = "00:00:00,000"    # timecode for the current loop, defaulted to 0

    # Iterate through the timecode file
    for marker in timecode:
        # Currently useless metadata from Pro Tools, skip it
        if timecodeIndex < 12:
            timecodeIndex += 1
            continue

        # Split the marker data and timestamp
        markerId, timestamp, _, _, loopNumber, _ = re.split("\s+", marker)

        # First index, since this is a backwards looking algorithm
        if newSection:
            timecodeIndex += 1
            previousTimecode = framesToMilliseconds(timestamp)
            newSection = False
            continue

        # Get translation from Word Doc
        loopText = translation.cells[translationRow].text

        # Reformat Timecode
        currentTimecode = framesToMilliseconds(timestamp)

        # Conditional Formatting here

        # Skip grunts and efforts
        if loopText == "(R)":
            previousTimecode = currentTimecode
            timecodeIndex += 1
            translationRow += 1
            continue

        # Generate SRT text
        srtText = generateSRT(currentSrtId, previousTimecode, currentTimecode, loopText)

        # print(srtText)

        # Add text to file
        srtFile.write(srtText)

        # Update iterators
        previousTimecode = currentTimecode
        timecodeIndex += 1
        translationRow += 1
        currentSrtId += 1

        # Support for the "x" marker in Pro Tools
        if loopNumber == 'x':
            newSection = True

    # Close related text files
    timecode.close()
    srtFile.close()

    return

# Test Case
if __name__ == '__main__':
    createSrtFile("test.docx", "test.txt", "test.srt")
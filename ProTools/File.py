"""
EXAMPLE File

Filename                                      	Location
BEEPS.1.wav                                   	Control D Internal:Users:studiod:Documents:BMVL:Season5:Tahitian:BMVL_501_TAH:Audio Files:
"""

from enum import Enum

class ColumnHeaders(Enum):
    FILENAME = "Filename"
    LOCATION = "Location"

class File:
    def __init__(self, filename: str, location: str):
        """Constructor for the File class
        
        Keyword arguments:
        filename: str -- the name of the file
        location: str -- the location of the file
        """

        self.filename = filename
        self.location = location